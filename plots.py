import plotly.graph_objects as go
import numpy as np
from models.bs_model import BlackScholes

def plot_heatmap(bs_model, spot_range, vol_range, strike):
    # Create a grid of Spot Prices and Volatilities
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            # Create a temp model for each grid point
            temp_model = BlackScholes(
                time_to_maturity=bs_model.T,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.r
            )
            c, p = temp_model.calculate_prices()
            call_prices[i, j] = c
            put_prices[i, j] = p

    # Create the Heatmap for Calls
    fig_call = go.Figure(data=go.Heatmap(
        z=call_prices,
        x=spot_range,
        y=vol_range,
        colorscale='Viridis',
        colorbar=dict(title='Price')
    ))
    fig_call.update_layout(
        title='Call Price Heatmap',
        xaxis_title='Spot Price',
        yaxis_title='Volatility',
        height=400
    )

    # Create the Heatmap for Puts
    fig_put = go.Figure(data=go.Heatmap(
        z=put_prices,
        x=spot_range,
        y=vol_range,
        colorscale='Plasma',
        colorbar=dict(title='Price')
    ))
    fig_put.update_layout(
        title='Put Price Heatmap',
        xaxis_title='Spot Price',
        yaxis_title='Volatility',
        height=400
    )

    return fig_call, fig_put