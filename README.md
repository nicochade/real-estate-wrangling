# Real Estate Wrangling + ML Preprocessing — Portfolio Project

This repo is a **refactor of a university data wrangling assignment into a portfolio project**. The original deliverable was split across two Spanish notebooks; here it lives as one coherent Spanish narrative split into two explicit tracks.

The core artifact is [`notebooks/showcase_real_estate.ipynb`](notebooks/showcase_real_estate.ipynb), which runs top-to-bottom on a fresh kernel.

## Structure

```
notebooks/showcase_real_estate.ipynb   # the showcase notebook (Spanish)
src/io.py                              # data loading + saving helpers
src/db.py                              # SQLite engine + table loading
src/run_queries.py                     # standalone SQL exploration module
data/{raw,interim,processed}/          # untracked working data folders
environment.yml                        # conda environment spec
```

## What the notebook covers

The notebook is organized into two tracks on top of the same raw Melbourne dataset.

- **Track A — Wrangling + AirBnB enrichment.** SQL exploration via SQLAlchemy + SQLite, feature selection, missing-value analysis, percentile-based outlier removal, AirBnB aggregation by zipcode, and merge into a clean dataset.
- **Track B — ML preprocessing.** OneHotEncoding (top-10 categories + "Other"), KNN-based iterative imputation (with vs. without scaling), PCA with `StandardScaler`, and saving the processed feature matrix.

Track B reloads Melbourne raw because the encoding / imputation / PCA stages need the full original feature set, while Track A's output is a reduced, enriched subset.

## Setup

```bash
conda env create -f environment.yml
conda activate real-estate-ml
```

## Run

Run the showcase notebook end-to-end from the CLI (used as the main verification step too):

```bash
jupyter nbconvert --execute --to notebook \
  --ExecutePreprocessor.timeout=600 \
  --output showcase_real_estate.executed.ipynb \
  notebooks/showcase_real_estate.ipynb
```

Or open it in JupyterLab:

```bash
jupyter lab notebooks/showcase_real_estate.ipynb
```

The SQL exploration is also runnable as a standalone module (it lazily populates the SQLite database on first run if needed):

```bash
python -m src.run_queries
```

## Data sources

Two public CSVs hosted by FAMAF / Universidad Nacional de Córdoba:

- Melbourne housing: `https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv`
- AirBnB Melbourne (cleansed): `https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/cleansed_listings_dec18.csv`

> ⚠️ **Third-party host availability.** These files live on a university server outside our control; if the host is offline, the notebook and the SQL module will fail to fetch data. You can mirror both files into `data/raw/` and pass local paths to `src.io.load_melbourne(path=...)` / `src.io.load_airbnb(path=...)` to work offline.

## License

MIT — see [LICENSE](LICENSE).
