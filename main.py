import streamlit as st
from bs_model import BlackScholes
from binomial_model import BinomialModel
from views.header import display_header
from views.sidebar import generate_sidebar
from views.metrics import display_metrics
from views.greeks import display_greeks
from views.heatmap_view import display_heatmaps

# Page configuration
st.set_page_config(
    page_title="Option Pricing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Setup Page
display_header()

# 2. Get User Inputs
input_data = generate_sidebar()

# 3. Model Logic
if input_data["pricing_model"] == "Black-Scholes (European)":
    # --- Black-Scholes Logic ---
    model = BlackScholes(
        time_to_maturity=input_data["time_to_maturity"],
        strike=input_data["strike_price"],
        current_price=input_data["current_price"],
        volatility=input_data["volatility"],
        interest_rate=input_data["interest_rate"]
    )
    
    call_price, put_price = model.calculate_prices()
    greeks = model.calculate_greeks()
    
    # Display Black-Scholes Outputs
    display_metrics(call_price, put_price, input_data["num_contracts"])
    display_greeks(greeks)
    display_heatmaps(model, input_data)

else:
    # --- Binomial Logic ---
    model = BinomialModel(
        S=input_data["current_price"],
        K=input_data["strike_price"],
        T=input_data["time_to_maturity"],
        r=input_data["interest_rate"],
        sigma=input_data["volatility"],
        steps=100
    )
    
    call_price = model.calculate_price(option_type='call', american=True)
    put_price = model.calculate_price(option_type='put', american=True)
    
    # Display Binomial Outputs
    display_metrics(call_price, put_price, input_data["num_contracts"])
    
    st.info("ℹ️ Greeks and Heatmaps are currently available only for the Black-Scholes model.")