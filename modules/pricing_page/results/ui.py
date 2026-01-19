import streamlit as st

def render_prices(call_price, put_price):
    """Renders the colorful Call/Put price cards."""
    st.subheader("Option Prices")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card call-card">
                <div class="metric-label">Call Price</div>
                <div class="metric-value" style="color: #2c7a7b;">${call_price:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card put-card">
                <div class="metric-label">Put Price</div>
                <div class="metric-value" style="color: #c53030;">${put_price:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("") # Spacing

def render_greeks(greeks):
    """Renders the tabs for Call/Put Greeks."""
    st.subheader("Option Greeks")
    greek_tab1, greek_tab2 = st.tabs(["Call Greeks", "Put Greeks"])

    with greek_tab1:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Delta", f"{greeks['call']['delta']:.4f}")
        c2.metric("Gamma", f"{greeks['call']['gamma']:.4f}")
        c3.metric("Theta", f"{greeks['call']['theta']:.4f}")
        c4.metric("Vega", f"{greeks['call']['vega']:.4f}")
        c5.metric("Rho", f"{greeks['call']['rho']:.4f}")

    with greek_tab2:
        p1, p2, p3, p4, p5 = st.columns(5)
        p1.metric("Delta", f"{greeks['put']['delta']:.4f}")
        p2.metric("Gamma", f"{greeks['put']['gamma']:.4f}")
        p3.metric("Theta", f"{greeks['put']['theta']:.4f}")
        p4.metric("Vega", f"{greeks['put']['vega']:.4f}")
        p5.metric("Rho", f"{greeks['put']['rho']:.4f}")
    
    st.markdown("---")
