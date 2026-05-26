import streamlit as st

from src.portfolio.simulation import monte_carlo_portfolios
from src.visualization.charts import plot_efficient_frontier


def render_simulation_tab(asset_returns):
    st.subheader("Monte Carlo Portfolio Simulation")

    n_portfolios = st.slider(
        "Number of simulated portfolios",
        min_value=1000,
        max_value=10000,
        value=3000,
        step=1000,
    )

    simulation_results = monte_carlo_portfolios(
        asset_returns,
        n_portfolios=n_portfolios,
    )

    st.plotly_chart(plot_efficient_frontier(simulation_results), width="stretch")