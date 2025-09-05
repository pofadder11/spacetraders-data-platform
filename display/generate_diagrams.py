from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from shutil import which


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "display" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None)


def run_capture(cmd: list[str], *, cwd: Path | None = None) -> str:
    print("$", " ".join(cmd))
    out = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    return out.stdout


def has_cmd(name: str) -> bool:
    return which(name) is not None


def ensure_graphviz() -> bool:
    """Ensure Graphviz 'dot' is on PATH; try common installs on Windows.

    Returns True if 'dot' is available for child processes after this call.
    """
    if has_cmd("dot"):
        return True
    # Try to detect common Windows install locations and patch PATH at runtime
    candidates = [
        Path(r"C:\\Program Files\\Graphviz\\bin"),
        Path(r"C:\\Program Files (x86)\\Graphviz\\bin"),
        Path.home() / r"AppData/Local/Programs/Graphviz/bin",
    ]
    for p in candidates:
        dot_exe = p / "dot.exe"
        if dot_exe.exists():
            os.environ["PATH"] = str(p) + os.pathsep + os.environ.get("PATH", "")
            if has_cmd("dot"):
                return True
    print("[warn] Graphviz 'dot' not found on PATH. Pyreverse/pydeps image generation may fail.")
    print("       Install Graphviz and ensure 'dot' is available (e.g., 'winget install Graphviz.Graphviz').")
    return False


def pyreverse_targets() -> list[str]:
    # Focus on local code, skip generated client
    targets = ["services", "state", "runner", "session", "models.py"]
    return [t for t in targets if (ROOT / t).exists()]


def gen_pyreverse() -> None:
    # Requires pylint (provides 'pyreverse') and Graphviz 'dot' for image output
    targets = pyreverse_targets()
    if not targets:
        print("No pyreverse targets found; skipping.")
        return
    has_dot = ensure_graphviz()
    output_fmt = "png" if has_dot else "dot"
    if has_cmd("pyreverse"):
        cmd = [
            "pyreverse",
            "-o",
            output_fmt,
            "-p",
            "spacetraders",
            "-d",
            str(OUT),
            *targets,
        ]
        run(cmd, cwd=ROOT)
        return
    # Fallback: call the module entrypoint directly
    try_modules = [
        "pylint.pyreverse.main",
        "pylint.pyreverse",
    ]
    last_err = None
    for mod in try_modules:
        cmd = [
            sys.executable,
            "-m",
            mod,
            "-o",
            output_fmt,
            "-p",
            "spacetraders",
            "-d",
            str(OUT),
            *targets,
        ]
        try:
            run(cmd, cwd=ROOT)
            return
        except subprocess.CalledProcessError as e:
            last_err = e
    if last_err:
        print("[error] pyreverse failed. Ensure 'pylint' is installed and 'pyreverse' entrypoint is available.")
        raise last_err
    # If we produced DOT files, some pyreverse versions ignore -d. Move to OUT.
    if output_fmt == "dot":
        for name in ("classes.dot", "packages.dot"):
            src = ROOT / name
            if src.exists():
                dst = OUT / name
                try:
                    src.replace(dst)
                    print(f"[info] Moved {src} -> {dst}")
                except Exception:
                    pass
    else:
        # Some pyreverse versions ignore -d for image output; relocate if needed
        for name in ("classes_spacetraders.png", "packages_spacetraders.png"):
            src = ROOT / name
            if src.exists():
                dst = OUT / name
                try:
                    src.replace(dst)
                    print(f"[info] Moved {src} -> {dst}")
                except Exception:
                    pass


def gen_pydeps() -> None:
    # Generate an import graph for the services package if present
    if not (ROOT / "services").exists():
        print("services/ not found; skipping pydeps.")
        return
    has_dot = ensure_graphviz()
    if has_dot:
        out_svg = OUT / "services-imports.svg"
        cmd_svg = [
            sys.executable,
            "-m",
            "pydeps",
            "services",
            "--max-bacon",
            "2",
            "--noshow",
            "-T",
            "svg",
            "-o",
            str(out_svg),
        ]
        # Run relative to project root for predictable behavior
        run(cmd_svg, cwd=ROOT)
        # Also emit DOT so the HTML preview is available and consistent
        out_dot = OUT / "services-imports.dot"
        cmd_dot = [
            sys.executable,
            "-m",
            "pydeps",
            "services",
            "--max-bacon",
            "2",
            "--show-dot",
            "--no-output",
            "--dot-output",
            str(out_dot),
        ]
        run(cmd_dot, cwd=ROOT)
    else:
        # Fallback: emit valid DOT to file without requiring Graphviz and
        # avoid creating any .svg/.png in the project root.
        out_dot = OUT / "services-imports.dot"
        cmd = [
            sys.executable,
            "-m",
            "pydeps",
            "services",
            "--max-bacon",
            "2",
            "--show-dot",
            "--no-output",  # don't try to run external 'dot' or write images
            "--dot-output",
            str(out_dot),
        ]
        run(cmd, cwd=ROOT)
        print(f"[info] Wrote DOT graph to {out_dot}. Install Graphviz to render to SVG/PNG.")


def gen_dot_previews() -> None:
    """Create HTML previews for DOT files using Viz.js (no Graphviz required)."""
    dot_files = list(OUT.glob("*.dot"))
    if not dot_files:
        return
    viewer_tpl = """<!DOCTYPE html>
<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\"/>\n<title>{title}</title>\n<style>body{{font-family:system-ui,Segoe UI,Arial;margin:0;padding:1rem}}#graph svg{{width:100%;height:auto}}</style>\n</head>\n<body>\n<h3>{title}</h3>\n<div id=\"graph\">Rendering…</div>\n<script src=\"https://cdn.jsdelivr.net/npm/viz.js@2.1.2/viz.js\"></script>\n<script src=\"https://cdn.jsdelivr.net/npm/viz.js@2.1.2/full.render.js\"></script>\n<script>\nconst dot = `{dot}`;\nconst viz = new Viz();\nviz.renderSVGElement(dot).then(el=>{{\n  const g=document.getElementById('graph'); g.innerHTML=''; g.appendChild(el);\n}}).catch(err=>{{\n  document.getElementById('graph').textContent = 'Failed to render DOT: ' + err;\n  console.error(err);\n}});\n</script>\n</body>\n</html>"""
    for dot_path in dot_files:
        try:
            dot_text = dot_path.read_text(encoding="utf-8")
            # Quick sanity-check to avoid trying to render non-DOT (e.g., JSON)
            first = dot_text.lstrip().splitlines()[0] if dot_text.strip() else ""
            if not (first.startswith("digraph") or first.startswith("graph")):
                print(f"[warn] Skipping HTML preview for {dot_path} (does not look like DOT)")
                continue
            # Escape backticks and backslashes for JS template literal
            dot_js = dot_text.replace("\\", r"\\").replace("`", r"\`")
            html = viewer_tpl.format(title=dot_path.name, dot=dot_js)
            html_path = dot_path.with_suffix(dot_path.suffix + ".html")
            html_path.write_text(html, encoding="utf-8")
            print(f"[info] Wrote HTML preview {html_path}")
        except Exception as e:
            print(f"[warn] Could not create HTML preview for {dot_path}: {e}")


def main() -> None:
    gen_pyreverse()
    gen_pydeps()
    gen_dot_previews()
    print(f"Diagrams written to {OUT}")


if __name__ == "__main__":
    main()
