from __future__ import annotations

from pathlib import Path
import argparse

from src.db import build_sqlite, run_query


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=None, help="Path to sqlite db (optional).")
    args = parser.parse_args()

    dbfile = Path(args.db) if args.db else None
    dbfile = build_sqlite(dbfile=dbfile)

    qdir = project_root() / "queries"
    query_files = [
        qdir / "tables_count.sql",
        qdir / "melbourne_price_by_type.sql",
        qdir / "airbnb_price_by_zipcode_top10.sql",
    ]

    for qpath in query_files:
        sql = read_sql(qpath)
        df = run_query(sql, dbfile=dbfile)
        print(f"\n--- {qpath.stem} ---")
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
