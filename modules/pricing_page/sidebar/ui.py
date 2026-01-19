import streamlit as st
from datetime import date, timedelta

# Import the Brains (Logic)
from modules.pricing_page.sidebar.core_logic import (
    calculate_time_to_maturity,
    sanitize_ticker,
    select_treasury_ticker,
    select_volatility_period
)

# Import the Data Fetchers (Utils)
from utils.stock_data import get_stock_price
from utils.treasury_data import get_treasury_rate
from utils.volatility_data import get_historical_vol

def render_sidebar():
    """Renders the sidebar and returns a dictionary of model parameters."""
    with st.sidebar:
        st.header("Market Data Parameters")
        
        # --- 1. Ticker & Expiry Inputs ---
        ticker_input = st.text_input("Ticker Symbol (e.g. AAPL)", value="AAPL")
        
        today = date.today()
        default_expiry = today + timedelta(days=365)
        expiry_date = st.date_input(
            "Expiry Date", 
            value=default_expiry, 
            min_value=today + timedelta(days=1)
        )
        
        # Logic Call: Calculate Maturity
        T = calculate_time_to_maturity(today, expiry_date)
        days_to_expiry = (expiry_date - today).days
        st.caption(f"Time to Maturity: {days_to_expiry} days ({T:.2f} years)")

        # --- 2. Data Fetching Button ---
        if st.button("Fetch Market Data"):
            # Logic Call: Sanitize Input
            ticker_symbol = sanitize_ticker(ticker_input)
            
            with st.spinner(f"Fetching data for {ticker_symbol}..."):
                # A. Fetch Price
                price = get_stock_price(ticker_symbol)
                if price:
                    st.session_state.spot_price = float(price)
                    st.success(f"Spot Price ({ticker_symbol}): ${price:.2f}")
                else:
                    st.error(f"Could not fetch price for {ticker_symbol}")
                    st.stop()

                # B. Logic Call: Select Treasury Proxy
                tn_ticker, tn_name = select_treasury_ticker(T)
                
                # Fetch Rate
                rf_rate = get_treasury_rate(tn_ticker)
                if rf_rate:
                    st.session_state.risk_free_rate = float(rf_rate)
                    st.info(f"Risk-Free Rate ({tn_name}): {rf_rate:.2f}%")

                # C. Logic Call: Select Volatility Window
                vol_period = select_volatility_period(T)
                
                # Fetch Volatility
                vol = get_historical_vol(ticker_symbol, vol_period)
                if vol:
                    st.session_state.volatility = float(vol * 100)
                    st.info(f"Vol ({vol_period}): {vol*100:.1f}%")
                else:
                    st.warning(f"Could not calc volatility for {vol_period}")

        st.markdown("---")
        
        # --- 3. Manual Overrides (Linked to Session State) ---
        # If session state is empty, default to 100.0, 20.0, 4.0
        S = st.number_input("Current Asset Price", value=st.session_state.get('spot_price', 100.0), key="spot_price")
        K = st.number_input("Strike Price", value=st.session_state.get('spot_price', 100.0))
        
        vol_input = st.number_input("Volatility (%)", value=st.session_state.get('volatility', 20.0), step=0.1, format="%.2f", key="volatility")
        sigma = vol_input / 100.0
        
        rf_input = st.number_input("Risk-Free Rate (%)", value=st.session_state.get('risk_free_rate', 4.0), step=0.01, format="%.2f", key="risk_free_rate")
        r = rf_input / 100.0
        
        st.markdown("---")
        
        # --- 4. Heatmap Settings ---
        st.header("Heatmap Settings")
        spot_min = st.number_input("Min Spot Price", value=S*0.8)
        spot_max = st.number_input("Max Spot Price", value=S*1.2)
        vol_min = st.slider("Min Volatility (%)", min_value=1.0, max_value=100.0, value=10.0)
        vol_max = st.slider("Max Volatility (%)", min_value=1.0, max_value=100.0, value=30.0)
        
    return {
        "ticker": ticker_input,
        "T": T,
        "S": S,
        "K": K,
        "sigma": sigma,
        "r": r,
        "spot_min": spot_min,
        "spot_max": spot_max,
        "vol_min": vol_min,
        "vol_max": vol_max
    }
