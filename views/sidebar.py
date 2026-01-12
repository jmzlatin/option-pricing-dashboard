import streamlit as st

def generate_sidebar():
    with st.sidebar:
        st.header("📊 Model Parameters")
        # NEW: Model Selection
        pricing_model = st.selectbox(
            "Pricing Model",
            ("Black-Scholes (European)", "Binomial (American)")
        )
        st.markdown("---")
        current_price = st.number_input("Current Asset Price", value=100.0)
        strike_price = st.number_input("Strike Price", value=100.0)
        time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
        volatility = st.number_input("Volatility (σ)", value=0.2)
        
        # Input as percentage (e.g. 5.0 for 5%)
        r_input = st.number_input("Risk-Free Interest Rate (%)", value=5.0, step=0.01)
        interest_rate = r_input / 100
        # NEW: Number of contracts to calculate total cost
        num_contracts = st.number_input("Number of Contracts", value=1, step=1)
        
        st.markdown("---")
        st.header("📉 Heatmap Parameters")
        spot_min = st.number_input("Min Spot Price", value=current_price*0.8)
        spot_max = st.number_input("Max Spot Price", value=current_price*1.2)
        vol_min = st.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.1)
        vol_max = st.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.3)
        
        st.markdown("---")
        with st.expander("ℹ️ User Guide"):
            st.markdown("""
            **Inputs**
            - **Spot Price:** Current market price of the asset.
            - **Strike Price:** The price at which the option can be exercised.
            - **Time to Maturity:** Time remaining until expiration (in years).
            - **Volatility (σ):** Annualized standard deviation of the asset's returns. Higher vol = higher option prices.
            - **Risk-Free Rate:** The theoretical return of an investment with zero risk.
            """)

    # Return a dictionary of all inputs
    return {
        "pricing_model": pricing_model,
        "current_price": current_price,
        "strike_price": strike_price,
        "time_to_maturity": time_to_maturity,
        "volatility": volatility,
        "interest_rate": interest_rate,
        "num_contracts": num_contracts,
        "spot_min": spot_min,
        "spot_max": spot_max,
        "vol_min": vol_min,
        "vol_max": vol_max
    }