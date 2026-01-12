import pytest
import numpy as np
import sys
import os

# Add the parent directory to sys.path so we can import bs_model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs_model import BlackScholes

def test_put_call_parity():
    # Setup known parameters
    S = 100     # Spot Price
    K = 100     # Strike Price
    T = 1       # Time (1 year)
    sigma = 0.2 # Volatility
    r = 0.05    # Risk-free rate

    # Initialize model
    model = BlackScholes(time_to_maturity=T, strike=K, current_price=S, volatility=sigma, interest_rate=r)
    call_price, put_price = model.calculate_prices()

    # Verify Put-Call Parity: C - P = S - K * e^(-rT)
    left_side = call_price - put_price
    right_side = S - K * np.exp(-r * T)

    # Assert equality (with a tiny tolerance for floating point math)
    assert np.isclose(left_side, right_side, atol=1e-4)

def test_call_price_positive():
    model = BlackScholes(1, 100, 100, 0.2, 0.05)
    c, p = model.calculate_prices()
    assert c > 0
    assert p > 0