import streamlit as st

from src.visualization.charts import (
    plot_benchmark_comparison,
    plot_rolling_beta,
)


def render_benchmark_tab(
    benchmark_ticker,
    cumulative_returns,
    benchmark_cumulative,
    rolling_beta,
    tracking_error,
    information_ratio,
):
    st.subheader("Benchmark Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Benchmark", benchmark_ticker.upper())
    col2.metric("Tracking Error", f"{tracking_error:.2%}")
    col3.metric("Information Ratio", f"{information_ratio:.2f}")

    st.plotly_chart(
        plot_benchmark_comparison(cumulative_returns, benchmark_cumulative),
        width="stretch",
    )

    st.plotly_chart(
        plot_rolling_beta(rolling_beta),
        width="stretch",
    )