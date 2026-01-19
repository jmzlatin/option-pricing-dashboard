import yfinance as yf

def get_risk_free_rate():
    """
    Fetches the 13-week Treasury Bill rate (^IRX) to use as the risk-free rate.
    Returns a float (e.g., 0.045 for 4.5%).
    Defaults to 4.0% if the fetch fails.
    """
    try:
        # ^IRX is the 13-week Treasury Bill Index
        ticker = yf.Ticker("^IRX")
        
        # We need the most recent close
        # "fast_info" is often more reliable/faster than .history() for indices
        rate = ticker.fast_info.get('last_price')
        
        if rate is None:
            # Fallback to history if fast_info fails
            hist = ticker.history(period="5d")
            if not hist.empty:
                rate = hist['Close'].iloc[-1]

        if rate:
            return rate / 100.0  # Convert 4.5 -> 0.045
            
    except Exception as e:
        print(f"Rate fetch error: {e}")
        
    return 0.04  # Safe default (4.0%)