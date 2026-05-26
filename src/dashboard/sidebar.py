import numpy as np
import pandas as pd
import streamlit as st


PORTFOLIO_PRESETS = {
    "Custom": {
        "tickers": "AAPL, MSFT, GOOGL, AMZN, SPY",
        "weights": "0.2, 0.2, 0.2, 0.2, 0.2",
    },
    "US Mega Cap Tech": {
        "tickers": "AAPL, MSFT, GOOGL, AMZN, NVDA",
        "weights": "0.2, 0.2, 0.2, 0.2, 0.2",
    },
    "Core ETFs": {
        "tickers": "SPY, QQQ, IWM, EFA, EEM",
        "weights": "0.4, 0.25, 0.15, 0.1, 0.1",
    },
    "Defensive Portfolio": {
        "tickers": "SPY, TLT, GLD, XLU, XLV",
        "weights": "0.35, 0.25, 0.15, 0.1, 0.15",
    },
}


def render_sidebar():
    st.sidebar.header("Portfolio Inputs")

    preset = st.sidebar.selectbox(
        "Portfolio Preset",
        list(PORTFOLIO_PRESETS.keys()),
    )

    default_tickers = PORTFOLIO_PRESETS[preset]["tickers"]
    default_weights = PORTFOLIO_PRESETS[preset]["weights"]

    tickers_input = st.sidebar.text_input(
        "Tickers",
        value=default_tickers,
    )

    use_equal_weights = st.sidebar.checkbox(
        "Use equal weights",
        value=False,
    )

    if use_equal_weights:
        weights_input = ""
    else:
        weights_input = st.sidebar.text_input(
            "Weights",
            value=default_weights,
        )

    benchmark_ticker = st.sidebar.text_input(
        "Benchmark",
        value="SPY",
    )

    start_date = st.sidebar.date_input(
        "Start Date",
        value=pd.to_datetime("2020-01-01"),
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=pd.to_datetime("2025-01-01"),
    )

    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]

    if use_equal_weights:
        weights = np.repeat(1 / len(tickers), len(tickers))
    else:
        weights = np.array([float(w.strip()) for w in weights_input.split(",") if w.strip()])

    if len(tickers) != len(weights):
        st.sidebar.error("Number of tickers must match number of weights.")
        st.stop()

    if not np.isclose(weights.sum(), 1.0):
        st.sidebar.error(f"Weights must sum to 1. Current sum: {weights.sum():.2f}")
        st.stop()

    if start_date >= end_date:
        st.sidebar.error("Start date must be before end date.")
        st.stop()

    return tickers, weights, benchmark_ticker, start_date, end_date