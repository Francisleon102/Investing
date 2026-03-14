from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockTradesRequest
from alpaca.data.timeframe import TimeFrame

from account import API_KEY, API_SECRET


DEFAULT_SYMBOL = "INTC"
DEFAULT_START = datetime(2026, 3, 13, tzinfo=timezone.utc)

NP_QUOTES_PATH = Path("np_stock_data.npy")
NP_TRADES_PATH = Path("np_stock_trades.npy")
NP_BARS_PATH = Path("np_stock_bars.npy")


class AlpacaDataClient:
    """Same style as your Alpaca class, focused on stock historical data."""

    def __init__(self, api_key: str, api_secret: str):
        self.stock_hist = StockHistoricalDataClient(api_key, api_secret)

    def stock_quotes(self, symbols, start=None, end=None, limit=None, feed=None):
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit,
            feed=feed,
        )
        return self.stock_hist.get_stock_quotes(req)

    def stock_trades(self, symbols, start=None, end=None, limit=None, feed=None):
        req = StockTradesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit,
            feed=feed,
        )
        return self.stock_hist.get_stock_trades(req)

    def stock_bars(self, symbols, timeframe, start=None, end=None, limit=None, feed=None):
        req = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit,
            feed=feed,
        )
        return self.stock_hist.get_stock_bars(req)


def _normalize_df(df: pd.DataFrame | None) -> np.ndarray:
    if df is None or df.empty:
        return np.empty((0, 0), dtype=object)

    df = df.sort_index().reset_index()

    # Keep datetime first when present.
    if "timestamp" in df.columns:
        ordered = ["timestamp"] + [c for c in df.columns if c != "timestamp"]
        df = df[ordered].sort_values("timestamp")

    return df.to_numpy(dtype=object)


def _load_cached(path: Path) -> np.ndarray:
    return np.asarray(np.load(path, allow_pickle=True), dtype=object)


def _pull_or_cache(name: str, path: Path, pull_fn, refresh: bool) -> tuple[np.ndarray, bool]:
    if path.exists() and not refresh:
        cached = _load_cached(path)
        print(f"{name}: cache hit ({path}) rows={len(cached)}")
        return cached, True

    pulled = _normalize_df(pull_fn())
    if pulled.size == 0:
        print(f"{name}: no data returned")
        return pulled, False

    np.save(path, pulled)
    print(f"{name}: saved {path} rows={len(pulled)}")
    return pulled, False


def run(
    symbol: str = DEFAULT_SYMBOL,
    start: datetime = DEFAULT_START,
    end: datetime | None = None,
    refresh: bool = False,
    bars_timeframe: TimeFrame = TimeFrame.Minute,
):
    client = AlpacaDataClient(API_KEY, API_SECRET)
    end = end or datetime.now(timezone.utc)

    quotes, quotes_cached = _pull_or_cache(
        name="quotes",
        path=NP_QUOTES_PATH,
        pull_fn=lambda: client.stock_quotes(symbols=symbol, start=start, end=end).df,
        refresh=refresh,
    )

    trades, trades_cached = _pull_or_cache(
        name="trades",
        path=NP_TRADES_PATH,
        pull_fn=lambda: client.stock_trades(symbols=symbol, start=start, end=end).df,
        refresh=refresh,
    )

    bars, bars_cached = _pull_or_cache(
        name="bars",
        path=NP_BARS_PATH,
        pull_fn=lambda: client.stock_bars(
            symbols=symbol,
            timeframe=bars_timeframe,
            start=start,
            end=end,
        ).df,
        refresh=refresh,
    )

    return {
        "quotes": quotes,
        "trades": trades,
        "bars": bars,
        "quotes_cached": quotes_cached,
        "trades_cached": trades_cached,
        "bars_cached": bars_cached,
    }


if __name__ == "__main__":
    run()
