#!/usr/bin/env python3
"""Build the static GitHub Pages site into an output folder (default: _site).

The pages in boq-va-mevalar/ are written in Claude Artifact format: they start
with <title>/<meta>/<link>/<style> and have no <!doctype>, <html>, <head> or
<body> of their own (the artifact host adds those). For GitHub Pages we wrap
each page in a full HTML document with the same small reset the artifact host
uses, and copy the images and the landing page next to them.

Usage:  python3 scripts/build_site.py [output_dir]
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_site").resolve()

# Chapter folders to publish: each holds artifact-format .html pages and an img/ folder.
CHAPTERS = ["boq-va-mevalar", "chalkash-uyga-keldi"]

RESET = (
    "<style>"
    ":root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0;font:14px/1.4 system-ui,-apple-system,'Segoe UI',sans-serif}"
    "img{max-width:100%}[hidden]{display:none!important}"
    "</style>"
)


def wrap(fragment: str) -> str:
    """Turn an artifact-format page into a complete HTML document."""
    if fragment.lstrip().lower().startswith("<!doctype"):
        return fragment  # already a full document
    # Everything up to the end of the first <style> block belongs in <head>.
    m = re.search(r"</style>", fragment, re.I)
    head, body = (fragment[: m.end()], fragment[m.end():]) if m else ("", fragment)
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">', "")
    head = (
        '<link rel="manifest" href="../manifest.webmanifest">\n'
        '<meta name="theme-color" content="#E5505A">\n'
        '<link rel="apple-touch-icon" href="../icons/icon-192.png">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n' + head
    )
    return (
        "<!doctype html>\n<html lang=\"uz\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        f"{RESET}\n{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for name in CHAPTERS:
        src, dst = ROOT / name, OUT / name
        dst.mkdir(parents=True)
        for page in sorted(src.glob("*.html")):
            (dst / page.name).write_text(wrap(page.read_text(encoding="utf-8")), encoding="utf-8")
            print(f"page  {name}/{page.name}")
        for sub in ("img", "audio"):
            if (src / sub).is_dir():
                shutil.copytree(src / sub, dst / sub)
                print(f"{sub:5} {name}/{sub} ({len(list((dst / sub).iterdir()))} files)")

    # Landing page and anything else in site/ is copied as-is.
    for item in (ROOT / "site").iterdir():
        target = OUT / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
        print(f"site  {item.name}")

    (OUT / ".nojekyll").write_text("")
    print(f"done  -> {OUT}")


if __name__ == "__main__":
    main()
