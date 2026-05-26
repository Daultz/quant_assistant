import streamlit as st

from src.portfolio.commentary import generate_risk_memo
from src.dashboard.report import build_markdown_report


def render_commentary_tab(
    metrics,
    asset_metrics,
    benchmark_ticker=None,
    tracking_error=None,
    information_ratio=None,
):
    st.subheader("AI-Style Risk Memo")

    memo = generate_risk_memo(
        metrics=metrics,
        asset_metrics=asset_metrics,
        benchmark_ticker=benchmark_ticker,
        tracking_error=tracking_error,
        information_ratio=information_ratio,
    )

    st.markdown(memo)

    report = build_markdown_report(
        metrics=metrics,
        asset_metrics=asset_metrics,
        benchmark_ticker=benchmark_ticker,
        tracking_error=tracking_error,
        information_ratio=information_ratio,
        memo=memo,
    )

    st.download_button(
        label="Download Risk Report",
        data=report,
        file_name="quant_risk_report.md",
        mime="text/markdown",
    )

    st.caption(
        "This memo is generated from computed portfolio analytics. "
        "It is explanatory and not financial advice."
    )