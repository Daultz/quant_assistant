import yfinance as yf


def search_tickers(query: str, max_results: int = 10):
    if not query or len(query.strip()) < 2:
        return []

    try:
        results = yf.Search(query.strip(), max_results=max_results).quotes
    except Exception:
        return []

    tickers = []

    for item in results:
        symbol = item.get("symbol")
        name = item.get("shortname") or item.get("longname") or ""
        exchange = item.get("exchange") or ""

        if symbol:
            tickers.append(
                {
                    "symbol": symbol.upper(),
                    "label": f"{symbol.upper()} - {name} ({exchange})",
                    "name": name,
                    "exchange": exchange,
                }
            )

    return tickers