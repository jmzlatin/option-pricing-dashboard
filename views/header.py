import streamlit as st

def display_header():
    # Custom CSS to adjust the styling
    st.markdown("""
    <style>
    .metric-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 8px;
        width: auto;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Black-Scholes Pricing Model")