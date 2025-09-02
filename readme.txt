Information flow and terminology

Fetch: Call openapi_client API → get Pydantic-like objects.

Transform: Normalize/trim to fields you want to persist.

Persist (ORM): Create/update rows using SQLAlchemy ORM models and a Session (transaction).

Query: Use ORM to read data for logic, reporting, or export to pandas.

Evolve: Use Alembic migrations to change schema over time (not strictly needed day 1, but best practice).

What is an ORM and how SQLAlchemy fits

ORM maps classes ↔ tables and object instances ↔ rows. You work with Python objects; the ORM issues SQL behind the scenes.

SQLAlchemy has two layers:
    Core: SQL expression layer (explicit SQL building).

    ORM: Declarative models, relationships, sessions, identity map, transactions.

Key pieces:

Declarative Base: class registry for your tables.

Session: unit-of-work and transaction boundary.

Identity map: a session ensures one Python object per row identity.

Transactions: you commit or rollback as a unit.