import streamlit as st
from utils.styles import get_custom_css

# --- MODULAR IMPORTS ---
from modules.pricing_page.sidebar.ui import render_sidebar
from modules.pricing_page.model_selection.ui import render_model_selector, render_step_slider
from modules.pricing_page.results.ui import render_prices, render_greeks
# NEW: Import Analysis Module
from modules.pricing_page.analysis.ui import render_analysis

from models.bs_model import BlackScholes
from models.binomial import BinomialModel

# Page configuration
st.set_page_config(page_title="Pricing Models", page_icon="📊", layout="wide")

# 1. Apply Styles
st.markdown(get_custom_css(), unsafe_allow_html=True)
st.title("📊 Option Pricing Models")

# 2. Initialize Session State
if 'spot_price' not in st.session_state: st.session_state.spot_price = 100.0
if 'volatility' not in st.session_state: st.session_state.volatility = 20.0 
if 'risk_free_rate' not in st.session_state: st.session_state.risk_free_rate = 4.0

# 3. Render Sidebar
params = render_sidebar()

# 4. Model Selection
model_choice = render_model_selector()

# 5. Run Logic
if model_choice == "Black-Scholes (European)":
    model = BlackScholes(params['T'], params['K'], params['S'], params['sigma'], params['r'])
    call_price, put_price = model.calculate_prices()
    greeks = model.calculate_greeks()
else:
    steps = render_step_slider()
    model = BinomialModel(params['T'], params['K'], params['S'], params['sigma'], params['r'], steps)
    call_price, put_price = model.calculate_prices()
    bs_temp = BlackScholes(params['T'], params['K'], params['S'], params['sigma'], params['r'])
    greeks = bs_temp.calculate_greeks()

# 6. Render Results
render_prices(call_price, put_price)
render_greeks(greeks)

# 7. Render Analysis
st.markdown("---")
render_analysis(model, params)