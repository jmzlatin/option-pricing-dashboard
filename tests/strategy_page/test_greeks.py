import pytest
from modules.strategy_page.logic.greeks import calculate_net_greeks

PARAMS = {'spot': 100.0, 'T': 1.0, 'r': 0.05, 'sigma': 0.2}

def test_long_call_greeks():
    # Long Call = Positive Delta, Negative Theta
    legs = [{'strike': 100.0, 'type': 'Call', 'position': 'Long', 'premium': 10}]
    greeks = calculate_net_greeks(legs, **PARAMS)
    assert greeks['delta'] > 0.5 
    assert greeks['theta'] < 0

def test_short_call_greeks():
    # Short Call = Negative Delta, Positive Theta
    legs = [{'strike': 100.0, 'type': 'Call', 'position': 'Short', 'premium': 10}]
    greeks = calculate_net_greeks(legs, **PARAMS)
    assert greeks['delta'] < -0.5
    assert greeks['theta'] > 0

def test_atm_straddle_neutrality():
    # Straddle = Delta Neutral (approx 0), High Gamma
    legs = [
        {'strike': 100.0, 'type': 'Call', 'position': 'Long', 'premium': 5},
        {'strike': 100.0, 'type': 'Put', 'position': 'Long', 'premium': 5}
    ]
    greeks = calculate_net_greeks(legs, **PARAMS)
    assert -0.2 < greeks['delta'] < 0.3
    assert greeks['gamma'] > 0.02
