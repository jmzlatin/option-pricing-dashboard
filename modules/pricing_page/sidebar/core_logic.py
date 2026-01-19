from datetime import date

def calculate_time_to_maturity(today: date, expiry: date) -> float:
    """Calculates years to maturity. Returns 0.0 if expired."""
    delta = (expiry - today).days
    return max(0.0, delta / 365.0)

def sanitize_ticker(ticker_input: str) -> str:
    """Ensures ticker is uppercase and stripped of whitespace."""
    if not ticker_input:
        return ""
    return ticker_input.strip().upper()

def select_treasury_ticker(years_to_maturity: float) -> tuple[str, str]:
    """
    Decides which Treasury Bond to use as a proxy for Risk-Free Rate.
    Returns: (Ticker Symbol, Human Readable Name)
    """
    if years_to_maturity <= 2.0:
        return "^IRX", "13-Week T-Bill"
    elif years_to_maturity <= 5.0:
        return "^FVX", "5-Year T-Note"
    elif years_to_maturity <= 10.0:
        return "^TNX", "10-Year T-Note"
    else:
        return "^TYX", "30-Year T-Bond"

def select_volatility_period(years_to_maturity: float) -> str:
    """
    Matches the historical volatility lookback window to the option maturity.
    """
    if years_to_maturity < 0.25:  # Less than 3 months
        return "3mo"
    elif years_to_maturity < 0.5: # Less than 6 months
        return "6mo"
    elif years_to_maturity < 1.0: # Less than 1 year
        return "1y"
    elif years_to_maturity < 2.0: # Less than 2 years
        return "2y"
    elif years_to_maturity < 5.0: # Less than 5 years
        return "5y"
    else:
        return "10y"
