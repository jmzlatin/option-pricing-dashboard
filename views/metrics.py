import streamlit as st

def display_metrics(call_price, put_price):
    st.subheader("Option Prices")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div style="text-align: center; background-color: #d4edda; padding: 10px; border-radius: 10px;">
                <h2 style="color: #155724;">Call Price</h2>
                <h1 style="color: #155724;">${call_price:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="text-align: center; background-color: #f8d7da; padding: 10px; border-radius: 10px;">
                <h2 style="color: #721c24;">Put Price</h2>
                <h1 style="color: #721c24;">${put_price:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("") # Spacing