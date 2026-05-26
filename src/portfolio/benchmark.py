import pandas as pd


def calculate_excess_returns(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> pd.Series:
    aligned = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    aligned.columns = ["Portfolio", "Benchmark"]

    return aligned["Portfolio"] - aligned["Benchmark"]


def calculate_rolling_beta(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 63,
) -> pd.Series:
    aligned = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    aligned.columns = ["Portfolio", "Benchmark"]

    rolling_cov = aligned["Portfolio"].rolling(window).cov(aligned["Benchmark"])
    rolling_var = aligned["Benchmark"].rolling(window).var()

    return rolling_cov / rolling_var