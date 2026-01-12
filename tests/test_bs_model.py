import pytest
from models.bs_model import BlackScholes

def test_call_price_calculation():
    """
    Checks if the Call price is calculated correctly for standard inputs.
    S=100, K=100, T=1, r=0.05, sigma=0.2 -> Call should be ~10.45
    """
    bs = BlackScholes(time_to_maturity=1, strike=100, current_price=100, volatility=0.2, interest_rate=0.05)
    call_price, _ = bs.calculate_prices()
    
    # Assert checks if the math is correct within a small margin of error
    assert abs(call_price - 10.4506) < 0.01

def test_put_price_calculation():
    """
    Checks if the Put price is calculated correctly.
    S=100, K=100, T=1, r=0.05, sigma=0.2 -> Put should be ~5.57
    """
    bs = BlackScholes(time_to_maturity=1, strike=100, current_price=100, volatility=0.2, interest_rate=0.05)
    _, put_price = bs.calculate_prices()
    
    assert abs(put_price - 5.5735) < 0.01

def test_greeks_calculation():
    """
    Ensures that Greeks are being returned and have the correct structure.
    """
    bs = BlackScholes(time_to_maturity=1, strike=100, current_price=100, volatility=0.2, interest_rate=0.05)
    greeks = bs.calculate_greeks()
    
    # Check if the dictionary has the right keys
    assert "call" in greeks
    assert "put" in greeks
    assert "delta" in greeks["call"]
    
    # Check a specific value (Call Delta should be roughly 0.63 for these inputs)
    assert abs(greeks["call"]["delta"] - 0.6368) < 0.01