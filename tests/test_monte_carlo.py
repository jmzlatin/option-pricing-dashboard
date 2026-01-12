import pytest
import numpy as np
from models.monte_carlo import MonteCarloPricing

def test_monte_carlo_shape():
    """
    Smoke Test: Does it generate the right number of paths and steps?
    """
    mc = MonteCarloPricing(S=100, K=100, T=1, r=0.05, sigma=0.2, simulations=100, steps=10)
    paths = mc.simulate_paths()
    
    # Shape should be (simulations, steps + 1) -> (100, 11) because of T=0
    assert paths.shape == (100, 11)
    
    # All paths should start at S0
    assert np.all(paths[:, 0] == 100)

def test_monte_carlo_zero_volatility():
    """
    Math Test: If volatility is 0, the stock should grow exactly by the risk-free rate.
    No randomness allowed.
    Formula: S_T = S_0 * e^(rT)
    """
    mc = MonteCarloPricing(S=100, K=100, T=1, r=0.05, sigma=0.0, simulations=10, steps=5)
    paths = mc.simulate_paths()
    terminal_prices = paths[:, -1]
    
    expected_price = 100 * np.exp(0.05 * 1)
    
    # Check if all 10 paths ended at exactly the expected price
    np.testing.assert_allclose(terminal_prices, expected_price, rtol=1e-5)