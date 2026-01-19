import streamlit as st
from utils.styles import get_custom_css

# --- MODULAR IMPORTS ---
from modules.strategy_page.sidebar.ui import render_strategy_sidebar
from modules.strategy_page.analysis.ui import render_strategy_analysis

st.set_page_config(page_title="Strategy Builder", page_icon="🏗️", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("🏗️ Options Strategy Architect")

# 1. Sidebar (Returns the built legs)
legs, strategy_name = render_strategy_sidebar()

# 2. Main Analysis (Visualizes the legs)
render_strategy_analysis(legs, strategy_name)