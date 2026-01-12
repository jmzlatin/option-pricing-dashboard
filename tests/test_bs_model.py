import streamlit as st
import pandas as pd
import numpy as np
from bs_model import BlackScholes
from plots import plot_heatmap

# Page configuration
st.set_page_config(
    page_title="Option Pricing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to adjust the styling
st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    width: auto;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

st.title("Black-Scholes Pricing Model")

# Sidebar for User Inputs
with st.sidebar:
    st.header("📊 Model Parameters")
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    
    # Input as percentage (e.g. 5.0 for 5%)
    r_input = st.number_input("Risk-Free Interest Rate (%)", value=5.0, step=0.01)
    interest_rate = r_input / 100

    st.markdown("---")
    st.header("📉 Heatmap Parameters")
    spot_min = st.number_input("Min Spot Price", value=current_price*0.8)
    spot_max = st.number_input("Max Spot Price", value=current_price*1.2)
    vol_min = st.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.1)
    vol_max = st.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.3)

# Initialize Model
bs_model = BlackScholes(time_to_maturity, strike_price, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()
greeks = bs_model.calculate_greeks()

# Display Main Metrics (Prices)
st.subheader("Option Prices")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div style="text-align: center; background-color: #d4edda; padding: 10px; border-radius: 10px;">
            <h2 style="color: #155724;">Call Price</h2>
            <h1 style="color: #155724;">${call_price:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="text-align: center; background-color: #f8d7da; padding: 10px; border-radius: 10px;">
            <h2 style="color: #721c24;">Put Price</h2>
            <h1 style="color: #721c24;">${put_price:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

st.markdown("") # Spacing

# Display Greeks
st.subheader("Option Greeks")

# Create a container for the Greeks
greek_col1, greek_col2 = st.columns(2)

with greek_col1:
    st.info("Call Greeks")
    g_col1, g_col2, g_col3 = st.columns(3)
    g_col1.metric("Delta", f"{greeks['call']['delta']:.4f}")
    g_col2.metric("Gamma", f"{greeks['call']['gamma']:.4f}")
    g_col3.metric("Vega", f"{greeks['call']['vega']:.4f}")
    
    g_col1, g_col2 = st.columns(2)
    g_col1.metric("Theta", f"{greeks['call']['theta']:.4f}")
    g_col2.metric("Rho", f"{greeks['call']['rho']:.4f}")

with greek_col2:
    st.error("Put Greeks")
    g_col1, g_col2, g_col3 = st.columns(3)
    g_col1.metric("Delta", f"{greeks['put']['delta']:.4f}")
    g_col2.metric("Gamma", f"{greeks['put']['gamma']:.4f}")
    g_col3.metric("Vega", f"{greeks['put']['vega']:.4f}")
    
    g_col1, g_col2 = st.columns(2)
    g_col1.metric("Theta", f"{greeks['put']['theta']:.4f}")
    g_col2.metric("Rho", f"{greeks['put']['rho']:.4f}")

st.markdown("---")

# Heatmaps
st.subheader("Interactive Heatmaps")
spot_range = np.linspace(spot_min, spot_max, 10)
vol_range = np.linspace(vol_min, vol_max, 10)
call_heatmap, put_heatmap = plot_heatmap(bs_model, spot_range, vol_range, strike_price)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(call_heatmap, use_container_width=True)
with col2:
    st.plotly_chart(put_heatmap, use_container_width=True)