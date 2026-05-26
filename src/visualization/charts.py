import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_cumulative_returns(cumulative_returns: pd.Series):
    fig = px.line(
        cumulative_returns,
        title="Portfolio Cumulative Returns",
        labels={"value": "Growth of £1", "index": "Date"},
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_drawdown(drawdown: pd.Series):
    fig = px.line(
        drawdown,
        title="Portfolio Drawdown",
        labels={"value": "Drawdown", "index": "Date"},
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_returns_distribution(returns: pd.Series):
    fig = px.histogram(
        returns,
        nbins=60,
        title="Portfolio Daily Returns Distribution",
        labels={"value": "Daily Return"},
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_correlation_heatmap(asset_returns: pd.DataFrame):
    corr = asset_returns.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(title="Asset Correlation Matrix")
    return fig


def plot_rolling_volatility(rolling_vol: pd.Series):
    fig = px.line(
        rolling_vol,
        title="Rolling Annualized Volatility",
        labels={"value": "Volatility", "index": "Date"},
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_portfolio_allocation(tickers, weights):
    fig = px.pie(
        names=tickers,
        values=weights,
        title="Portfolio Allocation",
        hole=0.4,
    )
    return fig


def plot_efficient_frontier(simulation_results):
    fig = px.scatter(
        simulation_results,
        x="Volatility",
        y="Return",
        color="Sharpe Ratio",
        title="Monte Carlo Portfolio Simulation",
        hover_data=["Sharpe Ratio"],
    )

    return fig


def plot_benchmark_comparison(portfolio_cumulative, benchmark_cumulative):
    comparison = pd.concat(
        [portfolio_cumulative, benchmark_cumulative],
        axis=1,
        join="inner",
    )

    comparison.columns = ["Portfolio", "Benchmark"]

    fig = px.line(
        comparison,
        title="Portfolio vs Benchmark",
        labels={"value": "Growth of £1", "index": "Date"},
    )

    return fig


def plot_rolling_beta(rolling_beta):
    fig = px.line(
        rolling_beta,
        title="Rolling Beta vs Benchmark",
        labels={"value": "Beta", "index": "Date"},
    )
    fig.update_layout(showlegend=False)
    return fig