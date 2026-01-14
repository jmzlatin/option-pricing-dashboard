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

# --- Initialize Session State for Inputs ---
if 'spot_price' not in st.session_state:
    st.session_state.spot_price = 100.0
if 'volatility' not in st.session_state:
    st.session_state.volatility = 20.0 # Default to 20%
if 'risk_free_rate' not in st.session_state:
    st.session_state.risk_free_rate = 4.0 # Default to 4%

# --- Sidebar: User Inputs ---
with st.sidebar:
    st.header("Market Data Parameters")
    
    # 1. Ticker Input
    ticker_input = st.text_input("Ticker Symbol (e.g. AAPL)", value="AAPL")
    
    # 2. Expiry Date
    today = date.today()
    default_expiry = today + timedelta(days=365)
    expiry_date = st.date_input("Expiry Date", value=default_expiry, min_value=today + timedelta(days=1))
    
    # Calculate Time to Maturity (T)
    days_to_expiry = (expiry_date - today).days
    time_to_maturity = days_to_expiry / 365.0
    st.caption(f"Time to Maturity: {days_to_expiry} days ({time_to_maturity:.2f} years)")

    # 3. Dynamic Fetch Button (Prices + Volatility + Risk Free Rate)
    if st.button("Fetch Market Data"):
        try:
            with st.spinner(f"Fetching data for {ticker_input}..."):
                # --- A. Stock Price ---
                ticker = yf.Ticker(ticker_input)
                history = ticker.history(period="1d")
                if not history.empty:
                    current_price = history['Close'].iloc[-1]
                    st.session_state.spot_price = float(current_price)
                    st.success(f"Spot Price: ${current_price:.2f}")
                
                # --- B. Smart Treasury Yield Selection ---
                # Select the right treasury note based on maturity
                if time_to_maturity <= 0.25:
                    treasury_ticker = "^IRX" # 13 Week Bill
                    rate_name = "13-Week T-Bill"
                elif time_to_maturity <= 5:
                    treasury_ticker = "^FVX" # 5 Year Note
                    rate_name = "5-Year T-Note"
                elif time_to_maturity <= 10:
                    treasury_ticker = "^TNX" # 10 Year Note
                    rate_name = "10-Year T-Note"
                else:
                    treasury_ticker = "^TYX" # 30 Year Bond
                    rate_name = "30-Year T-Bond"
                
                # Fetch Yield
                treasury_data = yf.Ticker(treasury_ticker).history(period="1d")
                if not treasury_data.empty:
                    market_rate = treasury_data['Close'].iloc[-1]
                    st.session_state.risk_free_rate = float(market_rate)
                    st.info(f"Risk-Free Rate ({rate_name}): {market_rate:.2f}%")

                # --- C. Volatility Logic ---
                if time_to_maturity < 0.25:
                    period = "3mo"
                elif time_to_maturity < 0.5:
                    period = "6mo"
                elif time_to_maturity < 1.0:
                    period = "1y"
                elif time_to_maturity < 2.0:
                    period = "2y"
                elif time_to_maturity < 5.0:
                    period = "5y"
                else:
                    period = "10y"
                
                hist_data = ticker.history(period=period)
                if len(hist_data) > 10: 
                    hist_data['Log Returns'] = np.log(hist_data['Close'] / hist_data['Close'].shift(1))
                    hist_vol = hist_data['Log Returns'].std() * np.sqrt(252)
                    st.session_state.volatility = float(hist_vol * 100) 
                    st.info(f"Vol ({period}): {hist_vol*100:.1f}%")
                else:
                    st.warning(f"Not enough data for {period} volatility.")

        except Exception as e:
            st.error(f"Error fetching data: {e}")

    st.markdown("---")
    
    # 4. Inputs (Linked to Session State)
    current_price = st.number_input("Current Asset Price", value=100.0, key="spot_price")
    strike_price = st.number_input("Strike Price", value=100.0)
    
    vol_input = st.number_input(
        "Volatility (%)", 
        value=20.00, 
        step=0.1, 
        format="%.2f", 
        key="volatility"
    )
    volatility = vol_input / 100.0
    
    # Risk Free Rate Input (Linked to key='risk_free_rate')
    rf_input = st.number_input(
        "Risk-Free Rate (%)", 
        value=4.00, 
        step=0.01, 
        format="%.2f",
        key="risk_free_rate"
    )
    risk_free_rate = rf_input / 100.0
    
    st.markdown("---")
    st.header("Heatmap Settings")
    spot_min = st.number_input("Min Spot Price", value=current_price*0.8)
    spot_max = st.number_input("Max Spot Price", value=current_price*1.2)
    vol_min_pct = st.slider("Min Volatility (%)", min_value=1.0, max_value=100.0, value=10.0)
    vol_max_pct = st.slider("Max Volatility (%)", min_value=1.0, max_value=100.0, value=30.0)

# --- Model Selection & Calculation ---
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

# --- Display Prices ---
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

# --- Display Greeks ---
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

# --- Advanced Visualization Tabs ---
st.subheader("Advanced Analysis")
viz_tab1, viz_tab2 = st.tabs(["🔥 Heatmap", "🧊 3D Greek Surface"])

with viz_tab1:
    st.write("Visualizing how Price changes with Spot & Volatility")
    spot_range = np.linspace(spot_min, spot_max, 10)
    
    # Convert slider percentages to decimals for the plot function
    vol_range = np.linspace(vol_min_pct, vol_max_pct, 10) / 100.0
    
    call_heatmap, put_heatmap = plot_heatmap(model, spot_range, vol_range, strike_price)
    
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.write("**Call Price Heatmap**")
        st.plotly_chart(call_heatmap, width='stretch')
    with h_col2:
        st.write("**Put Price Heatmap**")
        st.plotly_chart(put_heatmap, width='stretch')

with viz_tab2:
    st.write("Visualizing how Greeks sensitivity changes with Price & Time")
    
    greek_selector = st.selectbox("Select Greek", ["delta", "gamma", "theta", "vega", "rho"])
    
    surface_fig = plot_greek_surface(
        model_class=BlackScholes, 
        current_price=current_price,
        strike=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility, # Already converted to decimal above
        greek_type=greek_selector
    )
    
    st.plotly_chart(surface_fig, width='stretch')