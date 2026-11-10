#!/usr/bin/env python3
"""Rebuild every generated page in order, then the extras (sitemap, llms.txt, robots.txt, 404, sources page).

index.html and the fee page are edited by hand; every builder copies the style, header and footer from index.html.
"""
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ORDER = ["build_faq.py", "build_setup.py", "build_loanback.py", "build_whoruns.py", "build_vssipp.py",
         "build_property.py", "build_contrib.py", "build_disadv.py", "build_test.py", "build_about.py",
         "build_contact.py", "build_privacy.py", "build_cookies.py", "build_blog.py", "build_extras.py"]

for name in ORDER:
    r = subprocess.run([sys.executable, str(SRC / name)], capture_output=True, text=True)
    status = "ok" if r.returncode == 0 else "FAILED"
    print(f"{status:6} {name}")
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit(1)
    for line in r.stdout.splitlines():
        if "WARNING" in line:
            print("       " + line)
