from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockTradesRequest
from alpaca.data.timeframe import TimeFrame

from account import API_KEY, API_SECRET


DATA_DIR = Path("Data")
NP_QUOTES_PATH = DATA_DIR / "np_stock_data.npy"
NP_TRADES_PATH = DATA_DIR / "np_stock_trades.npy"
NP_BARS_PATH = DATA_DIR / "np_stock_bars.npy"


class AlpacaDataClient:
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

    df = _reset_all_index_levels(df.sort_index())
    df = _drop_synthetic_row_index_cols(df)
    if "timestamp" in df.columns:
        ordered = ["timestamp"] + [c for c in df.columns if c != "timestamp"]
        df = df[ordered].sort_values("timestamp")

    return df.to_numpy(dtype=object)


def _reset_all_index_levels(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten index safely even when index names collide with column names."""
    if isinstance(df.index, pd.MultiIndex):
        idx_names = [
            n if n is not None else f"index_level_{i}"
            for i, n in enumerate(df.index.names)
        ]
    else:
        idx_names = [df.index.name or "index"]

    existing = {str(c) for c in df.columns}
    safe_names = []
    for name in idx_names:
        base = str(name)
        candidate = base
        suffix = 0
        while candidate in existing or candidate in safe_names:
            suffix += 1
            candidate = f"{base}_idx{suffix}"
        safe_names.append(candidate)

    if isinstance(df.index, pd.MultiIndex):
        df.index = df.index.set_names(safe_names)
    else:
        df.index.name = safe_names[0]

    return df.reset_index()


def _drop_synthetic_row_index_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove reset-generated row-number columns like index/level_0 when they are
    just 0..N-1 counters.
    """
    if df.empty:
        return df

    seq = np.arange(len(df))
    drop_cols = []
    for col in df.columns:
        name = str(col).lower()
        is_index_like = (
            name in {"index", "level_0", "row_id", "index_idx1", "__index_level_0__"}
            or name.startswith("index_level_")
        )
        if not is_index_like:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        if values.notna().all() and np.array_equal(values.to_numpy(dtype=np.int64), seq):
            drop_cols.append(col)

    if drop_cols:
        df = df.drop(columns=drop_cols)
    return df


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

    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, pulled)
    print(f"{name}: saved {path} rows={len(pulled)}")
    return pulled, False


def run_historical_pull(
    symbols,
    start: datetime,
    end: datetime | None = None,
    refresh: bool = False,
    bars_timeframe: TimeFrame = TimeFrame.Minute,
    quotes_path: Path = NP_QUOTES_PATH,
    trades_path: Path = NP_TRADES_PATH,
    bars_path: Path = NP_BARS_PATH,
):
    client = AlpacaDataClient(API_KEY, API_SECRET)
    end = end or datetime.now(timezone.utc)

    quotes, quotes_cached = _pull_or_cache(
        name="quotes",
        path=quotes_path,
        pull_fn=lambda: client.stock_quotes(symbols=symbols, start=start, end=end).df,
        refresh=refresh,
    )
    trades, trades_cached = _pull_or_cache(
        name="trades",
        path=trades_path,
        pull_fn=lambda: client.stock_trades(symbols=symbols, start=start, end=end).df,
        refresh=refresh,
    )
    bars, bars_cached = _pull_or_cache(
        name="bars",
        path=bars_path,
        pull_fn=lambda: client.stock_bars(
            symbols=symbols,
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
