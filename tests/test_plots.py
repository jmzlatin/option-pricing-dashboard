import pytest
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.bs_model import BlackScholes
from plots import plot_heatmap

def test_plot_heatmap_generation():
    # Setup dummy data
    model = BlackScholes(1, 100, 100, 0.2, 0.05)
    spot_range = np.linspace(80, 120, 10)
    vol_range = np.linspace(0.1, 0.5, 10)
    
    # Run the function
    fig_call, fig_put = plot_heatmap(model, spot_range, vol_range, model.K)
    
    # Check if we got Figure objects back
    assert isinstance(fig_call, go.Figure)
    assert isinstance(fig_put, go.Figure)
    
    # Check if data was actually populated (accessing the first trace's z-data)
    # Plotly stores data in a tuple of traces. We check the first one.
    assert fig_call.data[0].z is not None
    assert len(fig_call.data[0].z) > 0