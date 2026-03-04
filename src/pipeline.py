from __future__ import annotations

from src.io import load_melbourne, load_airbnb, save_processed
from src.cleaning import filter_outliers_by_quantiles
from src.enrichment import aggregate_airbnb_by_zipcode, merge_airbnb_agg
from src.preprocessing import one_hot_encode, impute_iterative_knn, add_pca_columns
from src.validation import validate_processed_dataset


CAT_COLS = ["Suburb", "Type", "Method", "SellerG", "CouncilArea", "Regionname"]
OUTLIER_COLS = ["Price", "Distance"]


def run_pipeline() -> str:
    # 1) Load
    melb = load_melbourne()
    air = load_airbnb()

    # 2) Clean (light)
    melb = filter_outliers_by_quantiles(melb, cols=OUTLIER_COLS, q_low=0.01, q_high=0.99)

    # 3) Enrich
    air_agg = aggregate_airbnb_by_zipcode(air, min_count=5)
    df = merge_airbnb_agg(melb, air_agg)

    # 4) Preprocess (encode + impute + PCA)
    num_cols = df.select_dtypes(include="number").columns.tolist()
    X, _ = one_hot_encode(df, cat_cols=CAT_COLS, num_cols=num_cols, top_k=10)
    X_imp = impute_iterative_knn(X, n_neighbors=10, scale=True)
    X_pca, _ = add_pca_columns(X_imp, n_components=20, add_first_k=2)

    # 5) Validate
    validate_processed_dataset(X_pca)

    # 6) Save
    out_path = save_processed(X_pca, filename="melb_processed.parquet")
    return str(out_path)


if __name__ == "__main__":
    path = run_pipeline()
    print(f"Saved: {path}")
