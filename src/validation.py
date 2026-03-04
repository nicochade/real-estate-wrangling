from __future__ import annotations

import pandas as pd


def validate_processed_dataset(df: pd.DataFrame) -> None:
    """
    Minimal validation for the processed dataset.
    Raises ValueError with a clear message if something is wrong.
    """
    if df.empty:
        raise ValueError("Processed dataset is empty.")

    # Must-have columns (adjust later if needed)
    required = ["Price", "Postcode"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Basic plausibility checks
    if (df["Price"].isna().mean() > 0.0):
        # after preprocessing/imputation, Price should be present
        raise ValueError("Price has missing values after processing.")

    if (df["Price"] <= 0).any():
        raise ValueError("Found non-positive Price values.")

    # PCA columns if present (we will add them in the pipeline)
    for c in ["pca1", "pca2"]:
        if c in df.columns and df[c].isna().any():
            raise ValueError(f"{c} contains missing values.")

    # No duplicated index expected
    if df.index.has_duplicates:
        raise ValueError("Dataset index has duplicates.")


def report_missingness(df: pd.DataFrame) -> pd.Series:
    """Return missingness rate per column (fraction)."""
    return df.isna().mean().sort_values(ascending=False)
