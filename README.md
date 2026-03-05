# Real Estate Wrangling & Enrichment Pipeline (Melbourne)

This project turns a couple of “assignment notebooks” into a small, reproducible data pipeline.

It loads the Melbourne housing dataset, enriches it with Airbnb signals aggregated by zipcode, applies a few cleaning steps, and then runs a preprocessing stage (encoding + imputation + PCA). The result is a processed dataset you can reuse for analysis or modeling, plus a short notebook that visualizes the main outputs.

## What’s inside
- `src/`
  - `pipeline.py` — runs everything end-to-end (one command)
  - `io.py` — data loading/saving helpers
  - `cleaning.py` — missingness + quantile outlier filtering
  - `enrichment.py` — Airbnb aggregation by zipcode + merge into Melbourne data
  - `preprocessing.py` — one-hot encoding + iterative KNN imputation + PCA features
  - `validation.py` — small sanity checks
  - `showcase_io.py` — loads the processed dataset for notebooks
- `notebooks/01_showcase.ipynb` — reads the processed dataset and plots a few key views
- `environment.yml` — conda environment for reproducibility

## Quickstart

### 1) Create the environment
```bash
conda env create -f environment.yml
conda activate real-estate-wrangling

## Optional: SQL module
This repo also includes a small SQLite module (built locally under `data/interim/`) to run a few example SQL queries.

Run:
```bash
python -m src.run_queries
