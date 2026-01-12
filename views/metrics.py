import streamlit as st

def display_metrics(call_price, put_price, num_contracts):
    st.subheader("Option Prices & Total Premium")
    
    # Calculate Total Premium (Price * 100 shares * N contracts)
    call_total = call_price * 100 * num_contracts
    put_total = put_price * 100 * num_contracts

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div style="text-align: center; background-color: #d4edda; padding: 10px; border-radius: 10px;">
                <h2 style="color: #155724;">Call Price (Per Share)</h2>
                <h1 style="color: #155724;">${call_price:.2f}</h1>
                <p style="color: #155724; font-size: 18px;">
                    Total Premium ({num_contracts} Contracts): <b>${call_total:,.2f}</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="text-align: center; background-color: #f8d7da; padding: 10px; border-radius: 10px;">
                <h2 style="color: #721c24;">Put Price (Per Share)</h2>
                <h1 style="color: #721c24;">${put_price:.2f}</h1>
                <p style="color: #721c24; font-size: 18px;">
                    Total Premium ({num_contracts} Contracts): <b>${put_total:,.2f}</b>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("") # Spacing