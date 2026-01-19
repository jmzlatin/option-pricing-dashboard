import streamlit as st
from datetime import datetime, timedelta, date
from utils.stock_data import get_stock_price
from utils.volatility_data import get_implied_vol, get_historical_vol
from utils.market_data import get_risk_free_rate

def render_sidebar():
    """Renders the sidebar and returns a dictionary of model parameters."""
    st.sidebar.header("Model Settings")

    # --- 1. LIVE DATA PULLER ---
    st.sidebar.caption("📡 Data Source: **Yahoo Finance**")
    col1, col2 = st.sidebar.columns([2, 1])
    ticker = col1.text_input("Ticker", value="SPY", label_visibility="collapsed").upper()
    
    if col2.button("Pull"):
        with st.spinner("Fetching..."):
            current_price = get_stock_price(ticker)
            fetched_rate = get_risk_free_rate()
            
            if current_price:
                st.session_state.spot_price = current_price
                st.session_state.risk_free_rate = fetched_rate * 100
                
                fetched_vol = get_implied_vol(ticker, target_strike=current_price)
                if fetched_vol:
                    st.session_state.volatility = fetched_vol * 100
                    st.toast(f"Loaded {ticker}: ${current_price} | IV: {fetched_vol:.1%}", icon="✅")
                else:
                    hv = get_historical_vol(ticker)
                    if hv: st.session_state.volatility = hv * 100
                    st.toast(f"Loaded {ticker} (IV missing, used HV)", icon="⚠️")
                
                st.rerun()
            else:
                st.sidebar.error("Ticker not found")

    st.sidebar.markdown("---")

    # --- 2. INPUTS ---
    # Spot Price
    S = st.sidebar.number_input("Spot Price ($)", value=float(st.session_state.spot_price), step=1.0, format="%.2f")
    
    # Strike Price
    K = st.sidebar.number_input("Strike Price ($)", value=float(st.session_state.spot_price), step=1.0, format="%.2f")
    
    # --- DATE SELECTOR (NEW) ---
    today = date.today()
    default_date = today + timedelta(days=30) # Default to 30 days out
    
    expiry_date = st.sidebar.date_input(
        "Expiration Date", 
        value=default_date, 
        min_value=today + timedelta(days=1), # Prevent picking past dates
        format="YYYY-MM-DD"
    )
    
    # Logic: Calculate T (Years) from the date
    days_to_expiry = (expiry_date - today).days
    T = days_to_expiry / 365.0
    
    # Show the user the calculated days
    st.sidebar.caption(f"📅 Days to Expiry: **{days_to_expiry}**")
    
    # Volatility
    sigma = st.sidebar.number_input("Volatility (%)", value=float(st.session_state.volatility), step=0.1)
    
    # Risk-Free Rate
    r = st.sidebar.number_input("Risk-Free Rate (%)", value=float(st.session_state.risk_free_rate), step=0.1)

    st.sidebar.markdown("---")
    
    return {
        "S": S,
        "K": K,
        "T": T,       # We pass the calculated float
        "sigma": sigma / 100.0,
        "r": r / 100.0,
        "spot_min": S * 0.8,
        "spot_max": S * 1.2,
        "vol_min": max(1.0, sigma * 0.5),
        "vol_max": sigma * 1.5
    }