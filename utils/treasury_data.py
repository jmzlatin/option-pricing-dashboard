import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def get_treasury_rate(ticker_symbol):
    """Fetches the latest yield for a treasury ticker."""
    try:
        data = yf.Ticker(ticker_symbol).history(period="1d")
        if data.empty:
            return None
        return data['Close'].iloc[-1]
    except:
        return None