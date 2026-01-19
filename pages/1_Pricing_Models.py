import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, timedelta
from models.bs_model import BlackScholes
from models.binomial import BinomialModel
from plots import plot_heatmap, plot_greek_surface

# Page configuration
st.set_page_config(
    page_title="Pricing Models",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
.metric-card {
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
.call-card {
    background-color: #e6fffa; /* Light Green */
    border: 2px solid #38b2ac;
}
.put-card {
    background-color: #fff5f5; /* Light Red */
    border: 2px solid #fc8181;
}
.metric-label {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 5px;
    color: #4a4a4a; 
}
.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Option Pricing Models")

# --- Initialize Session State ---
if 'spot_price' not in st.session_state:
    st.session_state.spot_price = 100.0
if 'volatility' not in st.session_state:
    st.session_state.volatility = 20.0 
if 'risk_free_rate' not in st.session_state:
    st.session_state.risk_free_rate = 4.0

# --- Helper Function: Caching to prevent 429 Errors ---
@st.cache_data(ttl=300) # Cache for 5 minutes
def get_stock_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return None
        return history['Close'].iloc[-1]
    except:
        return None

@st.cache_data(ttl=300)
def get_treasury_rate(ticker_symbol):
    try:
        data = yf.Ticker(ticker_symbol).history(period="1d")
        if data.empty:
            return None
        return data['Close'].iloc[-1]
    except:
        return None

@st.cache_data(ttl=300)
def get_historical_vol(ticker_symbol, period):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist_data = ticker.history(period=period)
        if len(hist_data) > 10:
            hist_data['Log Returns'] = np.log(hist_data['Close'] / hist_data['Close'].shift(1))
            hist_vol = hist_data['Log Returns'].std() * np.sqrt(252)
            return hist_vol
        return None
    except:
        return None

# --- Sidebar: User Inputs ---
with st.sidebar:
    st.header("Market Data Parameters")
    
    ticker_input = st.text_input("Ticker Symbol (e.g. AAPL)", value="AAPL")
    
    today = date.today()
    default_expiry = today + timedelta(days=365)
    expiry_date = st.date_input("Expiry Date", value=default_expiry, min_value=today + timedelta(days=1))
    
    days_to_expiry = (expiry_date - today).days
    time_to_maturity = days_to_expiry / 365.0
    st.caption(f"Time to Maturity: {days_to_expiry} days ({time_to_maturity:.2f} years)")

    if st.button("Fetch Market Data"):
        ticker_symbol = ticker_input.upper() # Force Uppercase
        
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            # 1. Fetch Price
            price = get_stock_data(ticker_symbol)
            if price:
                st.session_state.spot_price = float(price)
                st.success(f"Spot Price ({ticker_symbol}): ${price:.2f}")
            else:
                st.error(f"Could not fetch price for {ticker_symbol}")
                st.stop()

            # 2. Smart Treasury Logic
            if time_to_maturity <= 2.0:
                tn_ticker = "^IRX"
                tn_name = "13-Week T-Bill"
            elif time_to_maturity <= 5.0:
                tn_ticker = "^FVX"
                tn_name = "5-Year T-Note"
            elif time_to_maturity <= 10.0:
                tn_ticker = "^TNX"
                tn_name = "10-Year T-Note"
            else:
                tn_ticker = "^TYX"
                tn_name = "30-Year T-Bond"

            rf_rate = get_treasury_rate(tn_ticker)
            if rf_rate:
                st.session_state.risk_free_rate = float(rf_rate)
                st.info(f"Risk-Free Rate ({tn_name}): {rf_rate:.2f}%")

            # 3. Volatility Logic
            if time_to_maturity < 0.25: vol_period = "3mo"
            elif time_to_maturity < 0.5: vol_period = "6mo"
            elif time_to_maturity < 1.0: vol_period = "1y"
            elif time_to_maturity < 2.0: vol_period = "2y"
            elif time_to_maturity < 5.0: vol_period = "5y"
            else: vol_period = "10y"
            
            vol = get_historical_vol(ticker_symbol, vol_period)
            if vol:
                st.session_state.volatility = float(vol * 100)
                st.info(f"Vol ({vol_period}): {vol*100:.1f}%")
            else:
                st.warning(f"Could not calc volatility for {vol_period}")

    st.markdown("---")
    
    # Inputs linked to Session State
    current_price = st.number_input("Current Asset Price", value=100.0, key="spot_price")
    strike_price = st.number_input("Strike Price", value=100.0)
    
    vol_input = st.number_input("Volatility (%)", value=20.00, step=0.1, format="%.2f", key="volatility")
    volatility = vol_input / 100.0
    
    rf_input = st.number_input("Risk-Free Rate (%)", value=4.00, step=0.01, format="%.2f", key="risk_free_rate")
    risk_free_rate = rf_input / 100.0
    
    st.markdown("---")
    st.header("Heatmap Settings")
    spot_min = st.number_input("Min Spot Price", value=current_price*0.8)
    spot_max = st.number_input("Max Spot Price", value=current_price*1.2)
    
    # These are the variables we need to match below
    vol_min_pct = st.slider("Min Volatility (%)", min_value=1.0, max_value=100.0, value=10.0)
    vol_max_pct = st.slider("Max Volatility (%)", min_value=1.0, max_value=100.0, value=30.0)

# --- Model Execution ---
model_choice = st.selectbox("Select Pricing Model", ["Black-Scholes (European)", "Binomial Tree (American)"])

if model_choice == "Black-Scholes (European)":
    model = BlackScholes(time_to_maturity, strike_price, current_price, volatility, risk_free_rate)
    call_price, put_price = model.calculate_prices()
    greeks = model.calculate_greeks()
else:
    steps = st.slider("Number of Steps (Tree Depth)", 10, 100, 50)
    model = BinomialModel(time_to_maturity, strike_price, current_price, volatility, risk_free_rate, steps)
    call_price, put_price = model.calculate_prices()
    bs_temp = BlackScholes(time_to_maturity, strike_price, current_price, volatility, risk_free_rate)
    greeks = bs_temp.calculate_greeks()

# --- Display Section ---
st.subheader("Option Prices")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
        <div class="metric-card call-card">
            <div class="metric-label">Call Price</div>
            <div class="metric-value" style="color: #2c7a7b;">${call_price:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card put-card">
            <div class="metric-label">Put Price</div>
            <div class="metric-value" style="color: #c53030;">${put_price:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("") 

st.subheader("Option Greeks")
greek_tab1, greek_tab2 = st.tabs(["Call Greeks", "Put Greeks"])
with greek_tab1:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Delta", f"{greeks['call']['delta']:.4f}")
    c2.metric("Gamma", f"{greeks['call']['gamma']:.4f}")
    c3.metric("Theta", f"{greeks['call']['theta']:.4f}")
    c4.metric("Vega", f"{greeks['call']['vega']:.4f}")
    c5.metric("Rho", f"{greeks['call']['rho']:.4f}")
with greek_tab2:
    p1, p2, p3, p4, p5 = st.columns(5)
    p1.metric("Delta", f"{greeks['put']['delta']:.4f}")
    p2.metric("Gamma", f"{greeks['put']['gamma']:.4f}")
    p3.metric("Theta", f"{greeks['put']['theta']:.4f}")
    p4.metric("Vega", f"{greeks['put']['vega']:.4f}")
    p5.metric("Rho", f"{greeks['put']['rho']:.4f}")

st.markdown("---")
st.subheader("Advanced Analysis")
viz_tab1, viz_tab2 = st.tabs(["🔥 Heatmap", "🧊 3D Greek Surface"])

with viz_tab1:
    st.write("Visualizing how Price changes with Spot & Volatility")
    spot_range = np.linspace(spot_min, spot_max, 10)
    
    # FIXED: Using vol_max_pct instead of vol_max
    vol_range = np.linspace(vol_min_pct, vol_max_pct, 10) / 100.0
    
    call_heatmap, put_heatmap = plot_heatmap(model, spot_range, vol_range, strike_price)
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.write("**Call Price Heatmap**")
        st.plotly_chart(call_heatmap, width="stretch")
    with h_col2:
        st.write("**Put Price Heatmap**")
        st.plotly_chart(put_heatmap, width="stretch")

with viz_tab2:
    st.write("Visualizing how Greeks sensitivity changes with Price & Time")
    greek_selector = st.selectbox("Select Greek", ["delta", "gamma", "theta", "vega", "rho"])
    surface_fig = plot_greek_surface(
        model_class=BlackScholes, 
        current_price=current_price,
        strike=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        greek_type=greek_selector
    )
    st.plotly_chart(surface_fig, width="stretch")