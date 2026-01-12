import streamlit as st
import numpy as np
import plotly.graph_objects as go
from models.monte_carlo import MonteCarloPricing

st.set_page_config(page_title="Monte Carlo Simulation", layout="wide")

st.title("🎲 Monte Carlo Simulation")
st.markdown("Simulating future stock price paths using **Geometric Brownian Motion (GBM)**.")

# --- Sidebar Inputs ---
st.sidebar.header("Simulation Parameters")
S = st.sidebar.number_input("Spot Price", value=100.0)
K = st.sidebar.number_input("Strike Price", value=110.0)
T = st.sidebar.number_input("Time to Maturity (Years)", value=1.0)
vol = st.sidebar.number_input("Volatility (σ)", value=0.2)
r = st.sidebar.number_input("Risk-Free Rate (%)", value=5.0) / 100
sims = st.sidebar.slider("Number of Simulations", 1000, 50000, 10000)

# Run Simulation Button
if st.button("Run Simulation"):
    with st.spinner('Simulating thousands of market scenarios...'):
        # 1. Initialize and Run Model
        mc = MonteCarloPricing(S, K, T, r, vol, simulations=sims)
        paths = mc.simulate_paths()
        call_price = mc.calculate_price(paths, 'Call')
        put_price = mc.calculate_price(paths, 'Put')

        # 2. Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("Estimated Call Price", f"${call_price:.2f}")
        col2.metric("Estimated Put Price", f"${put_price:.2f}")

        # 3. Plot Paths (The "Bundle of Wires")
        # We only plot the first 50 paths to avoid crashing the browser
        st.subheader("Simulated Price Paths (First 50)")
        
        fig_paths = go.Figure()
        
        # X-axis (Time Steps)
        time_steps = np.linspace(0, T, mc.steps + 1)
        
        for i in range(50):
            fig_paths.add_trace(go.Scatter(
                x=time_steps, 
                y=paths[i, :], 
                mode='lines', 
                line=dict(width=1),
                opacity=0.6,
                showlegend=False
            ))
            
        # Add Strike Line
        fig_paths.add_hline(y=K, line_dash="dash", line_color="red", annotation_text="Strike Price")
        
        fig_paths.update_layout(
            xaxis_title="Time (Years)",
            yaxis_title="Stock Price",
            template="plotly_white"
        )
        st.plotly_chart(fig_paths, width="stretch")

        # 4. Histogram of Terminal Prices
        st.subheader("Distribution of Prices at Expiration")
        terminal_prices = paths[:, -1]
        
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=terminal_prices,
            nbinsx=50,
            marker_color='blue',
            opacity=0.7
        ))
        
        # Add vertical line for Strike
        fig_hist.add_vline(x=K, line_dash="dash", line_color="red", annotation_text="Strike")
        
        fig_hist.update_layout(
            xaxis_title="Price at Expiration",
            yaxis_title="Frequency",
            template="plotly_white"
        )
        st.plotly_chart(fig_hist, width="stretch")