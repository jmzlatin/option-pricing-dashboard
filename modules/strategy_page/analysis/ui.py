import streamlit as st
import numpy as np
import plotly.graph_objects as go
from modules.strategy_page.logic.greeks import calculate_net_greeks

def render_strategy_analysis(legs, strategy_name, market_params):
    """Renders the Risk Dashboard, Payoff Diagram, and Leg Table."""
    if not legs:
        st.info("Select a strategy or add custom legs to see the payoff.")
        return

    st.subheader(f"Strategy Analysis: {strategy_name}")

    # --- 1. Risk Dashboard (Net Greeks) ---
    # Calculate using the market params from sidebar
    net_greeks = calculate_net_greeks(
        legs, 
        market_params['spot'], 
        market_params['T'], 
        market_params['r'], 
        market_params['sigma']
    )
    
    st.caption("Net Portfolio Greeks (Theoretical Risk Exposure)")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Net Delta", f"{net_greeks['delta']:.2f}", help="Price Sensitivity")
    g2.metric("Net Theta", f"{net_greeks['theta']:.2f}", help="Daily Time Decay")
    g3.metric("Net Gamma", f"{net_greeks['gamma']:.3f}", help="Acceleration of Delta")
    g4.metric("Net Vega",  f"{net_greeks['vega']:.2f}",  help="Volatility Sensitivity")
    
    st.markdown("---")

    # --- 2. Payoff Diagram ---
    spot_price = market_params['spot']
    strikes = [leg['strike'] for leg in legs]
    min_s = min(strikes) if strikes else spot_price
    max_s = max(strikes) if strikes else spot_price
    margin = max(20, (max_s - min_s) * 0.5)
    
    spot_range = np.linspace(min_s - margin, max_s + margin, 200)
    total_payoff = np.zeros_like(spot_range)
    
    for leg in legs:
        if leg['type'] == 'Call':
            payoff = np.maximum(spot_range - leg['strike'], 0)
        else:
            payoff = np.maximum(leg['strike'] - spot_range, 0)
            
        if leg['position'] == 'Long':
            payoff = payoff - leg['premium']
        else:
            payoff = leg['premium'] - payoff
        total_payoff += payoff

    fig = go.Figure()
    fig.add_hline(y=0, line_color="gray", line_dash="dash")
    fig.add_trace(go.Scatter(
        x=spot_range, y=total_payoff, 
        mode='lines', name='P&L', fill='tozeroy',
        line=dict(color='purple', width=3)
    ))
    fig.add_vline(x=spot_price, line_color="orange", line_dash="dot", annotation_text="Spot")
    
    fig.update_layout(
        title=f"Profit/Loss at Expiry",
        xaxis_title="Stock Price",
        yaxis_title="P&L ($)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # 3. Details
    with st.expander("View Strategy Composition"):
        st.table(legs)