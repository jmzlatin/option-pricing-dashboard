import streamlit as st

st.set_page_config(
    page_title="Quant Options Dashboard",
    page_icon="⚡",
    layout="wide"
)

# --- Header ---
st.title("⚡ Quantitative Options Pricing Engine")
st.markdown("### Welcome to the Derivatives Analytics Suite")
st.markdown("""
This project demonstrates advanced financial engineering concepts using Python. 
Select a module below to launch the respective analysis tool.
""")

st.divider()

# --- Navigation Section ---
col1, col2, col3 = st.columns(3)

# Column 1: Pricing Models
with col1:
    st.header("📊")
    st.subheader("Pricing Models")
    st.markdown("Black-Scholes & Binomial Trees for European/American options.")
    st.page_link("pages/1_Pricing_Models.py", label="Launch Model", icon="🚀")

# Column 2: Strategy Builder
with col2:
    st.header("🏗️")
    st.subheader("Strategy Builder")
    st.markdown("Analyze PnL for Straddles, Iron Condors, and custom multi-leg trades.")
    st.page_link("pages/2_Strategy_Builder.py", label="Build Strategy", icon="🛠️")

# Column 3: Monte Carlo
with col3:
    st.header("🎲")
    st.subheader("Monte Carlo")
    st.markdown("Stochastic simulations using Geometric Brownian Motion (GBM).")
    st.page_link("pages/3_Monte_Carlo.py", label="Run Simulation", icon="📉")

st.divider()

# --- Footer ---
st.info("""
**Project Architecture:**
* **Tech Stack:** Python, Streamlit, NumPy, Plotly
* **Models:** Black-Scholes (European), Binomial Tree (American), Geometric Brownian Motion
* **Testing:** 100% Unit Test Coverage (Pytest)
""")