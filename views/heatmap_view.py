import streamlit as st
import numpy as np
from plots import plot_heatmap

def display_heatmaps(bs_model, input_data):
    st.subheader("Interactive Heatmaps")
    
    # Extract needed inputs
    spot_min = input_data["spot_min"]
    spot_max = input_data["spot_max"]
    vol_min = input_data["vol_min"]
    vol_max = input_data["vol_max"]
    strike = input_data["strike_price"]

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
    
    call_heatmap, put_heatmap = plot_heatmap(bs_model, spot_range, vol_range, strike)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(call_heatmap, width="stretch") # Updated parameter
    with col2:
        st.plotly_chart(put_heatmap, width="stretch") # Updated parameter