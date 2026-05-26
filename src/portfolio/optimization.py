from pypfopt import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import risk_models

import pandas as pd


def optimize_max_sharpe(prices: pd.DataFrame):
    mu = expected_returns.mean_historical_return(prices)
    S = risk_models.sample_cov(prices)

    ef = EfficientFrontier(mu, S)

    weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    performance = ef.portfolio_performance(verbose=False)

    return cleaned_weights, performance


def optimize_min_volatility(prices: pd.DataFrame):
    mu = expected_returns.mean_historical_return(prices)
    S = risk_models.sample_cov(prices)

    ef = EfficientFrontier(
    mu,
    S,
    weight_bounds=(0.05, 0.40),
)

    weights = ef.min_volatility()

    cleaned_weights = ef.clean_weights()

    performance = ef.portfolio_performance(verbose=False)

    return cleaned_weights, performance