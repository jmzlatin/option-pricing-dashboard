import streamlit as st
import numpy as np
import plotly.graph_objects as go
from models.strategies import calculate_payoff # We will reuse your existing logic if possible

def render_strategy_analysis(legs, strategy_name, spot_price=100):
    """Renders the Payoff Diagram and Leg Table."""
    if not legs:
        st.info("Select a strategy or add custom legs to see the payoff.")
        return

    st.subheader(f"Payoff Diagram: {strategy_name}")

    # 1. Determine X-Axis Range
    strikes = [leg['strike'] for leg in legs]
    min_s = min(strikes) if strikes else spot_price
    max_s = max(strikes) if strikes else spot_price
    margin = max(20, (max_s - min_s) * 0.5)
    
    spot_range = np.linspace(min_s - margin, max_s + margin, 200)
    
    # 2. Calculate Payoff (Vectorized)
    total_payoff = np.zeros_like(spot_range)
    
    for leg in legs:
        # Check if Call or Put
        if leg['type'] == 'Call':
            payoff = np.maximum(spot_range - leg['strike'], 0)
        else: # Put
            payoff = np.maximum(leg['strike'] - spot_range, 0)
            
        # Adjust for Premium
        if leg['position'] == 'Long':
            payoff = payoff - leg['premium']
        else: # Short
            payoff = leg['premium'] - payoff
            
        total_payoff += payoff

    # 3. Plot with Plotly
    fig = go.Figure()
    
    # Add Zero Line
    fig.add_hline(y=0, line_color="gray", line_dash="dash")
    
    # Add Payoff Curve
    fig.add_trace(go.Scatter(
        x=spot_range, 
        y=total_payoff, 
        mode='lines', 
        name='P&L',
        fill='tozeroy',
        line=dict(color='purple', width=3)
    ))
    
    # Mark Spot Price
    fig.add_vline(x=spot_price, line_color="orange", line_dash="dot", annotation_text="Spot")
    
    fig.update_layout(
        title=f"{strategy_name} P&L at Expiry",
        xaxis_title="Stock Price at Expiry",
        yaxis_title="Profit / Loss ($)",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # 4. Show Details
    with st.expander("View Strategy Composition"):
        st.table(legs)
