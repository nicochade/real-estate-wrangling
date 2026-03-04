from __future__ import annotations

import pandas as pd


def _to_numeric_money(s: pd.Series) -> pd.Series:
    """Convert strings like '$1,234.00' to float."""
    s = s.astype(str).str.replace(r"[^0-9\.]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def aggregate_airbnb_by_zipcode(airbnb_df: pd.DataFrame, min_count: int = 5) -> pd.DataFrame:
    """
    Aggregate Airbnb listings by zipcode with price summary statistics.

    Requires columns: 'zipcode', 'price'.
    """
    df = airbnb_df.copy()

    if "zipcode" not in df.columns or "price" not in df.columns:
        raise ValueError("airbnb_df must contain columns: 'zipcode' and 'price'")

    df["zipcode"] = pd.to_numeric(df["zipcode"], errors="coerce").astype("Int64")
    df["price"] = _to_numeric_money(df["price"])

    df = df.dropna(subset=["zipcode", "price"])

    agg = (
        df.groupby("zipcode")["price"]
        .agg(
            median_price="median",
            mean_price="mean",
            min_price="min",
            max_price="max",
            record_count="count",
        )
        .reset_index()
    )

    return agg[agg["record_count"] >= min_count].reset_index(drop=True)


def merge_airbnb_agg(
    melb_df: pd.DataFrame,
    airbnb_agg: pd.DataFrame,
    melb_postcode_col: str = "Postcode",
) -> pd.DataFrame:
    """Left-join Melbourne data with Airbnb aggregates by postcode/zipcode."""
    left = melb_df.copy()
    left[melb_postcode_col] = pd.to_numeric(left[melb_postcode_col], errors="coerce").astype("Int64")

    out = left.merge(airbnb_agg, how="left", left_on=melb_postcode_col, right_on="zipcode")
    return out.drop(columns=["zipcode"], errors="ignore")