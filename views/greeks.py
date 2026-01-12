import streamlit as st

def display_greeks(greeks):
    st.subheader("Option Greeks")

    greek_col1, greek_col2 = st.columns(2)

    with greek_col1:
        st.info("Call Greeks")
        g_col1, g_col2, g_col3 = st.columns(3)
        g_col1.metric("Delta", f"{greeks['call']['delta']:.4f}")
        g_col2.metric("Gamma", f"{greeks['call']['gamma']:.4f}")
        g_col3.metric("Vega", f"{greeks['call']['vega']:.4f}")
        
        g_col1, g_col2 = st.columns(2)
        g_col1.metric("Theta", f"{greeks['call']['theta']:.4f}")
        g_col2.metric("Rho", f"{greeks['call']['rho']:.4f}")

    with greek_col2:
        st.error("Put Greeks")
        g_col1, g_col2, g_col3 = st.columns(3)
        g_col1.metric("Delta", f"{greeks['put']['delta']:.4f}")
        g_col2.metric("Gamma", f"{greeks['put']['gamma']:.4f}")
        g_col3.metric("Vega", f"{greeks['put']['vega']:.4f}")
        
        g_col1, g_col2 = st.columns(2)
        g_col1.metric("Theta", f"{greeks['put']['theta']:.4f}")
        g_col2.metric("Rho", f"{greeks['put']['rho']:.4f}")
    
    st.markdown("---")