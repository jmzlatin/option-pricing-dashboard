import streamlit as st
from modules.strategy_page.logic.builder import build_strategy_legs

def render_strategy_sidebar():
    """Renders sidebar inputs and returns the constructed legs + market params."""
    st.sidebar.header("Strategy Settings")
    spot = st.sidebar.number_input("Current Spot Price", value=100.0, step=1.0)
    
    # --- Market Assumptions (NEW) ---
    with st.sidebar.expander("Market Assumptions (for Risk)", expanded=False):
        days = st.number_input("Days to Expiry", value=30, min_value=1)
        vol = st.number_input("Volatility (%)", value=20.0, step=1.0)
        rate = st.number_input("Risk-Free Rate (%)", value=4.0, step=0.1)
        
        # Pack these for the logic layer
        market_params = {
            "T": days / 365.0,
            "sigma": vol / 100.0,
            "r": rate / 100.0,
            "spot": spot
        }
    
    strategy_type = st.sidebar.selectbox(
        "Select Strategy", 
        ["Straddle", "Long Strangle", "Bull Call Spread", "Bear Put Spread", "Iron Condor", "Custom"]
    )
    
    params = {}
    st.sidebar.markdown("---")
    
    # --- Dynamic Inputs ---
    if strategy_type == "Straddle":
        st.sidebar.caption("Setup: Buy Call + Buy Put at ATM.")
        params['premium_c'] = st.sidebar.number_input("Call Premium", 2.50)
        params['premium_p'] = st.sidebar.number_input("Put Premium", 3.00)
        
    elif strategy_type == "Long Strangle":
        st.sidebar.caption("Setup: Buy OTM Put + Buy OTM Call.")
        params['distance'] = st.sidebar.number_input("Strike Distance", 5.0)
        params['premium'] = st.sidebar.number_input("Leg Premium", 1.50)
        
    elif strategy_type in ["Bull Call Spread", "Bear Put Spread"]:
        st.sidebar.caption("Setup: Buy ATM + Sell OTM.")
        params['width'] = st.sidebar.number_input("Spread Width", 5.0)
        params['premium_long'] = st.sidebar.number_input("Long Premium", 4.0)
        params['premium_short'] = st.sidebar.number_input("Short Premium", 1.5)
        
    elif strategy_type == "Iron Condor":
        st.sidebar.caption("Setup: Sell Inner Strangle + Buy Outer Wings.")
        params['width'] = st.sidebar.number_input("Wing Width", 5.0)
        params['premium_short'] = st.sidebar.number_input("Short Premium (Inner)", 2.0)
        params['premium_long'] = st.sidebar.number_input("Long Premium (Outer)", 0.5)

    # --- Build Legs ---
    if strategy_type == "Custom":
        legs = _render_custom_builder(spot)
    else:
        legs = build_strategy_legs(strategy_type, spot, params)
        
    return legs, strategy_type, market_params

def _render_custom_builder(spot):
    """Helper for the Custom Builder UI."""
    if "custom_legs" not in st.session_state:
        st.session_state.custom_legs = []

    st.sidebar.write("### Custom Leg Builder")
    with st.sidebar.form("add_leg"):
        l_type = st.selectbox("Type", ["Call", "Put"])
        l_pos = st.selectbox("Position", ["Long", "Short"])
        l_strike = st.number_input("Strike", value=spot)
        l_prem = st.number_input("Premium", value=1.0)
        if st.form_submit_button("Add Leg"):
            st.session_state.custom_legs.append({
                'strike': l_strike, 'premium': l_prem, 
                'type': l_type, 'position': l_pos
            })
            
    if st.sidebar.button("Clear Legs"):
        st.session_state.custom_legs = []
        
    return st.session_state.custom_legs