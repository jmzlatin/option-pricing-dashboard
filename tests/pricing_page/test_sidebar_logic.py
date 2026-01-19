import pytest
from datetime import date
from modules.pricing_page.sidebar.core_logic import (
    calculate_time_to_maturity,
    sanitize_ticker,
    select_treasury_ticker,
    select_volatility_period
)

# --- Ticker Tests ---
def test_sanitize_ticker_basic():
    assert sanitize_ticker("aapl") == "AAPL"

def test_sanitize_ticker_whitespace():
    assert sanitize_ticker("  msft  ") == "MSFT"

def test_sanitize_ticker_empty():
    assert sanitize_ticker("") == ""

# --- Maturity Tests ---
def test_maturity_calculation():
    today = date(2025, 1, 1)
    expiry = date(2026, 1, 1) # 365 days later
    assert calculate_time_to_maturity(today, expiry) == 1.0

def test_maturity_past_date():
    today = date(2025, 1, 1)
    expiry = date(2024, 1, 1) # Past
    assert calculate_time_to_maturity(today, expiry) == 0.0

# --- Treasury Selector Logic (UPDATED) ---

def test_treasury_selector_short_term():
    # 2 months (0.16 years) -> 13-Week Bill
    ticker, name = select_treasury_ticker(0.16)
    assert ticker == "^IRX"
    assert "13-Week" in name

def test_treasury_selector_one_year_gap():
    # 1.0 years -> Should default to IRX but warn about 1-Year
    # Ideally, this should trigger a "Check 1-Year Rate" label
    ticker, name = select_treasury_ticker(1.0)
    assert ticker == "^IRX"
    assert "Check 1-Year" in name

def test_treasury_selector_medium_term():
    # 3 years -> 5-Year Note
    ticker, name = select_treasury_ticker(3.0)
    assert ticker == "^FVX"
    assert "5-Year" in name

def test_treasury_selector_long_term():
    # 25 years -> 30-Year Bond
    ticker, name = select_treasury_ticker(25.0)
    assert ticker == "^TYX"
    assert "30-Year" in name

# --- Volatility Window Logic ---
def test_volatility_window_very_short():
    assert select_volatility_period(0.1) == "3mo"

def test_volatility_window_standard():
    assert select_volatility_period(0.8) == "1y"

def test_volatility_window_long():
    assert select_volatility_period(6.0) == "10y"