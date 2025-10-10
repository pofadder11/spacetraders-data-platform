
# spacetraders-data-platform
fullstack api-familiarisation sandbox
----------------------------

A modular data platform built around the [SpaceTraders API](https://spacetraders.io/), designed as a learning project for data engineering and potentially data science.  
It demonstrates **API integration, SQL databases, analytics, visualization, and testing** using (hopefully) software-development-industry relevant tools and methodologies.

---

## Features
- :white_check_mark: **API Client**: Robust Python client with rate-limit handling and caching
- :white_check_mark: **Database Layer**: PostgreSQL/SQLite with SQLAlchemy ORM (currently on SQLite, Postgres for Docker later)
- :white_check_mark: **Analytics**: Trade route profitability (to add: fleet allocation, contracts)
- :white_check_mark: **Dashboards**: React dashboard with real-time fleet and market arbitrage and profit-loss insights
- ⬜ **Testing & CI/CD**: Pytest, linting, and GitHub Actions for automation
- ⬜ **Dockerized**: Fully reproducible environment

---

## Architecture overview

(API) → [ETL] → (Database: SQL) → [Analytics / ML] → (Dashboards)

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
```

3. Configure

Edit `.env` with your API token and DB connection string.

4. Initialize database

```python
python scripts/init_db.py
```

5. Run ETL

```python
python scripts/run_etl.py #tbd
```

6. Launch dashboard

```bash
streamlit run dashboards/streamlit_app.py #tbd
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
