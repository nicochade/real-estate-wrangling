from __future__ import annotations

from pathlib import Path
import argparse

from src.db import build_sqlite, run_query


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=None, help="Path to sqlite db (optional).")
    args = parser.parse_args()

    dbfile = Path(args.db) if args.db else None
    dbfile = build_sqlite(dbfile=dbfile)

    queries = {
        "tables_count": """
            SELECT
              (SELECT COUNT(*) FROM melbourne) AS melbourne_rows,
              (SELECT COUNT(*) FROM airbnb_listings) AS airbnb_rows;
        """,
        "melbourne_price_by_type": """
            SELECT Type, COUNT(*) AS n, AVG(Price) AS avg_price
            FROM melbourne
            WHERE Price IS NOT NULL
            GROUP BY Type
            ORDER BY avg_price DESC;
        """,
        "airbnb_price_by_zipcode_top10": """
            SELECT zipcode, COUNT(*) AS n, AVG(CAST(REPLACE(REPLACE(price,'$',''),',','') AS REAL)) AS avg_price
            FROM airbnb_listings
            WHERE zipcode IS NOT NULL AND price IS NOT NULL
            GROUP BY zipcode
            HAVING n >= 5
            ORDER BY avg_price DESC
            LIMIT 10;
        """,
    }

    for name, sql in queries.items():
        df = run_query(sql, dbfile=dbfile)
        print(f"\n--- {name} ---")
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
