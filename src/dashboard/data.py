import streamlit as st


def render_data_tab(prices, asset_returns):
    st.subheader("Raw Price Data")
    st.dataframe(prices.tail(20), width="stretch")

    st.subheader("Asset Returns")
    st.dataframe(asset_returns.tail(20), width="stretch")