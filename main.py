import streamlit as st
from bs_model import BlackScholes
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

# 3. Initialize Model (Model)
bs_model = BlackScholes(
    time_to_maturity=input_data["time_to_maturity"],
    strike=input_data["strike_price"],
    current_price=input_data["current_price"],
    volatility=input_data["volatility"],
    interest_rate=input_data["interest_rate"]
)

# 4. Perform Calculations (Controller Logic)
call_price, put_price = bs_model.calculate_prices()
greeks = bs_model.calculate_greeks()

# 5. Display Output (Views)
display_metrics(call_price, put_price)
display_greeks(greeks)
display_heatmaps(bs_model, input_data)