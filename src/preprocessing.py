from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA


@dataclass(frozen=True)
class EncodingArtifacts:
    encoder: OneHotEncoder
    feature_names: list[str]


def reduce_rare_categories(
    df: pd.DataFrame,
    cat_cols: list[str],
    top_k: int = 10,
    other_label: str = "Other",
) -> pd.DataFrame:
    """Keep only the top_k categories per column; map the rest to other_label."""
    out = df.copy()
    for c in cat_cols:
        if c not in out.columns:
            continue
        top = out[c].value_counts(dropna=False).head(top_k).index
        out[c] = out[c].where(out[c].isin(top), other_label)
    return out


def one_hot_encode(
    df: pd.DataFrame,
    cat_cols: list[str],
    num_cols: list[str],
    top_k: int = 10,
) -> tuple[pd.DataFrame, EncodingArtifacts]:
    """
    One-hot encode categorical columns (after reducing rare categories)
    and return a numeric dataframe ready for imputers/PCA.
    """
    work = df.copy()

    work = reduce_rare_categories(work, cat_cols=cat_cols, top_k=top_k)

    # ensure all selected columns exist
    cat_cols = [c for c in cat_cols if c in work.columns]
    num_cols = [c for c in num_cols if c in work.columns]

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_cat = encoder.fit_transform(work[cat_cols]) if cat_cols else np.empty((len(work), 0))
    cat_feature_names = encoder.get_feature_names_out(cat_cols).tolist() if cat_cols else []

    X_num = work[num_cols].to_numpy() if num_cols else np.empty((len(work), 0))
    num_feature_names = num_cols

    X = np.hstack([X_num, X_cat])
    feature_names = num_feature_names + cat_feature_names

    X_df = pd.DataFrame(X, columns=feature_names, index=work.index)
    return X_df, EncodingArtifacts(encoder=encoder, feature_names=feature_names)


def impute_iterative_knn(
    X: pd.DataFrame,
    n_neighbors: int = 15,
    random_state: int = 10,
    scale: bool = True,
) -> pd.DataFrame:
    """
    Impute missing values using IterativeImputer with a KNN regressor.
    Optionally scale features to [0,1] before imputation and invert back.
    """
    arr = X.to_numpy(dtype=float)

    scaler = None
    if scale:
        scaler = MinMaxScaler()
        arr_scaled = scaler.fit_transform(arr)
    else:
        arr_scaled = arr

    imputer = IterativeImputer(
        estimator=KNeighborsRegressor(n_neighbors=n_neighbors),
        random_state=random_state,
        max_iter=30,
        tol=1e-3,
    )
    arr_imp = imputer.fit_transform(arr_scaled)

    if scale and scaler is not None:
        arr_imp = scaler.inverse_transform(arr_imp)

    return pd.DataFrame(arr_imp, columns=X.columns, index=X.index)


def add_pca_columns(
    X: pd.DataFrame,
    n_components: int = 20,
    add_first_k: int = 2,
    random_state: int = 10,
) -> tuple[pd.DataFrame, PCA]:
    """
    Fit PCA on X and add the first add_first_k components as columns 'pca1', 'pca2', ...
    """
    n_samples, n_features = X.shape
    n_comp = min(n_components, n_samples, n_features)

    pca = PCA(n_components=n_comp, random_state=random_state)
    Z = pca.fit_transform(X.to_numpy(dtype=float))

    out = X.copy()
    for i in range(add_first_k):
        out[f"pca{i+1}"] = Z[:, i]

    return out, pca
