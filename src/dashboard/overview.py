import streamlit as st

from src.visualization.charts import (
    plot_cumulative_returns,
    plot_portfolio_allocation,
)


def render_overview_tab(
    metrics,
    cumulative_returns,
    tickers,
    weights,
    asset_metrics,
):
    st.subheader("Portfolio Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Annual Return", f"{metrics['Annual Return']:.2%}")
    col2.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
    col3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
    col4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
    col5.metric("Daily VaR 95%", f"{metrics['Daily VaR 95%']:.2%}")

    st.plotly_chart(
        plot_cumulative_returns(cumulative_returns),
        width="stretch",
    )

    st.subheader("Portfolio Allocation")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.plotly_chart(
            plot_portfolio_allocation(tickers, weights),
            width="stretch",
        )

    with col_right:
        st.dataframe(
            asset_metrics.style.format(
                {
                    "Weight": "{:.2%}",
                    "Annual Return": "{:.2%}",
                    "Annual Volatility": "{:.2%}",
                    "Risk Contribution": "{:.2%}",
                    "Percentage Risk Contribution": "{:.2%}",
                }
            ),
            width="stretch",
        )