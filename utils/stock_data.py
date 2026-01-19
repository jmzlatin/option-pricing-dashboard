import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def get_stock_price(ticker_symbol):
    """Fetches the latest closing price for a ticker."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return None
        return history['Close'].iloc[-1]
    except:
        return None