import streamlit as st
from bs_model import BlackScholes

# Page configuration
st.set_page_config(
    page_title="Option Pricing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Black-Scholes Pricing Model")

# Sidebar for User Inputs
with st.sidebar:
    st.header("📊 Model Parameters")
    current_price = st.number_input("Current Asset Price", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

# Calculate Call and Put values
bs_model = BlackScholes(time_to_maturity, strike_price, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()

# Display Results
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Call Option Price", value=f"${call_price:.2f}")

with col2:
    st.metric(label="Put Option Price", value=f"${put_price:.2f}")