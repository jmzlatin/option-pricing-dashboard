import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

def get_historical_vol(ticker_symbol, period="1y"):
    """Calculates annualized historical volatility based on log returns."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist_data = ticker.history(period=period)
        if len(hist_data) > 10:
            hist_data['Log Returns'] = np.log(hist_data['Close'] / hist_data['Close'].shift(1))
            hist_vol = hist_data['Log Returns'].std() * np.sqrt(252)
            return hist_vol
        return None
    except:
        return None

def get_implied_vol(ticker_symbol, target_strike=None):
    """
    Fetches Implied Volatility (IV) for a specific strike.
    If target_strike is None, defaults to the At-The-Money (ATM) strike.
    """
    try:
        tk = yf.Ticker(ticker_symbol)
        
        # 1. Get Stock Price if strike not provided
        if target_strike is None:
            hist = tk.history(period='1d')
            if hist.empty: return None
            target_strike = hist['Close'].iloc[-1]

        # 2. Find an expiration ~30 days out
        exps = tk.options
        if not exps: return None
        
        target_date = datetime.now() + timedelta(days=30)
        chosen_exp = min(exps, key=lambda d: abs(datetime.strptime(d, "%Y-%m-%d") - target_date))
        
        # 3. Get Option Chain
        opt = tk.option_chain(chosen_exp)
        calls = opt.calls
        
        # 4. Find the row closest to our Target Strike
        # This is crucial: We find the IV for the *specific* strike the user wants
        calls['abs_diff'] = abs(calls['strike'] - target_strike)
        target_row = calls.loc[calls['abs_diff'].idxmin()]
        
        return target_row['impliedVolatility']
        
    except Exception as e:
        print(f"Error fetching IV: {e}")
        return None