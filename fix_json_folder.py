#!/usr/bin/env python3
import argparse
import ast
import json
from pathlib import Path

try:
    import json5  # optional, for JSON with comments/trailing commas
except Exception:
    json5 = None


def try_parse(raw: str):
    """Return (obj, source) where source is 'json', 'json5', or 'ast'."""
    # 1) Try strict JSON
    try:
        return json.loads(raw), "json"
    except Exception:
        pass
    # 2) Try JSON5 (if installed) for comments/trailing commas
    if json5 is not None:
        try:
            return json5.loads(raw), "json5"
        except Exception:
            pass
    # 3) Try Python literal (single quotes, True/False/None)
    try:
        return ast.literal_eval(raw), "ast"
    except Exception as e:
        raise ValueError(
            f"Could not parse as JSON/JSON5/Python-literal: {e}"
        ) from e


def fix_file(p: Path, inplace: bool, backup: bool, force: bool) -> str:
    raw = p.read_text(encoding="utf-8")

    # If it’s .json and not forced, accept valid JSON and skip rewrite
    if p.suffix.lower() == ".json" and not force:
        try:
            json.loads(raw)
            return f"OK (valid JSON): {p.name}"
        except Exception:
            # fall through to repair
            pass

    try:
        obj, source = try_parse(raw)
    except Exception as e:
        return f"❌ FAIL {p.name}: {e}"

    # Determine output path
    if inplace:
        if backup:
            bak = p.with_suffix(p.suffix + ".bak")
            bak.write_text(raw, encoding="utf-8")
        out_path = p
    else:
        out_path = p.with_suffix(p.suffix + ".fixed.json")

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    if out_path == p:
        return f"✅ FIXED (via {source}): {p.name}"
    else:
        return f"✅ WROTE {out_path.name} (via {source})"


def run(
    folder: str,
    recursive: bool,
    inplace: bool,
    backup: bool,
    force: bool,
    exts: list[str],
):
    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"❌ Folder not found: {folder}")
        return

    paths = folder_path.rglob("*") if recursive else folder_path.iterdir()
    exts = {e.lower() for e in exts}

    total = fixed = failed = 0
    for p in paths:
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        total += 1
        msg = fix_file(p, inplace=inplace, backup=backup, force=force)
        print(msg)
        if msg.startswith("✅"):
            fixed += 1
        elif msg.startswith("❌"):
            failed += 1

    print(
        f"\nSummary: scanned={total}, fixed/written={fixed}, failed={failed}"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Validate and repair JSON files in a folder."
    )
    ap.add_argument("folder", nargs="?", default="json_output_samples")
    ap.add_argument(
        "--recursive", action="store_true", help="Recurse into subfolders."
    )
    ap.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite files instead of writing .fixed.json.",
    )
    ap.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not write .bak when using --inplace.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Rewrite even valid .json files (normalize formatting).",
    )
    ap.add_argument(
        "--ext",
        action="append",
        default=[".json", ".txt"],
        help="File extensions to process (repeatable). Default: .json, .txt",
    )
    args = ap.parse_args()

    run(
        folder=args.folder,
        recursive=args.recursive,
        inplace=args.inplace,
        backup=not args.no_backup,
        force=args.force,
        exts=args.ext,
    )
