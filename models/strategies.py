import numpy as np
import plotly.graph_objects as go

def calculate_payoff(spot_prices, strike_price, premium, option_type, position_type):
    """
    Calculates PnL for a single option leg over a range of spot prices.
    position_type: 'Long' (Buy) or 'Short' (Sell)
    """
    if option_type == "Call":
        intrinsic_value = np.maximum(spot_prices - strike_price, 0)
    else:
        intrinsic_value = np.maximum(strike_price - spot_prices, 0)
    
    if position_type == "Long":
        # profit = intrinsic value - cost to buy
        return intrinsic_value - premium
    else:
        # profit = money received - intrinsic value liability
        return premium - intrinsic_value

def plot_strategy(spot_range, strategy_name, legs):
    """
    legs: List of dictionaries like:
    {'strike': 100, 'premium': 5, 'type': 'Call', 'position': 'Long'}
    """
    total_pnl = np.zeros_like(spot_range)
    
    fig = go.Figure()

    # Calculate PnL for each leg and add to total
    for leg in legs:
        pnl = calculate_payoff(spot_range, leg['strike'], leg['premium'], leg['type'], leg['position'])
        total_pnl += pnl
        
    # Plot the Total Strategy PnL (Thick Line)
    fig.add_trace(go.Scatter(
        x=spot_range, y=total_pnl, 
        mode='lines', 
        name='Total P&L',
        line=dict(color='blue', width=4),
        fill='tozeroy',  # Shade area under curve
    ))

    # Add reference line at $0
    fig.add_hline(y=0, line_dash="dash", line_color="black")

    fig.update_layout(
        title=f"Strategy Payoff: {strategy_name}",
        xaxis_title="Stock Price at Expiration",
        yaxis_title="Profit / Loss ($)",
        template="plotly_white"
    )
    
    return fig