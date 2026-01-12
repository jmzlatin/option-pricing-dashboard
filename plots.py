import plotly.graph_objects as go
import numpy as np

def plot_heatmap(model, spot_range, vol_range, strike):
    """
    Generates Heatmaps for Call and Put Prices.
    """
    # Initialize grids
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))
    
    # Loop through volatilities (Y-axis) and spots (X-axis)
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            # Temporarily update model inputs
            model.S = spot
            model.sigma = vol
            
            # Recalculate prices
            c, p = model.calculate_prices()
            call_prices[i, j] = c
            put_prices[i, j] = p

    # --- Plot Call Heatmap ---
    fig_call = go.Figure(data=go.Heatmap(
        z=call_prices,
        x=spot_range,
        y=vol_range,
        colorscale='Viridis',
        colorbar=dict(title='Price')
    ))
    fig_call.update_layout(
        title="Call Price Heatmap",
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        template="plotly_dark"
    )

    # --- Plot Put Heatmap ---
    fig_put = go.Figure(data=go.Heatmap(
        z=put_prices,
        x=spot_range,
        y=vol_range,
        colorscale='Plasma',
        colorbar=dict(title='Price')
    ))
    fig_put.update_layout(
        title="Put Price Heatmap",
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        template="plotly_dark"
    )

    return fig_call, fig_put

def plot_greek_surface(model_class, current_price, strike, time_to_maturity, risk_free_rate, volatility, greek_type="delta"):
    """
    Generates a 3D Surface plot for a specific Greek.
    X: Spot Price Range (+/- 20%)
    Y: Time to Maturity Range (0 to T)
    Z: Calculated Greek
    """
    # 1. Define the grid range
    spot_range = np.linspace(current_price * 0.8, current_price * 1.2, 50)
    time_range = np.linspace(0.01, time_to_maturity, 50) 
    
    # 2. Create the Meshgrid (2D arrays for X and Y)
    S_grid, T_grid = np.meshgrid(spot_range, time_range)
    
    # 3. Initialize a vectorized model with these GRIDS as inputs
    # The model calculates 2,500 points instantly
    bs_grid = model_class(
        time_to_maturity=T_grid,
        strike=strike,
        current_price=S_grid,
        volatility=volatility,
        interest_rate=risk_free_rate
    )
    
    # 4. Get the Greeks
    greeks_grid = bs_grid.calculate_greeks()
    
    # Extract the specific Z-axis data (default to Call greeks)
    Z = greeks_grid['call'][greek_type]
    
    # 5. Plot 3D Surface
    fig = go.Figure(data=[go.Surface(x=S_grid, y=T_grid, z=Z, colorscale='Viridis')])

    fig.update_layout(
        title=f"Call {greek_type.capitalize()} Surface",
        scene=dict(
            xaxis_title='Spot Price ($)',
            yaxis_title='Time to Expiry (Years)',
            zaxis_title=f'{greek_type.capitalize()}'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        template="plotly_dark"
    )
    
    return fig