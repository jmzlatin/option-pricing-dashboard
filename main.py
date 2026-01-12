import streamlit as st

st.set_page_config(
    page_title="Quant Options Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for the cards
st.markdown("""
    <style>
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:hover {
        background-color: #e1e4e8;
        transform: scale(1.02);
        transition: all 0.2s;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Quantitative Options Pricing Engine")
st.markdown("### Welcome to the Derivatives Analytics Suite")
st.markdown("""
This project demonstrates advanced financial engineering concepts using Python. 
Navigate to any module below to explore different pricing methodologies and risk visualizations.
""")

st.divider()

# Creating a 3-column layout for navigation cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊")
    st.subheader("Pricing Models")
    st.caption("Black-Scholes & Binomial")
    st.page_link("pages/1_Pricing_Models.py", label="Launch Model", icon="🚀")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🏗️")
    st.subheader("Strategy Builder")
    st.caption("Straddles & Iron Condors")
    st.page_link("pages/2_Strategy_Builder.py", label="Build Strategy", icon="🛠️")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🎲")
    st.subheader("Monte Carlo")
    st.caption("Stochastic Simulations")
    st.page_link("pages/3_Monte_Carlo.py", label="Run Simulation", icon="📉")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Footer / About Section
st.info("""
**Project Architecture:**
* **Tech Stack:** Python, Streamlit, NumPy, Plotly
* **Models:** Black-Scholes (European), Binomial Tree (American), Geometric Brownian Motion
* **Testing:** 100% Unit Test Coverage (Pytest)
""")