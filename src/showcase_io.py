from __future__ import annotations

from pathlib import Path
import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_processed(filename: str = "melb_processed.parquet") -> pd.DataFrame:
    path = project_root() / "data" / "processed" / filename
    if not path.exists():
        raise FileNotFoundError(f"Processed file not found: {path}. Run: python -m src.pipeline")
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)
