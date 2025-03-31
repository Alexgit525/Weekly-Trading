
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Weekly Market Dashboard", layout="wide")

st.title("📊 Weekly Stock Market Dashboard")
st.markdown("Live market header for major US, HK, and China indices.")

# Define ticker symbols
tickers = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC",
    "Hang Seng Index": "^HSI",
    "HSCEI": "^HSCE",
    "HSTECH": "^HSTECH",
    "CSI 300": "000300.SS",
    "CSI 500": "000905.SS",
    "CSI 1000": "000852.SS"
}

# Download latest prices
data = yf.download(list(tickers.values()), period="2d", interval="1d", progress=False)["Adj Close"]

if len(data) < 2:
    st.error("Not enough data returned. Try again later.")
else:
    latest_prices = data.iloc[-1]
    prev_prices = data.iloc[-2]
    changes = ((latest_prices - prev_prices) / prev_prices) * 100

    df = pd.DataFrame({
        "Index": list(tickers.keys()),
        "Last Price": [round(latest_prices[tickers[name]], 2) for name in tickers],
        "% Change": [round(changes[tickers[name]], 2) for name in tickers]
    })

    st.dataframe(df.set_index("Index"), height=400)
