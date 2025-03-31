
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Weekly Trading Dashboard", layout="wide")

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

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Live Market Header",
    "🗓️ Economic Calendar",
    "📊 Weekly Index Recap",
    "📋 Watchlist & Notes",
    "💸 Fund Flows & Sentiment"
])

# Tab 1: Live Market Header
with tab1:
    st.header("📈 Live Market Prices")

    symbols = list(tickers.values())
    df = yf.download(symbols, period="2d", interval="1d", progress=False)["Adj Close"]

    if df.empty or len(df) < 2:
        st.warning("Live data not available or incomplete. Please try again later.")
    else:
        latest = df.iloc[-1]
        previous = df.iloc[-2]

        records = []
        for name, symbol in tickers.items():
            try:
                last = latest[symbol]
                prev = previous[symbol]
                pct_change = ((last - prev) / prev) * 100
                records.append((name, round(last, 2), round(pct_change, 2)))
            except KeyError:
                records.append((name, "N/A", "N/A"))

        live_df = pd.DataFrame(records, columns=["Index", "Last Price", "% Change"]).set_index("Index")
        st.dataframe(live_df)

# Tab 2: Economic Calendar
with tab2:
    st.header("🗓️ Economic Calendar (Week Ahead)")
    st.markdown("*(Mock data shown below — replace with API or Google Sheet feed)*")
    econ_data = {
        "Date": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Event": [
            "US ISM Manufacturing PMI",
            "China Caixin Services PMI",
            "Eurozone CPI",
            "US Initial Jobless Claims",
            "US Non-Farm Payrolls"
        ]
    }
    econ_df = pd.DataFrame(econ_data)
    st.table(econ_df)

# Tab 3: Weekly Index Recap
with tab3:
    st.header("📊 Friday-to-Friday Index Recap")
    st.markdown("*(Sample data — replace with historical fetch or upload)*")
    index_perf = {
        "Index": ["S&P 500", "NASDAQ", "HSI", "CSI 300", "CSI 500", "HSTECH"],
        "Last Week": ["+1.5%", "+2.2%", "-0.8%", "+0.3%", "+0.5%", "-1.1%"]
    }
    perf_df = pd.DataFrame(index_perf).set_index("Index")
    st.dataframe(perf_df)

# Tab 4: Watchlist & Strategy Notes
with tab4:
    st.header("📋 Watchlist & Strategy Notes")
    st.markdown("*(Editable Google Sheet support coming soon)*")

    st.subheader("Watchlist")
    watchlist = ["AAPL", "NVDA", "TSLA", "BABA", "KWEB"]
    wl_data = yf.download(watchlist, period="2d", interval="1d", progress=False)["Adj Close"]
    if len(wl_data) >= 2:
        wl_latest = wl_data.iloc[-1]
        wl_prev = wl_data.iloc[-2]
        wl_change = ((wl_latest - wl_prev) / wl_prev * 100).round(2)
        watch_df = pd.DataFrame({
            "Ticker": watchlist,
            "Last Price": [wl_latest.get(t, "N/A") for t in watchlist],
            "% Change": [wl_change.get(t, "N/A") for t in watchlist]
        })
        st.dataframe(watch_df.set_index("Ticker"))

    st.subheader("Notes")
    notes = st.text_area("Write your trading thoughts, strategy, or risk notes for the week:", height=200)

# Tab 5: Fund Flows & Sentiment
with tab5:
    st.header("💸 Fund Flows & Market Sentiment")
    st.markdown("*(Static sample — replace with API or Sheet integration)*")
    st.subheader("ETF Flows (Last Week)")
    flow_data = {
        "ETF": ["SPY", "QQQ", "ARKK", "KWEB", "FXI"],
        "Flow ($M)": [1200, 850, -300, 150, -220]
    }
    st.table(pd.DataFrame(flow_data))

    st.subheader("Sentiment Indicators")
    sentiment = {
        "Indicator": ["VIX", "Fear & Greed Index", "Put/Call Ratio"],
        "Value": ["13.5", "65 (Greed)", "0.88"]
    }
    st.table(pd.DataFrame(sentiment))
