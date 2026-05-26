import pandas as pd
import streamlit as st

from src.portfolio.optimization import optimize_max_sharpe, optimize_min_volatility


def render_optimization_tab(prices):
    st.subheader("Portfolio Optimization")

    max_sharpe_weights, max_sharpe_perf = optimize_max_sharpe(prices)
    min_vol_weights, min_vol_perf = optimize_min_volatility(prices)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Max Sharpe Portfolio")

        st.dataframe(
            pd.DataFrame.from_dict(
                max_sharpe_weights,
                orient="index",
                columns=["Weight"],
            ).style.format("{:.2%}"),
            width="stretch",
        )

        st.write(f"Expected Return: {max_sharpe_perf[0]:.2%}")
        st.write(f"Volatility: {max_sharpe_perf[1]:.2%}")
        st.write(f"Sharpe Ratio: {max_sharpe_perf[2]:.2f}")

    with col2:
        st.markdown("### Minimum Volatility Portfolio")

        st.dataframe(
            pd.DataFrame.from_dict(
                min_vol_weights,
                orient="index",
                columns=["Weight"],
            ).style.format("{:.2%}"),
            width="stretch",
        )

        st.write(f"Expected Return: {min_vol_perf[0]:.2%}")
        st.write(f"Volatility: {min_vol_perf[1]:.2%}")
        st.write(f"Sharpe Ratio: {min_vol_perf[2]:.2f}")