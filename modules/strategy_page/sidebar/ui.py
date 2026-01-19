import streamlit as st
from modules.strategy_page.logic.builder import build_strategy_legs
from utils.stock_data import get_stock_price
from utils.volatility_data import get_historical_vol
from models.bs_model import BlackScholes

def estimate_premium(market_params, strike, option_type):
    """
    Helper to calculate the theoretical Black-Scholes price for a leg.
    Order: Time, Strike, Spot, Volatility, Rate
    """
    bs = BlackScholes(
        market_params['T'],      
        strike,                  
        market_params['spot'],   
        market_params['sigma'],  
        market_params['r']       
    )
    call_price, put_price = bs.calculate_prices()
    return call_price if option_type == "Call" else put_price

def render_strategy_sidebar():
    """Renders a polished, beginner-friendly sidebar."""
    st.sidebar.title("Strategy Settings")

    # --- SECTION 1: DATA SOURCE (Yahoo Finance) ---
    st.sidebar.caption("📡 Data Source: **Yahoo Finance**")
    
    col1, col2 = st.sidebar.columns([2, 1])
    ticker = col1.text_input("Ticker Symbol", value="SPY", label_visibility="collapsed", placeholder="e.g. NVDA").upper()
    
    # Initialize State if missing
    if 'strat_spot' not in st.session_state: st.session_state['strat_spot'] = 100.0 
    if 'strat_vol' not in st.session_state: st.session_state['strat_vol'] = 20.0 
    
    if col2.button("Pull Data"):
        with st.spinner("Fetching..."):
            current_price = get_stock_price(ticker)
            current_vol = get_historical_vol(ticker, "1y")
            
            if current_price:
                st.session_state['strat_spot'] = current_price
                if current_vol:
                    st.session_state['strat_vol'] = current_vol * 100 
                else:
                    st.session_state['strat_vol'] = 20.0 
                
                # FORCE RELOAD: This fixes the "100 vs 186" mismatch
                st.rerun()
            else:
                st.sidebar.error("Ticker not found")

    # --- SECTION 2: MARKET CONTEXT (Grouped) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("1. Market Context")
    
    # We group these because a beginner usually just wants them "set and forget"
    with st.sidebar.container():
        # SPOT PRICE (Crucial)
        spot = st.number_input(
            "Underlying Price ($)", 
            value=float(st.session_state['strat_spot']), 
            step=0.5, 
            format="%.2f",
            help="The current price of the stock. Updated automatically via Yahoo Finance."
        )

        # EXPANDER for advanced/secondary inputs
        with st.expander("Show Volatility & Interest Rates", expanded=False):
            days = st.number_input(
                "Days to Expiry", 
                value=30, 
                min_value=1,
                help="How many days until the options expire."
            )
            vol = st.number_input(
                "Implied Volatility (%)", 
                value=float(st.session_state['strat_vol']), 
                step=1.0,
                help="Higher Volatility = More Expensive Options."
            )
            rate = st.number_input(
                "Risk-Free Rate (%)", 
                value=4.0, 
                step=0.1,
                help="The theoretical return of a 'safe' investment (like a T-Bill)."
            )

        # Pack params
        mp = {
            "T": days / 365.0,
            "sigma": vol / 100.0,
            "r": rate / 100.0,
            "spot": spot
        }

    # --- SECTION 3: STRATEGY (The Focus) ---
    st.sidebar.subheader("2. Design Strategy")
    
    strategy_type = st.sidebar.selectbox(
        "Select Strategy", 
        ["Straddle", "Long Strangle", "Bull Call Spread", "Bear Put Spread", "Iron Condor", "Custom"],
        help="Choose a pre-defined template or build your own."
    )
    
    params = {}
    
    # --- SMART INPUTS (Auto-Pricing) ---
    # We use columns to make it look less like a "List" and more like a "Form"
    
    if strategy_type == "Straddle":
        st.sidebar.info("ℹ️ **Straddle:** Profit if stock moves HUGE in *either* direction.")
        est_call = estimate_premium(mp, spot, "Call")
        est_put = estimate_premium(mp, spot, "Put")
        
        c1, c2 = st.sidebar.columns(2)
        params['premium_c'] = c1.number_input("Call Price", value=float(est_call), format="%.2f")
        params['premium_p'] = c2.number_input("Put Price", value=float(est_put), format="%.2f")
        
    elif strategy_type == "Long Strangle":
        st.sidebar.info("ℹ️ **Strangle:** Cheaper than a Straddle, but needs a bigger move.")
        dist = st.sidebar.number_input("Strike Distance", value=5.0, help="How far OTM (Out of the Money) should the legs be?")
        
        est_put = estimate_premium(mp, spot - dist, "Put")
        est_call = estimate_premium(mp, spot + dist, "Call")
        avg_prem = (est_put + est_call) / 2
        
        params['distance'] = dist
        params['premium'] = st.sidebar.number_input("Avg Leg Price", value=float(avg_prem), format="%.2f")

    elif strategy_type in ["Bull Call Spread", "Bear Put Spread"]:
        direction = "Bullish" if "Bull" in strategy_type else "Bearish"
        st.sidebar.info(f"ℹ️ **{strategy_type}:** A {direction} bet with capped risk and capped profit.")
        
        width = st.sidebar.number_input("Spread Width", value=5.0)
        is_call = "Call" in strategy_type
        
        est_long = estimate_premium(mp, spot, "Call" if is_call else "Put")
        strike_short = spot + width if is_call else spot - width
        est_short = estimate_premium(mp, strike_short, "Call" if is_call else "Put")
        
        params['width'] = width
        c1, c2 = st.sidebar.columns(2)
        params['premium_long'] = c1.number_input("Long (Buy)", value=float(est_long), format="%.2f")
        params['premium_short'] = c2.number_input("Short (Sell)", value=float(est_short), format="%.2f")
        
    elif strategy_type == "Iron Condor":
        st.sidebar.info("ℹ️ **Iron Condor:** Profit if the stock stays flat (Low Volatility).")
        width = st.sidebar.number_input("Wing Width", value=5.0)
        
        est_short_call = estimate_premium(mp, spot + width, "Call")
        est_long_call = estimate_premium(mp, spot + (2*width), "Call")
        
        params['width'] = width
        c1, c2 = st.sidebar.columns(2)
        params['premium_short'] = c1.number_input("Inner (Sell)", value=float(est_short_call), format="%.2f")
        params['premium_long'] = c2.number_input("Outer (Buy)", value=float(est_long_call), format="%.2f")

    # --- Build Legs ---
    if strategy_type == "Custom":
        legs = _render_custom_builder(spot, mp)
    else:
        legs = build_strategy_legs(strategy_type, spot, params)
        
    return legs, strategy_type, mp

def _render_custom_builder(spot, mp):
    if "custom_legs" not in st.session_state: st.session_state.custom_legs = []

    st.sidebar.markdown("### 🛠 Custom Builder")
    with st.sidebar.form("add_leg"):
        c1, c2 = st.columns(2)
        l_type = c1.selectbox("Type", ["Call", "Put"])
        l_pos = c2.selectbox("Side", ["Long", "Short"])
        
        l_strike = st.number_input("Strike Price", value=spot)
        l_prem = st.number_input("Premium ($)", value=1.0)
        
        if st.form_submit_button("Add Leg"):
            st.session_state.custom_legs.append({
                'strike': l_strike, 'premium': l_prem, 
                'type': l_type, 'position': l_pos
            })
            st.rerun()
            
    # Show active legs nicely
    if st.session_state.custom_legs:
        st.sidebar.caption(f"Active Legs: {len(st.session_state.custom_legs)}")
        if st.sidebar.button("Clear All"):
            st.session_state.custom_legs = []
            st.rerun()
        
    return st.session_state.custom_legs