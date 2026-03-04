from __future__ import annotations

import pandas as pd


def fraction_rows_with_any_missing(df: pd.DataFrame) -> float:
    """Return fraction of rows that have at least one missing value."""
    return df.isna().any(axis=1).mean()


def filter_outliers_by_quantiles(
    df: pd.DataFrame,
    cols: list[str],
    q_low: float = 0.01,
    q_high: float = 0.99,
) -> pd.DataFrame:
    """
    Filter rows keeping values within [q_low, q_high] quantiles for each column.

    Important: this filter is cumulative across columns.
    """
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            continue
        s = out[c]
        if not pd.api.types.is_numeric_dtype(s):
            continue
        lo, hi = s.quantile(q_low), s.quantile(q_high)
        out = out[(s >= lo) & (s <= hi)]
    return out
