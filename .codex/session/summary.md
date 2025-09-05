# Session Summary

- Context: Starting fresh after generating the OpenAPI client. Goal is a clean async PostgreSQL write-through architecture with domain models, adapters, caching, and orchestration.
- Decisions: 
  - Use async SQLModel + asyncpg with Alembic migrations. 
  - Separate layers: generated DTOs → adapters → Pydantic domain models (immutable) → ORM models.
  - Split DB into reference vs telemetry schemas. 
  - Centralize writes via `DbWriter` queue. 
  - Use cache + TTL in `DataService`. 
  - Store config in `.env` and `config/settings.py`.
- TODOs:
  - [ ] Create repo layout with `adapters/`, `domain/`, `db/`, `services/`, `runners/`, `tests/`.
  - [ ] Add `pyproject.toml` with dependencies (`sqlmodel`, `asyncpg`, `alembic`, `pydantic`, etc.).
  - [ ] Add `.env.example` and `config/settings.py` loader.
  - [ ] Implement `db/session.py` with async engine + session factory.
  - [ ] Implement `db/models.py` with reference (systems, waypoints) and telemetry (ships, markets, contracts).
  - [ ] Init Alembic, wire `env.py` to async engine, create and run first migration.
  - [ ] Implement `domain/` models (`ShipState`, `MarketState`, etc.) as immutable Pydantic objects.
  - [ ] Implement `adapters/` mappers (DTO → domain).
  - [ ] Implement `db/repositories.py` with idempotent upserts.
  - [ ] Implement `db/queue.py` with `DbWriter` async queue + background writer.
  - [ ] Implement `services/data_service.py` with cache + TTL + write-through.
  - [ ] Add `services/fleet_service.py` and `services/market_service.py` for orchestration logic.
  - [ ] Implement `runners/fleet_loop.py` and `runners/poll_markets.py` for end-to-end tests.
  - [ ] Ensure generated OpenAPI client is async-capable; wrap in client factory.
  - [ ] Add `tests/` for adapters, repositories, and services.
  - [ ] Add linting/formatting (ruff/black) and optional GitHub Actions CI for tests + Alembic.
- Assumptions: PostgreSQL available at `postgresql+asyncpg://st_dev:st_dev@localhost:5432/spacetraders_dev`; `.env` provides DB URL + API token; VS Code Codex extension runs commands in repo.

## Docs/Visualisation Plan

- MkDocs (Material): optional later for developer docs, quickstart, and diagrams.
- Diagrams: possible `pyreverse` + `pydeps` integration under `display/`.
- Runtime tracing: VizTracer optional for call tree debugging.
- CI: GitHub Action for migrations/tests, lint/format, and optional docs build.

Implemented in this session:
- Defined clean project structure and directory layout.
- Drafted full to-do list covering DB, services, adapters, and runners.
- Provided sample code snippets for each component (DbWriter, DataService, adapters, etc.).

Next session default: auto-read `.codex/session/summary.md` and tail `.codex/history/<session>.jsonl` to bootstrap context before coding tasks.
