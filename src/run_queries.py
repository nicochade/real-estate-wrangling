"""Run the 6 SQL exploratory queries against the SQLite database.

If the database isn't populated yet, this will load the raw Melbourne and AirBnB
datasets, aggregate the AirBnB data by zipcode, and write both tables before
running the queries.

Usage:
    python -m src.run_queries
"""

from __future__ import annotations

import pandas as pd
from sqlalchemy import inspect, text

from src import io as data_io
from src.db import get_engine, load_dataframes_to_db

QUERIES: dict[str, str] = {
    "Cantidad de registros por ciudad": """
        SELECT CouncilArea AS ciudad, COUNT(*) AS cantidad
        FROM melbourne
        GROUP BY ciudad
        ORDER BY cantidad DESC
    """,
    "Top 10 barrios por cantidad de registros": """
        SELECT Suburb AS barrio, CouncilArea AS ciudad, COUNT(*) AS cantidad
        FROM melbourne
        GROUP BY barrio, ciudad
        ORDER BY cantidad DESC
        LIMIT 10
    """,
    "Propiedades con más de 2 habitaciones por ciudad": """
        SELECT CouncilArea AS ciudad, COUNT(*) AS cantidad
        FROM melbourne
        WHERE Rooms > 2
        GROUP BY ciudad
        ORDER BY cantidad DESC
    """,
    "Precio promedio por tipo y ciudad": """
        SELECT Type, CouncilArea AS ciudad, AVG(Price) AS precio_promedio
        FROM melbourne
        GROUP BY Type, ciudad
        ORDER BY precio_promedio DESC
    """,
    "Top 5 barrios con propiedades más caras (promedio)": """
        SELECT Suburb AS barrio, AVG(Price) AS precio_promedio
        FROM melbourne
        GROUP BY barrio
        ORDER BY precio_promedio DESC
        LIMIT 5
    """,
    "Join Melbourne x AirBnB agregado por código postal": """
        SELECT m.Suburb, m.Postcode, m.Price,
               a.airbnb_price_mean, a.airbnb_weekly_price_mean, a.airbnb_monthly_price_mean
        FROM melbourne m
        JOIN airbnb a ON m.Postcode = a.zipcode
        LIMIT 10
    """,
}


def _ensure_db_populated() -> None:
    engine = get_engine()
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    if {"melbourne", "airbnb"}.issubset(existing):
        return

    melb_df = data_io.load_melbourne()
    melb_df["Date"] = pd.to_datetime(melb_df["Date"], errors="coerce")
    melb_df["Postcode"] = melb_df["Postcode"].astype(int)

    interesting_cols = [
        "description", "neighborhood_overview",
        "street", "neighborhood", "city", "suburb", "state", "zipcode",
        "price", "weekly_price", "monthly_price",
        "latitude", "longitude",
    ]
    airbnb_df = data_io.load_airbnb(columns=interesting_cols)
    airbnb_df["zipcode"] = airbnb_df["zipcode"].astype(str).str.extract(r"(\d+)")
    airbnb_df["zipcode"] = pd.to_numeric(airbnb_df["zipcode"], errors="coerce").astype("Int64")

    airbnb_agg = airbnb_df.groupby("zipcode", dropna=True).agg(
        airbnb_price_median=("price", "median"),
        airbnb_price_mean=("price", "mean"),
        airbnb_weekly_price_mean=("weekly_price", "mean"),
        airbnb_monthly_price_mean=("monthly_price", "mean"),
        airbnb_price_min=("price", "min"),
        airbnb_price_max=("price", "max"),
        airbnb_record_count=("price", "count"),
    ).reset_index()
    airbnb_agg = airbnb_agg[airbnb_agg["airbnb_record_count"] >= 5]

    load_dataframes_to_db(melb_df, airbnb_agg)


def main() -> None:
    _ensure_db_populated()
    engine = get_engine()
    with engine.connect() as conn:
        for title, query in QUERIES.items():
            print(f"\n=== {title} ===")
            for row in conn.execute(text(query)).fetchall():
                print(row)


if __name__ == "__main__":
    main()
