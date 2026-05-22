import numpy as np
import pandas as pd


def annualized_return(returns: pd.Series, periods_per_year: int = 252) -> float:
    return returns.mean() * periods_per_year


def annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    return returns.std() * np.sqrt(periods_per_year)


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    excess_returns = returns - risk_free_rate / periods_per_year
    return annualized_return(excess_returns, periods_per_year) / annualized_volatility(returns, periods_per_year)


def max_drawdown(cumulative_returns: pd.Series) -> float:
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1
    return drawdown.min()


def historical_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
    return returns.quantile(1 - confidence_level)