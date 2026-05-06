"""SQLite engine and table-loading helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "data" / "interim"
DB_PATH = DB_DIR / "melbourne_airbnb.db"


def get_engine() -> Engine:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{DB_PATH}")


def load_dataframes_to_db(melb_df: pd.DataFrame, airbnb_df: pd.DataFrame) -> None:
    engine = get_engine()
    melb_df.to_sql("melbourne", engine, index=False, if_exists="replace")
    airbnb_df.to_sql("airbnb", engine, index=False, if_exists="replace")
