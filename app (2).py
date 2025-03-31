
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
    df = yf.download(symbols, period="2d", interval="1d", progress=False)

    if "Adj Close" not in df or df.get("Adj Close").empty:
        st.warning("Live data not available or incomplete. Please try again later.")
    else:
        adj_close = df.get("Adj Close")
        if len(adj_close) < 2:
            st.warning("Not enough data to calculate changes.")
        else:
            latest = adj_close.iloc[-1]
            previous = adj_close.iloc[-2]

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
    wl_df = yf.download(watchlist, period="2d", interval="1d", progress=False)
    adj_close = wl_df.get("Adj Close")

    if adj_close is None or len(adj_close) < 2:
        st.warning("Watchlist data not available.")
    else:
        latest = adj_close.iloc[-1]
        previous = adj_close.iloc[-2]
        wl_data = []

        for ticker in watchlist:
            try:
                last = latest[ticker]
                prev = previous[ticker]
                pct_change = ((last - prev) / prev) * 100
                wl_data.append((ticker, round(last, 2), round(pct_change, 2)))
            except KeyError:
                wl_data.append((ticker, "N/A", "N/A"))

        watch_df = pd.DataFrame(wl_data, columns=["Ticker", "Last Price", "% Change"]).set_index("Ticker")
        st.dataframe(watch_df)

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
