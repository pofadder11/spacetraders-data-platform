Contributing Guidelines

🔹 Branch Naming Convention

Branches should follow the format:

<area>/<type>/<short-description>
Areas

api-client → API client layer (httpx, retries, JSON normalization)

etl-pipeline → ETL orchestration (Prefect/Airflow, transformations, loaders)

db-layer → Database schema, migrations, queries

analytics → Analytics scripts & queries (profit routes, ship allocation, etc.)

decision-logic → Heuristics & ML models (route selection, predictive pricing)

dashboard → Dashboard layer (Streamlit/Dash)

infra → Infrastructure (CI/CD, Docker, deployment, monitoring)

Types

feature → New functionality

fix → Bug fix

chore → Refactor, maintenance, style changes

docs → Documentation only

Examples

api-client/feature/rate-limit-retry
etl-pipeline/fix/scheduler-bug
db-layer/feature/add-contracts-table
dashboard/feature/market-trends-viz
decision-logic/experiment/xgboost-pricing
infra/chore/dockerfile-update
🔹 Commit Message Convention

Each commit message should:

Start with the area (same categories as branches).

Use imperative style (“add,” “fix,” “update”).

Be concise but descriptive.

Format:

<area>: <verb> <description>
Examples:

api-client: add retry with exponential backoff
etl-pipeline: fix timezone issue in scheduler
db-layer: create markets table with indexes
analytics: update ship allocation query
decision-logic: add baseline heuristic for route selection
dashboard: implement fleet status page
infra: update Dockerfile to slim base image
🔹 Linking PRs and Commits to Issues

To ensure work is tracked against tasks and architecture areas:

Reference issues in commit messages or PR descriptions using GitHub keywords:

fixes #23 → closes the issue when merged

closes #45 → same as above

refs #12 → links to the issue without closing it

Example Commit:

dashboard: add contract progress chart (fixes #23)
Example PR Description:

Implements new dashboard feature for visualizing contract progress.
Architecture area: dashboard
Fixes #23
👉 This way:

The issue/task is auto-closed when the PR merges.

You can always trace: Issue → Branch → PR → Commits.

🔹 Workflow

Start from main:

git checkout main
git pull origin main
Create a new branch:

git checkout -b dashboard/feature/contract-progress-plot
Make commits following the convention.

Push branch & open a Pull Request:

git push origin dashboard/feature/contract-progress-plot
PR title = same as branch name.

PR description = include architecture area + issue/task reference.

After merge → branch is deleted, but PR history remains as tracking log.
