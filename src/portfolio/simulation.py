import numpy as np
import pandas as pd


def monte_carlo_portfolios(
    asset_returns: pd.DataFrame,
    n_portfolios: int = 5000,
    periods_per_year: int = 252,
):
    n_assets = asset_returns.shape[1]

    mean_returns = asset_returns.mean() * periods_per_year
    cov_matrix = asset_returns.cov() * periods_per_year

    results = []

    for _ in range(n_portfolios):

        weights = np.random.random(n_assets)
        weights /= np.sum(weights)

        portfolio_return = np.dot(weights, mean_returns)

        portfolio_volatility = np.sqrt(
            weights.T @ cov_matrix @ weights
        )

        sharpe_ratio = portfolio_return / portfolio_volatility

        results.append(
            {
                "Return": portfolio_return,
                "Volatility": portfolio_volatility,
                "Sharpe Ratio": sharpe_ratio,
                "Weights": weights,
            }
        )

    return pd.DataFrame(results)