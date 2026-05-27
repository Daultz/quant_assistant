import pandas as pd
import streamlit as st
from datetime import date

from src.data.ticker_search import search_tickers


DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "SPY"]


def initialize_portfolio_state():
    if "selected_tickers" not in st.session_state:
        st.session_state["selected_tickers"] = DEFAULT_TICKERS.copy()

    if "shares" not in st.session_state:
        st.session_state["shares"] = {
            ticker: 10.0 for ticker in st.session_state["selected_tickers"]
        }


def render_sidebar():
    initialize_portfolio_state()

    st.sidebar.header("Portfolio Inputs")

    search_query = st.sidebar.text_input(
        "Search ticker",
        placeholder="Type company name or ticker, e.g. Apple or AAPL",
    )

    search_results = search_tickers(search_query)

    if search_results:
        label_to_symbol = {
            item["label"]: item["symbol"]
            for item in search_results
        }

        selected_label = st.sidebar.selectbox(
            "Search results",
            list(label_to_symbol.keys()),
        )

        if st.sidebar.button("Add selected ticker"):
            selected_symbol = label_to_symbol[selected_label]

            if selected_symbol not in st.session_state["selected_tickers"]:
                st.session_state["selected_tickers"].append(selected_symbol)
                st.session_state["shares"][selected_symbol] = 10.0
                st.sidebar.success(f"Added {selected_symbol}")
            else:
                st.sidebar.info(f"{selected_symbol} is already in the portfolio.")

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            background: transparent;
            border: none;
            padding: 0;
            font-size: 18px;
        }

        div[data-testid="stButton"] button:hover {
            background: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.sidebar.subheader("Selected Holdings")

    tickers_to_remove = []

    for ticker in st.session_state["selected_tickers"]:
        col1, col2 = st.sidebar.columns([5, 1])

        with col1:
            st.session_state["shares"][ticker] = st.number_input(
                label=ticker,
                min_value=0.0,
                value=float(st.session_state["shares"].get(ticker, 10.0)),
                step=1.0,
                key=f"shares_{ticker}",
            )

        with col2:
            st.markdown("##### ")

            if st.button(
                "🗑️",
                key=f"remove_{ticker}",
                help=f"Remove {ticker}",
            ):
                tickers_to_remove.append(ticker)

    for ticker in tickers_to_remove:
        st.session_state["selected_tickers"].remove(ticker)
        st.session_state["shares"].pop(ticker, None)
        st.rerun()

    benchmark_ticker = st.sidebar.text_input(
        "Benchmark",
        value="SPY",
    ).upper()

    start_date = st.sidebar.date_input(
        "Start Date",
        value=pd.to_datetime("2020-01-01"),
    )

    use_latest_end_date = st.sidebar.checkbox(
        "Use latest available end date",
        value=True,
    )

    if use_latest_end_date:
        end_date = date.today()
        st.sidebar.caption(f"End Date: {end_date} latest")
    else:
        end_date = st.sidebar.date_input(
            "End Date",
            value=date.today(),
        )

    tickers = st.session_state["selected_tickers"]
    shares = st.session_state["shares"]

    if not tickers:
        st.sidebar.error("Please add at least one ticker.")
        st.stop()

    if sum(shares[ticker] for ticker in tickers) <= 0:
        st.sidebar.error("Please enter at least one positive share amount.")
        st.stop()

    if start_date >= end_date:
        st.sidebar.error("Start date must be before end date.")
        st.stop()

    return tickers, shares, benchmark_ticker, start_date, end_date