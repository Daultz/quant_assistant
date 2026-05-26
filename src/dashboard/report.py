import pandas as pd


def build_markdown_report(
    metrics,
    asset_metrics,
    benchmark_ticker,
    tracking_error,
    information_ratio,
    memo,
):
    report = "# Quant Risk Dashboard Report\n\n"

    report += "## Portfolio Metrics\n\n"
    for key, value in metrics.items():
        if "Ratio" in key:
            report += f"- **{key}:** {value:.2f}\n"
        else:
            report += f"- **{key}:** {value:.2%}\n"

    report += "\n## Benchmark Metrics\n\n"
    report += f"- **Benchmark:** {benchmark_ticker.upper()}\n"
    report += f"- **Tracking Error:** {tracking_error:.2%}\n"
    report += f"- **Information Ratio:** {information_ratio:.2f}\n"

    report += "\n## Asset Metrics\n\n"
    report += asset_metrics.to_markdown()

    report += "\n\n## Risk Memo\n\n"
    report += memo

    return report