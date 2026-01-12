import pytest
from models.binomial import BinomialModel
from models.bs_model import BlackScholes

def test_binomial_vs_black_scholes():
    # Setup parameters
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    
    # 1. Calculate Black-Scholes Price (The "True" theoretical price for European)
    bs = BlackScholes(T, K, S, sigma, r)
    bs_call, _ = bs.calculate_prices()
    
    # 2. Calculate Binomial Price (European style)
    # We use 500 steps for higher accuracy in comparison
    bi = BinomialModel(S, K, T, r, sigma, steps=500)
    bi_call = bi.calculate_price(option_type='call', american=False)
    
    # 3. Assert they are close (within 10 cents)
    assert abs(bs_call - bi_call) < 0.1, f"Binomial {bi_call} too far from BS {bs_call}"

def test_american_vs_european_put():
    # Deep In-The-Money Put where early exercise is valuable
    # S=80, K=100 (Intrinsic value = 20)
    S, K, T, r, sigma = 80, 100, 1, 0.05, 0.2
    
    bi = BinomialModel(S, K, T, r, sigma, steps=100)
    
    euro_put = bi.calculate_price(option_type='put', american=False)
    amer_put = bi.calculate_price(option_type='put', american=True)
    
    # American put should be worth more (or equal) because of early exercise right
    assert amer_put >= euro_put
    
    # Specifically here, since it's deep ITM, American should be > European
    # (Because waiting loses money due to time value of money on the strike price)
    assert amer_put > euro_put