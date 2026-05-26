import pandas as pd


def generate_risk_memo(
    metrics: dict,
    asset_metrics: pd.DataFrame,
    benchmark_ticker: str | None = None,
    tracking_error: float | None = None,
    information_ratio: float | None = None,
):
    annual_return = metrics["Annual Return"]
    annual_vol = metrics["Annual Volatility"]
    sharpe = metrics["Sharpe Ratio"]
    max_dd = metrics["Max Drawdown"]
    var_95 = metrics["Daily VaR 95%"]

    memo = []

    memo.append("## Performance Summary")

    memo.append(
        f"The portfolio delivered an annualized return of **{annual_return:.2%}** "
        f"with annualized volatility of **{annual_vol:.2%}**."
    )

    if sharpe >= 1:
        memo.append(f"The Sharpe ratio of **{sharpe:.2f}** indicates strong risk-adjusted performance.")
    elif sharpe >= 0.5:
        memo.append(f"The Sharpe ratio of **{sharpe:.2f}** indicates moderate risk-adjusted performance.")
    else:
        memo.append(f"The Sharpe ratio of **{sharpe:.2f}** indicates weak risk-adjusted performance.")

    memo.append("## Risk Summary")

    memo.append(
        f"The maximum drawdown was **{max_dd:.2%}**, representing the largest peak-to-trough decline."
    )

    memo.append(
        f"The historical 95% daily VaR was **{var_95:.2%}**, meaning that on the worst 5% "
        f"of trading days, losses were at least this large."
    )

    memo.append("## Concentration and Risk Contribution")

    if "Percentage Risk Contribution" in asset_metrics.columns:
        top_risk_asset = asset_metrics["Percentage Risk Contribution"].idxmax()
        top_risk_value = asset_metrics.loc[top_risk_asset, "Percentage Risk Contribution"]

        memo.append(
            f"The largest contributor to portfolio risk is **{top_risk_asset}**, "
            f"contributing approximately **{top_risk_value:.2%}** of total portfolio risk."
        )

    top_weight_asset = asset_metrics["Weight"].idxmax()
    top_weight_value = asset_metrics.loc[top_weight_asset, "Weight"]

    memo.append(
        f"The largest portfolio weight is **{top_weight_asset}** at **{top_weight_value:.2%}**."
    )

    if benchmark_ticker and tracking_error is not None and information_ratio is not None:
        memo.append("## Benchmark Interpretation")

        memo.append(
            f"Relative to **{benchmark_ticker.upper()}**, the portfolio has tracking error of "
            f"**{tracking_error:.2%}**."
        )

        if information_ratio > 0.5:
            memo.append(
                f"The information ratio of **{information_ratio:.2f}** suggests strong excess return "
                f"relative to benchmark-relative risk."
            )
        elif information_ratio > 0:
            memo.append(
                f"The information ratio of **{information_ratio:.2f}** suggests modest excess return "
                f"relative to benchmark-relative risk."
            )
        else:
            memo.append(
                f"The information ratio of **{information_ratio:.2f}** suggests the portfolio has not "
                f"been rewarded for taking benchmark-relative risk."
            )

    memo.append("## Practical Takeaway")

    if annual_vol > 0.25 or max_dd < -0.30:
        memo.append(
            "The portfolio appears relatively high risk. A risk manager would likely investigate "
            "drawdown exposure, concentration, and sensitivity to broad market moves."
        )
    elif sharpe >= 1 and max_dd > -0.25:
        memo.append(
            "The portfolio shows attractive historical risk-adjusted performance, though the results "
            "should still be tested across different market regimes."
        )
    else:
        memo.append(
            "The portfolio has a mixed profile. Further analysis should focus on diversification, "
            "benchmark-relative performance, and robustness across time periods."
        )

    return "\n\n".join(memo)