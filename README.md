````markdown
# spacetraders-data-platform
fullstack datascience sandbox
----------------------------

A modular data platform built around the [SpaceTraders API](https://spacetraders.io/), designed as a learning project for data engineering and data science.  
It demonstrates **API integration, ETL pipelines, SQL databases, analytics, visualization, and testing** — all with production-style structure (to serve as a learning environment for ).

---

## Features
- **API Client**: Robust Python client with rate-limit handling and caching
- **ETL Pipelines**: Extract/Transform/Load workflows (Prefect/Airflow-ready)
- **Database Layer**: PostgreSQL/SQLite with SQLAlchemy ORM
- **Analytics**: Trade route profitability, fleet allocation, contracts
- **Dashboards**: Streamlit app with real-time fleet and market insights
- **Testing & CI/CD**: Pytest, linting, and GitHub Actions for automation
- **Dockerized**: Fully reproducible environment

---

## Architecture

(API) → [ETL] → (Database: SQL) → [Analytics / ML] → (Dashboards)

See the [ARCHITECTURE.md](ARCHITECTURE.md) for details.

---

## Quickstart

1. Clone the repo

```bash
git clone https://github.com/pofadder11/spacetraders-data-platform.git
cd spacetraders-data-platform
````

2. Setup environment

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Configure

Edit `config.yaml` with your API token and DB connection string.

4. Initialize database

```python
python scripts/init_db.py
```

5. Run ETL

```python
python scripts/run_etl.py
```

6. Launch dashboard

```bash
streamlit run dashboards/streamlit_app.py
```

---

## TESTING

Run all unit and integration tests:

```bash
pytest
```

Lint and check formatting:

```bash
ruff
isort
black --check
```

```
```
