import streamlit as st
import yfinance as yf
import numpy as np

@st.cache_data(ttl=300)
def get_historical_vol(ticker_symbol, period):
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