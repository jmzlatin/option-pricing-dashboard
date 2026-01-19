import streamlit as st

def render_model_selector():
    """Renders the dropdown to select the pricing model."""
    return st.selectbox("Select Pricing Model", ["Black-Scholes (European)", "Binomial Tree (American)"])

def render_step_slider():
    """Renders the slider for Binomial Tree steps."""
    return st.slider("Number of Steps (Tree Depth)", 10, 100, 50)
