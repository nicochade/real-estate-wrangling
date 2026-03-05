from __future__ import annotations

from pathlib import Path
import sqlite3
import pandas as pd

from src.io import load_melbourne, load_airbnb


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def db_path(default_name: str = "real_estate.db") -> Path:
    out_dir = project_root() / "data" / "interim"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / default_name


def build_sqlite(dbfile: Path | None = None, if_exists: str = "replace") -> Path:
    """
    Build a local SQLite database with two tables:
      - melbourne
      - airbnb_listings
    """
    dbfile = dbfile or db_path()
    conn = sqlite3.connect(dbfile)

    melb = load_melbourne()
    air = load_airbnb()

    melb.to_sql("melbourne", conn, if_exists=if_exists, index=False)
    air.to_sql("airbnb_listings", conn, if_exists=if_exists, index=False)

    conn.commit()
    conn.close()
    return dbfile


def run_query(sql: str, dbfile: Path | None = None) -> pd.DataFrame:
    dbfile = dbfile or db_path()
    conn = sqlite3.connect(dbfile)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
