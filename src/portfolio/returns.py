import pandas as pd
import numpy as np


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    """
    return prices.pct_change().dropna()


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: np.ndarray,
) -> pd.Series:
    """
    Calculate weighted portfolio returns.
    """
    return asset_returns @ weights


def calculate_cumulative_returns(
    returns: pd.Series,
) -> pd.Series:
    """
    Calculate cumulative growth of £1 invested.
    """
    return (1 + returns).cumprod()