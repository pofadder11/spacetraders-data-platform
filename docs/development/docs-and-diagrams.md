---
title: Docs & Diagrams
---

# Docs & Diagrams

This repo includes a light-weight setup for docs, static diagrams, and a runtime call-tree.

What you get:
- MkDocs (Material) site from docstrings and `docs/` content
- Auto class/package diagrams via `pyreverse` and import graphs via `pydeps`
- One-command runtime call-tree with VizTracer
- Architecture contracts via `import-linter` (tighten over time)

## Quickstart

1) Install the docs toolchain:

```bash
pip install -r requirements-docs.txt
```

Also install Graphviz (required for image generation by pyreverse/pydeps):

- Windows (PowerShell): `winget install Graphviz.Graphviz` or `choco install graphviz`
- macOS (Homebrew): `brew install graphviz`
- Linux (Debian/Ubuntu): `sudo apt-get install graphviz`

If you installed Graphviz on Windows during an open terminal, restart your terminal so PATH updates (look for `C:\\Program Files\\Graphviz\\bin` containing `dot.exe`).

2) Build the docs site locally:

```bash
mkdocs serve
# or
mkdocs build --strict
```

3) Generate diagrams:

```bash
python display/generate_diagrams.py
```

Artifacts are written to `display/diagrams/`. If Graphviz is not installed, the script falls back to DOT files (e.g., `*.dot`) which you can render later once Graphviz is available.

4) Capture a runtime call tree (VizTracer):

```bash
viztracer --ignore_site_packages --output display/trace.json run.py
# or trace a specific module
viztracer --ignore_site_packages --output display/trace.json -m services.actions
vizviewer display/trace.json
```

5) Check import architecture contracts:

```bash
lint-imports
```

## Conventions

- Keep visual outputs in `display/` (git-ignored where appropriate).
- Prefer documenting public functions/classes with Google-style docstrings.
- If you add a new package/module, consider updating the import-linter contracts.
