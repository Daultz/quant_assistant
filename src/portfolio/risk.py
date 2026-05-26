import pandas as pd
import numpy as np


def calculate_drawdown(cumulative_returns: pd.Series) -> pd.Series:
    running_max = cumulative_returns.cummax()
    return cumulative_returns / running_max - 1


def rolling_volatility(
    returns: pd.Series,
    window: int = 21,
    periods_per_year: int = 252,
) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(periods_per_year)