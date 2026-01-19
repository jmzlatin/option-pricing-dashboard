import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from utils.stock_data import get_stock_price
from utils.treasury_data import get_treasury_rate
from utils.volatility_data import get_historical_vol

# --- Test Stock Data ---
@patch('yfinance.Ticker')
def test_get_stock_price_success(mock_ticker):
    # Setup the fake data
    mock_hist = pd.DataFrame({'Close': [150.0, 155.0]})
    mock_instance = mock_ticker.return_value
    mock_instance.history.return_value = mock_hist
    
    price = get_stock_price("AAPL")
    assert price == 155.0

@patch('yfinance.Ticker')
def test_get_stock_price_failure(mock_ticker):
    # Simulate empty data (invalid ticker)
    mock_instance = mock_ticker.return_value
    mock_instance.history.return_value = pd.DataFrame()
    
    price = get_stock_price("INVALID")
    assert price is None

# --- Test Volatility Calc ---
@patch('yfinance.Ticker')
def test_get_historical_vol_calculation(mock_ticker):
    # Create a synthetic price series with known movement
    # 20 days of data
    prices = [100 * (1.01)**i for i in range(20)] 
    mock_hist = pd.DataFrame({'Close': prices})
    
    mock_instance = mock_ticker.return_value
    mock_instance.history.return_value = mock_hist
    
    vol = get_historical_vol("TEST", "1mo")
    
    # Volatility should be a float, not None
    assert vol is not None
    assert isinstance(vol, float)
    assert vol > 0
