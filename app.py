import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from src.portfolio.returns import (
    calculate_returns,
    calculate_portfolio_returns,
    calculate_cumulative_returns,
)
from src.portfolio.metrics import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    historical_var,
)
from src.portfolio.risk import calculate_drawdown, rolling_volatility
from src.portfolio.risk_contribution import calculate_risk_contribution
from src.portfolio.benchmark import calculate_excess_returns, calculate_rolling_beta

from src.dashboard.sidebar import render_sidebar
from src.dashboard.overview import render_overview_tab
from src.dashboard.risk import render_risk_tab
from src.dashboard.benchmark import render_benchmark_tab
from src.dashboard.optimization import render_optimization_tab
from src.dashboard.simulation import render_simulation_tab
from src.dashboard.commentary import render_commentary_tab
from src.dashboard.data import render_data_tab


st.set_page_config(
    page_title="Quant Risk Dashboard",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_price_data(tickers, start_date, end_date):
    return yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        threads=False,
    )["Close"]


def calculate_portfolio_analytics(prices, weights):
    asset_returns = calculate_returns(prices)
    portfolio_returns = calculate_portfolio_returns(asset_returns, weights)
    cumulative_returns = calculate_cumulative_returns(portfolio_returns)
    drawdown = calculate_drawdown(cumulative_returns)
    rolling_vol = rolling_volatility(portfolio_returns)

    return asset_returns, portfolio_returns, cumulative_returns, drawdown, rolling_vol


def calculate_metrics(portfolio_returns, cumulative_returns):
    return {
        "Annual Return": annualized_return(portfolio_returns),
        "Annual Volatility": annualized_volatility(portfolio_returns),
        "Sharpe Ratio": sharpe_ratio(portfolio_returns),
        "Max Drawdown": max_drawdown(cumulative_returns),
        "Daily VaR 95%": historical_var(portfolio_returns),
    }


def build_asset_metrics(asset_returns, weights):
    asset_metrics = pd.DataFrame(
        {
            "Weight": weights,
            "Annual Return": asset_returns.mean() * 252,
            "Annual Volatility": asset_returns.std() * np.sqrt(252),
        },
        index=asset_returns.columns,
    )

    risk_contribution = calculate_risk_contribution(asset_returns, weights)

    return asset_metrics.join(
        risk_contribution[
            [
                "Risk Contribution",
                "Percentage Risk Contribution",
            ]
        ]
    )


def calculate_benchmark_analytics(
    benchmark_ticker,
    start_date,
    end_date,
    portfolio_returns,
):
    benchmark_prices = load_price_data([benchmark_ticker], start_date, end_date)

    if isinstance(benchmark_prices, pd.DataFrame):
        benchmark_prices = benchmark_prices.iloc[:, 0]

    benchmark_returns = calculate_returns(benchmark_prices)
    benchmark_cumulative = calculate_cumulative_returns(benchmark_returns)

    excess_returns = calculate_excess_returns(
        portfolio_returns,
        benchmark_returns,
    )

    rolling_beta = calculate_rolling_beta(
        portfolio_returns,
        benchmark_returns,
        window=63,
    )

    tracking_error = excess_returns.std() * np.sqrt(252)

    if tracking_error == 0:
        information_ratio = np.nan
    else:
        information_ratio = excess_returns.mean() * 252 / tracking_error

    return {
        "benchmark_returns": benchmark_returns,
        "benchmark_cumulative": benchmark_cumulative,
        "excess_returns": excess_returns,
        "rolling_beta": rolling_beta,
        "tracking_error": tracking_error,
        "information_ratio": information_ratio,
    }


st.title("Quant Risk Dashboard")
st.write(
    "Portfolio analytics, risk metrics, optimization, benchmark analysis, "
    "and AI-style commentary."
)

tickers, shares, benchmark_ticker, start_date, end_date = render_sidebar()

prices = load_price_data(tickers, start_date, end_date)

latest_prices = prices.ffill().iloc[-1]

position_values = pd.Series(
    {
        ticker: shares[ticker] * latest_prices[ticker]
        for ticker in tickers
    }
)

portfolio_value = position_values.sum()

if portfolio_value <= 0:
    st.error("Portfolio value must be greater than zero.")
    st.stop()

weights = (position_values / portfolio_value).values

if prices.empty:
    st.error("No price data found. Check tickers or date range.")
    st.stop()

asset_returns, portfolio_returns, cumulative_returns, drawdown, rolling_vol = (
    calculate_portfolio_analytics(prices, weights)
)

metrics = calculate_metrics(portfolio_returns, cumulative_returns)
asset_metrics = build_asset_metrics(asset_returns, weights)

benchmark_analytics = calculate_benchmark_analytics(
    benchmark_ticker=benchmark_ticker,
    start_date=start_date,
    end_date=end_date,
    portfolio_returns=portfolio_returns,
)

(
    overview_tab,
    risk_tab,
    benchmark_tab,
    optimization_tab,
    simulation_tab,
    commentary_tab,
    data_tab,
) = st.tabs(
    [
        "Overview",
        "Risk Analysis",
        "Benchmark",
        "Optimization",
        "Simulation",
        "Commentary",
        "Data",
    ]
)

with overview_tab:
    render_overview_tab(
        metrics=metrics,
        cumulative_returns=cumulative_returns,
        tickers=tickers,
        weights=weights,
        asset_metrics=asset_metrics,
    )

with risk_tab:
    render_risk_tab(
        drawdown=drawdown,
        rolling_vol=rolling_vol,
        portfolio_returns=portfolio_returns,
        asset_returns=asset_returns,
    )

with benchmark_tab:
    render_benchmark_tab(
        benchmark_ticker=benchmark_ticker,
        cumulative_returns=cumulative_returns,
        benchmark_cumulative=benchmark_analytics["benchmark_cumulative"],
        rolling_beta=benchmark_analytics["rolling_beta"],
        tracking_error=benchmark_analytics["tracking_error"],
        information_ratio=benchmark_analytics["information_ratio"],
    )

with optimization_tab:
    render_optimization_tab(prices=prices)

with simulation_tab:
    render_simulation_tab(asset_returns=asset_returns)

with commentary_tab:
    render_commentary_tab(
        metrics=metrics,
        asset_metrics=asset_metrics,
        benchmark_ticker=benchmark_ticker,
        tracking_error=benchmark_analytics["tracking_error"],
        information_ratio=benchmark_analytics["information_ratio"],
    )

with data_tab:
    render_data_tab(
        prices=prices,
        asset_returns=asset_returns,
    )