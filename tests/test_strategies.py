import pytest
import numpy as np
from models.strategies import calculate_payoff

def test_long_call_payoff():
    # Buy Call: Strike 100, Premium 5. 
    # If Spot is 110, Value is 10. Profit should be 10 - 5 = 5.
    profit = calculate_payoff(spot_prices=110, strike_price=100, premium=5, option_type="Call", position_type="Long")
    assert profit == 5.0

def test_short_put_payoff():
    # Sell Put: Strike 100, Premium 5.
    # If Spot is 90, Intrinsic is 10. Loss is 5 (premium) - 10 (liability) = -5.
    profit = calculate_payoff(spot_prices=90, strike_price=100, premium=5, option_type="Put", position_type="Short")
    assert profit == -5.0

def test_vectorized_payoff():
    # Test passing an array of prices (NumPy efficiency check)
    spots = np.array([90, 100, 110])
    # Long Call 100, Premium 2
    # 90 -> 0 - 2 = -2
    # 100 -> 0 - 2 = -2
    # 110 -> 10 - 2 = 8
    expected = np.array([-2.0, -2.0, 8.0])
    result = calculate_payoff(spots, 100, 2, "Call", "Long")
    np.testing.assert_array_equal(result, expected)