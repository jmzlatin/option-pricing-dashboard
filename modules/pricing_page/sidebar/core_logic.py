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
    # < 4 Months: Use 13-Week T-Bill
    if years_to_maturity <= 0.33:
        return "^IRX", "13-Week T-Bill"
    
    # 4 Months - 2 Years: No good Yahoo ticker exists for 1-Year.
    # We return "^IRX" as a fallback, but the UI should warn the user.
    # Ideally, they should manually input the "1-Year Constant Maturity" rate.
    elif years_to_maturity <= 2.0:
        return "^IRX", "13-Week T-Bill (Check 1-Year Rate!)"
    
    # 2 - 7 Years: Use 5-Year T-Note
    elif years_to_maturity <= 7.0:
        return "^FVX", "5-Year T-Note"
    
    # 7 - 20 Years: Use 10-Year T-Note
    elif years_to_maturity <= 20.0:
        return "^TNX", "10-Year T-Note"
    
    # > 20 Years: Use 30-Year T-Bond
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