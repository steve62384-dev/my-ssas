#!/usr/bin/env python3
"""Check the built site: internal links and anchors, JSON-LD, dashes, and phone width (390px)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
problems = []

pages = [p for p in ROOT.rglob("*.html") if not p.relative_to(ROOT).parts[0].startswith("_")]
ids = {}
for p in pages:
    ids[p] = set(re.findall(r'\sid="([^"]+)"', p.read_text(encoding="utf-8")))


def target_file(path):
    path = path.split("?")[0]
    if path.endswith("/"):
        return ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    return ROOT / path.lstrip("/")


for p in pages:
    t = p.read_text(encoding="utf-8")
    rel = p.relative_to(ROOT)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{rel}: bad JSON-LD ({e})")
    if "—" in t or "–" in t:
        problems.append(f"{rel}: contains an em or en dash")
    for href in re.findall(r'href="([^"]+)"', t):
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids[p]:
                problems.append(f"{rel}: missing anchor {href}")
            continue
        path, _, frag = href.partition("#")
        f = target_file(path)
        if not f.exists():
            problems.append(f"{rel}: broken link {href}")
        elif frag and f in ids and frag not in ids[f]:
            problems.append(f"{rel}: missing anchor {href}")

for f in ["robots.txt", "sitemap.xml", "llms.txt"]:
    t = (ROOT / f).read_text(encoding="utf-8")
    if "—" in t or "–" in t:
        problems.append(f"{f}: contains an em or en dash")
    for loc in re.findall(r"https://my-ssas\.co\.uk(/[^\s<)]*)", t):
        if not target_file(loc).exists():
            problems.append(f"{f}: points to missing {loc}")

if "--no-browser" not in sys.argv:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844})
        for p in sorted(pages):
            pg.goto(p.as_uri())
            w = pg.evaluate("document.documentElement.scrollWidth")
            if w > 390:
                problems.append(f"{p.relative_to(ROOT)}: wider than a phone ({w}px)")
        b.close()

print(f"checked {len(pages)} pages")
print("\n".join(problems) if problems else "no problems found")
sys.exit(1 if problems else 0)
