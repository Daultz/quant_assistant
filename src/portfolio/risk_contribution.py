import numpy as np
import pandas as pd


def calculate_portfolio_volatility(
    asset_returns: pd.DataFrame,
    weights: np.ndarray,
    periods_per_year: int = 252,
) -> float:
    cov_matrix = asset_returns.cov() * periods_per_year
    portfolio_variance = weights.T @ cov_matrix @ weights
    return np.sqrt(portfolio_variance)


def calculate_risk_contribution(
    asset_returns: pd.DataFrame,
    weights: np.ndarray,
    periods_per_year: int = 252,
) -> pd.DataFrame:
    cov_matrix = asset_returns.cov() * periods_per_year

    portfolio_vol = calculate_portfolio_volatility(
        asset_returns,
        weights,
        periods_per_year,
    )

    marginal_contribution = cov_matrix @ weights / portfolio_vol
    risk_contribution = weights * marginal_contribution
    percentage_contribution = risk_contribution / portfolio_vol

    return pd.DataFrame(
        {
            "Weight": weights,
            "Marginal Risk Contribution": marginal_contribution,
            "Risk Contribution": risk_contribution,
            "Percentage Risk Contribution": percentage_contribution,
        },
        index=asset_returns.columns,
    )