import streamlit as st

from src.visualization.charts import (
    plot_drawdown,
    plot_rolling_volatility,
    plot_returns_distribution,
    plot_correlation_heatmap,
)


def render_risk_tab(drawdown, rolling_vol, portfolio_returns, asset_returns):
    st.subheader("Risk Analysis")

    st.plotly_chart(plot_drawdown(drawdown), width="stretch")
    st.plotly_chart(plot_rolling_volatility(rolling_vol), width="stretch")

    col_left, col_right = st.columns(2)

    with col_left:
        st.plotly_chart(plot_returns_distribution(portfolio_returns), width="stretch")

    with col_right:
        st.plotly_chart(plot_correlation_heatmap(asset_returns), width="stretch")