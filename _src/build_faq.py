#!/usr/bin/env python3
"""Build /faq/index.html for my-ssas.co.uk from _src/faq.txt.

Template parts (style, header, footer) are copied from the home page so every
page looks the same. Run from anywhere: python3 build_faq.py
"""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "faq.txt"
HOME = ROOT / "index.html"
OUT = ROOT / "faq" / "index.html"

SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/faq/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"

LABEL_ORDER = ["Law", "HMRC", "TPR", "DWP", "FCA", "FSCS", "PRA", "Ombudsman",
               "MoneyHelper", "GOV.UK", "HM Treasury", "Administrators",
               "Provider evidence", "Steve's analysis"]


def slugify(text):
    text = text.lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def parse(path):
    sections = []
    sec = q = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            title, sid = [p.strip() for p in line[2:].split("|")]
            sec = {"title": title, "id": sid, "note": None, "qs": []}
            sections.append(sec)
            q = None
        elif line.startswith("NOTE:"):
            sec["note"] = line[5:].strip()
        elif line.startswith("## "):
            question = line[3:].strip()
            q = {"q": question, "id": slugify(question), "paras": [], "srcs": []}
            sec["qs"].append(q)
        elif line.startswith("SRC:"):
            label, title, url = [p.strip() for p in line[4:].split("|")]
            q["srcs"].append((label, title, url))
        else:
            q["paras"].append(line.strip())
    return sections


def link(title, url):
    t = html.escape(title, quote=False)
    if url.startswith("http"):
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{t}</a>'
    return f'<a href="{html.escape(url)}">{t}</a>'


def src_line(srcs):
    groups = OrderedDict()
    for label, title, url in srcs:
        groups.setdefault(label, []).append(link(title, url))
    parts = [f'<span class="lbl">{html.escape(lbl)}:</span> ' + "; ".join(items)
             for lbl, items in groups.items()]
    return '<p class="src"><span class="lead">Sources</span> ' + " &middot; ".join(parts) + "</p>"


def plain(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip()


def main():
    sections = parse(SRC)
    qs = [q for s in sections for q in s["qs"]]
    ids = [q["id"] for q in qs]
    assert len(ids) == len(set(ids)), "duplicate question ids"
    n = len(qs)

    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0)
    extra_css = """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 26px 0 6px; }
  .toc h3 { font-size: 17px; margin: 18px 0 4px; }
  .toc ul { padding-left: 20px; margin: 0 0 6px; }
  .toc li { margin-bottom: 3px; }
  p.src { font-size: 14px; color: var(--muted); margin: 6px 0 0; word-break: break-word; }
  p.src .lead { font-weight: 700; margin-right: 4px; }
  p.src .lbl { font-weight: 600; }
  p.back { font-size: 14px; margin: 18px 0 0; }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>"""
    style = style.replace("</style>", extra_css)
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    short = ("a SSAS (small self-administered scheme) is a pension scheme set up by an employer, "
             "usually a company owned and run by its directors. Below are the "
             f"{n} questions people ask most about SSAS pensions. Each answer is in plain English, "
             "with the law or HMRC guidance it relies on linked underneath, so you can check it.")

    # JSON-LD
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/",
         "inLanguage": "en-GB", "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP",
         "url": SITE + "/about/",
         "sameAs": ["https://www.linkedin.com/in/steve~hunt", "https://www.youtube.com/@SteveHuntACIITEP",
                    "https://x.com/SHunt_ACII_TEP", "https://inheritancetaxexplained.co.uk/about-steve-hunt/"]},
        {"@type": "Article", "@id": PAGE_URL + "#article",
         "headline": "SSAS pension FAQ: every question answered",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#faq", "url": PAGE_URL, "inLanguage": "en-GB",
         "mainEntity": [{"@type": "Question", "name": q["q"],
                         "acceptedAnswer": {"@type": "Answer", "text": plain(" ".join(q["paras"]))}}
                        for q in qs]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS pension FAQ", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    out = []
    w = out.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w(f"<title>SSAS pension FAQ: {n} questions answered, with sources | My SSAS</title>")
    w(f'<meta name="description" content="{n} questions about SSAS pensions answered in plain English: what a SSAS is, who runs it, loanbacks, property, contributions, tax and death benefits, each with the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="SSAS pension FAQ: every question answered">')
    w(f'<meta property="og:description" content="{n} questions about SSAS pensions, answered in plain English with the law linked. By Steve Hunt ACII TEP.">')
    w(f'<meta property="og:url" content="{PAGE_URL}">')
    w('<script type="application/ld+json">')
    w(ld)
    w("</script>")
    w(style)
    w("</head>")
    w("<body>")
    w(header)
    w("")
    w("<main>")
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS pension FAQ</p>')
    w("  <h1>SSAS pension FAQ: every question answered</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {short}</p>")
    w("  </div>")
    w("")
    w('  <h2 id="the-questions">The questions</h2>')
    w('  <div class="toc">')
    for s in sections:
        w(f'    <h3><a href="#{s["id"]}">{html.escape(s["title"])}</a></h3>')
        w("    <ul>")
        for q in s["qs"]:
            w(f'      <li><a href="#{q["id"]}">{html.escape(q["q"], quote=False)}</a></li>')
        w("    </ul>")
    w("  </div>")
    for s in sections:
        w("")
        w(f'  <h2 id="{s["id"]}">{html.escape(s["title"])}</h2>')
        if s["note"]:
            w(f'  <p class="note">{html.escape(s["note"])}</p>')
        for q in s["qs"]:
            w(f'  <h3 id="{q["id"]}">{html.escape(q["q"], quote=False)}</h3>')
            for p in q["paras"]:
                w(f"  <p>{p}</p>")
            w("  " + src_line(q["srcs"]))
        w('  <p class="back"><a href="#the-questions">Back to the questions</a></p>')

    w("")
    w('  <div class="choice">')
    w("    <h2>Ask Steve a question about SSAS pensions</h2>")
    w("    <p>If your question is not here, you can ask Steve.</p>")
    w('    <a class="ask" href="/contact/">Ask Steve a question about SSAS pensions</a>')
    w("  </div>")

    # consolidated sources
    allsrc = OrderedDict((lbl, OrderedDict()) for lbl in LABEL_ORDER)
    for q in qs:
        for label, title, url in q["srcs"]:
            assert label in allsrc, f"unknown label {label}"
            if label == "Steve's analysis":
                continue
            allsrc[label].setdefault(url if label != "Law" else title, (title, url))
    w("")
    w('  <h2 id="sources">Sources and evidence</h2>')
    w('  <div class="srclist">')
    w("  <p>Every answer above links to its own sources. Here they are in one place, by type.</p>")
    for label, items in allsrc.items():
        if label == "Steve's analysis":
            w(f'  <h3 id="steves-analysis">Steve\'s analysis</h3>')
            w("  <ul><li>The flat fee and 1% comparison: 1% of £150,000 is £1,500. So a flat fee of £1,500 a year costs the same as a 1% yearly charge on a £150,000 pension, less on a bigger one and more on a smaller one. This is arithmetic, not a recommendation.</li></ul>")
            continue
        if not items:
            continue
        w(f"  <h3>{html.escape(label)}</h3>")
        w("  <ul>")
        for title, url in sorted(items.values(), key=lambda t: t[0]):
            w(f"    <li>{link(title, url)}</li>")
        w("  </ul>")
    w("  </div>")

    w("")
    w("  <h2>Who writes this site</h2>")
    w("  <p>Steve Hunt is a Chartered Insurance Risk Manager and an Associate of the Chartered Insurance Institute (ACII). He is also a Trust and Estate Practitioner (TEP), a full member of STEP. He has worked in UK financial services since 1980, in pensions, protection and estate planning.</p>")
    w('  <p>Every answer on this site links to the law or the HMRC guidance it relies on, so you can check it yourself. <a href="/about/">More about Steve</a></p>')
    w("</main>")
    w("")
    w(footer)
    w("</body>")
    w("</html>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(out) + "\n"
    assert "—" not in text and "–" not in text, "dash found"
    OUT.write_text(text, encoding="utf-8")
    print(f"built {OUT} with {n} questions in {len(sections)} sections, {len(text):,} bytes")


if __name__ == "__main__":
    main()
