import streamlit as st
import pandas as pd
import numpy as np
from models.bs_model import BlackScholes
from models.binomial import BinomialModel
from plots import plot_heatmap, plot_greek_surface

# Page configuration
st.set_page_config(
    page_title="Pricing Models",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for the Green/Red Price Cards ---
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
    color: #4a4a4a; /* <--- FIXED: Forces text to be dark grey, even in Dark Mode */
}
.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Option Pricing Models")

# --- Sidebar: User Inputs ---
with st.sidebar:
    st.header("Model Parameters")
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    risk_free_rate = st.number_input("Risk-Free Rate (%)", value=5.0) / 100
    
    st.markdown("---")
    st.header("Heatmap Settings")
    spot_min = st.number_input("Min Spot Price", value=current_price*0.8)
    spot_max = st.number_input("Max Spot Price", value=current_price*1.2)
    vol_min = st.slider("Min Volatility", min_value=0.01, max_value=1.0, value=0.1)
    vol_max = st.slider("Max Volatility", min_value=0.01, max_value=1.0, value=0.3)

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
    # Use BS for Greeks approximation to keep UI clean
    bs_temp = BlackScholes(time_to_maturity, strike_price, current_price, volatility, risk_free_rate)
    greeks = bs_temp.calculate_greeks()

# --- Display Prices (Restored Green/Red Cards) ---
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

st.markdown("") # Spacing

# --- Display Greeks (Restored Organized Tabs) ---
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

# --- Advanced Visualization Tabs (New 3D Surface Included) ---
st.subheader("Advanced Analysis")
viz_tab1, viz_tab2 = st.tabs(["🔥 Heatmap", "🧊 3D Greek Surface"])

with viz_tab1:
    st.write("Visualizing how Price changes with Spot & Volatility")
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
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
    
    # Selector for which Greek to view
    greek_selector = st.selectbox("Select Greek", ["delta", "gamma", "theta", "vega", "rho"])
    
    # Generate 3D Plot
    surface_fig = plot_greek_surface(
        model_class=BlackScholes, 
        current_price=current_price,
        strike=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        greek_type=greek_selector
    )
    
    st.plotly_chart(surface_fig, width='stretch')