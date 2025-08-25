
## **architecture**

# (API) → [ETL] → (Database: SQL) → [Analytics / ML] → (Dashboards)


## **COMPONENTS**

###  1. **Client** (api/client.py)

  Defines SpaceTradersClient.

  Handles:

  * Authentication (API token from config.py).

  * Request/response logic (_request method).

  * Endpoint wrappers (e.g., list_ships, list_waypoints, get_my_agent).

  * Stores derived context (e.g., system_symbol from my/agent.headquarters).
  

### 2. ETL/Normalizers (api/normalizers.py)

  * Functions to transform raw API JSON → flat dicts (rows).

  * Each endpoint has a matching normalizer (e.g. normalize_ships, normalize_waypoints).

  * Keeps database schema clean and queryable.

### 3. **Database** (api/db.py)

  Manages SQLite schema.

  Provides get_connection() helper.

  Defines tables for:

  - Ships

  - Waypoints

  - Contracts

  - Markets

### 4. Analytics & ML

  Structure and implement responsive logic patterns to optimise for resource gathering and cashflow

  * optimal route planning / travel cost minimisation
  * comparative market trade optimisation
  * optimal resource mining

### 5. **Sync Helpers** (api/sync.py)

  sync_data function: generic wrapper to fetch, normalize, and upsert data.

  Designed to be reusable across multiple endpoints.

  Handles conflict resolution with UPSERT.

### 6. **Testing & FAAFO** (notebooks/exploration.ipynb)

  Jupyter notebook for interactive testing

  GitHub actions from ci.yml
  
### 7. Dashboard

For manual interactivity and monitoring of responsive ML strategies
