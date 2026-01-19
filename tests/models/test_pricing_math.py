import pytest
import numpy as np
from models.bs_model import BlackScholes
from models.binomial import BinomialModel

# Standard Textbook Case
# S=100, K=100, T=1, r=5%, sigma=20%
# Call Price should be roughly $10.45
PARAMS = {
    "T": 1.0,    # Time to Maturity
    "K": 100.0,  # Strike
    "S": 100.0,  # Spot (Current Price)
    "sigma": 0.2,# Volatility
    "r": 0.05    # Risk Free Rate
}

def test_black_scholes_call_price():
    # Passing arguments positionally to avoid name mismatches
    # Order: Time, Strike, Spot, Volatility, Rate
    bs = BlackScholes(
        PARAMS["T"], 
        PARAMS["K"], 
        PARAMS["S"], 
        PARAMS["sigma"], 
        PARAMS["r"]
    )
    call, put = bs.calculate_prices()
    
    # Check within 1 cent accuracy
    assert 10.44 <= call <= 10.46

def test_black_scholes_put_call_parity():
    """Call - Put should equal S - K * exp(-rT)"""
    bs = BlackScholes(
        PARAMS["T"], 
        PARAMS["K"], 
        PARAMS["S"], 
        PARAMS["sigma"], 
        PARAMS["r"]
    )
    call, put = bs.calculate_prices()
    
    lhs = call - put
    rhs = PARAMS["S"] - PARAMS["K"] * np.exp(-PARAMS["r"] * PARAMS["T"])
    
    assert np.isclose(lhs, rhs, atol=0.01)

def test_binomial_convergence():
    """Binomial model should approach Black-Scholes as steps increase."""
    # 1. Calculate BS Price
    bs = BlackScholes(
        PARAMS["T"], 
        PARAMS["K"], 
        PARAMS["S"], 
        PARAMS["sigma"], 
        PARAMS["r"]
    )
    bs_call, _ = bs.calculate_prices()
    
    # 2. Calculate Binomial Price (using 100 steps)
    # Note: BinomialModel likely takes steps as the last argument or a specific kwarg
    binom = BinomialModel(
        PARAMS["T"], 
        PARAMS["K"], 
        PARAMS["S"], 
        PARAMS["sigma"], 
        PARAMS["r"],
        steps=100
    )
    bin_call, _ = binom.calculate_prices()
    
    # Should be within roughly 20 cents of BS
    diff = abs(bs_call - bin_call)
    assert diff < 0.20