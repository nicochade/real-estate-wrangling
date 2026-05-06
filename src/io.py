"""Data loading and saving helpers for the Melbourne + AirBnB project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

MELBOURNE_URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv"
AIRBNB_URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/cleansed_listings_dec18.csv"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_melbourne(path: str | Path | None = None) -> pd.DataFrame:
    source = path if path is not None else MELBOURNE_URL
    return pd.read_csv(source)


def load_airbnb(
    path: str | Path | None = None,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    source = path if path is not None else AIRBNB_URL
    return pd.read_csv(source, usecols=columns, low_memory=False)


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / filename
    df.to_csv(out, index=False)
    return out
