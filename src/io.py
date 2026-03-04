from __future__ import annotations

from pathlib import Path
import pandas as pd

MELB_URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv"

AIRBNB_URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/cleansed_listings_dec18.csv"

AIRBNB_INTERESTING_COLS = [
    "description", "neighborhood_overview",
    "street", "neighborhood", "city", "suburb", "state", "zipcode",
    "price", "weekly_price", "monthly_price",
    "latitude", "longitude",
]

def load_airbnb(url: str = AIRBNB_URL) -> pd.DataFrame:
    """Load Airbnb listings and keep only available columns (robust to schema changes)."""
    df = pd.read_csv(url, low_memory=False)
    cols_ok = [c for c in AIRBNB_INTERESTING_COLS if c in df.columns]
    if cols_ok:
        df = df[cols_ok].copy()
    return df


def project_root() -> Path:
    """Return the repository root path (assumes this file is in src/)."""
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    return project_root() / "data"


def load_melbourne(url: str = MELB_URL) -> pd.DataFrame:
    """Load the Melbourne housing dataset from a URL."""
    return pd.read_csv(url)


def save_processed(df: pd.DataFrame, filename: str = "melb_processed.parquet") -> Path:
    """
    Save a processed dataset into data/processed/.

    Returns the output path.
    """
    out_dir = data_dir() / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    try:
        df.to_parquet(out_path, index=False)
    except Exception:
        out_path = out_path.with_suffix(".csv")
        df.to_csv(out_path, index=False)

    return out_path
