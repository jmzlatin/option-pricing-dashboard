import pytest
from models.binomial import BinomialModel
from models.bs_model import BlackScholes

def test_binomial_convergence_to_bs():
    """
    For a European Call (non-dividend paying), the American Binomial price 
    should be very close to the Black-Scholes European price.
    """
    # Parameters
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
    
    # 1. Black-Scholes Price (True European)
    # Order: T, K, S, sigma, r
    bs = BlackScholes(T, K, S, sigma, r)
    bs_call, _ = bs.calculate_prices()
    
    # 2. Binomial Price (American)
    # Order: T, K, S, sigma, r
    # We use 500 steps for better precision
    bi = BinomialModel(T, K, S, sigma, r, steps=500)
    bi_call, _ = bi.calculate_prices()
    
    # They should be close (within $0.10)
    assert abs(bi_call - bs_call) < 0.1

def test_american_put_early_exercise():
    """
    For a deep In-The-Money Put, the American Option (Binomial) 
    should be worth MORE than the European Option (Black-Scholes)
    because of the Early Exercise premium.
    """
    # Deep ITM Put: Stock=80, Strike=100
    S, K, T, r, sigma = 80, 100, 1.0, 0.1, 0.2
    
    # 1. European Put (BS)
    bs = BlackScholes(T, K, S, sigma, r)
    _, bs_put = bs.calculate_prices()
    
    # 2. American Put (Binomial)
    bi = BinomialModel(T, K, S, sigma, r, steps=100)
    _, bi_put = bi.calculate_prices()
    
    # American Put must be strictly greater than European Put
    assert bi_put > bs_put