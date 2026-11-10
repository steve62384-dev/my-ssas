#!/usr/bin/env python3
"""Build the site-wide extras: /sources-and-corrections/, 404.html, robots.txt, sitemap.xml and llms.txt.

Run this last, after every page builder, because the sitemap and llms.txt are read from the built pages.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
SITE = "https://my-ssas.co.uk"
UPDATED = "10 November 2026"
UPDATED_ISO = "2026-11-10"
PDF_PATH = "/wp-content/uploads/2022/11/SSAS-pension-administrator-fees-based-on-My-SSAS-co-uk-research-at-November-2022-.pdf"

LABELS = [
    ("Law", "Acts of Parliament and regulations, linked to the official text on legislation.gov.uk."),
    ("HMRC", "HMRC&rsquo;s manuals and guidance on GOV.UK: HMRC&rsquo;s published view of how it applies the tax law. It is guidance, not law."),
    ("TPR, FCA, PRA, FSCS, ICO, DWP, HM Treasury, Bank of England, Ombudsman", "what the regulators, government departments and other official bodies publish."),
    ("GOV.UK", "other government guidance, such as rate tables."),
    ("MoneyHelper", "the free guidance service backed by the government."),
    ("Provider evidence", "fee sheets, published terms and written confirmations from providers, with the date they were checked."),
    ("Administrators", "reports from the administrators of a firm that has gone into administration."),
    ("Published source", "figures credited to the publication that reported them."),
    ("Steve&rsquo;s analysis", "Steve&rsquo;s own arithmetic or reasoning, such as a worked example."),
    ("Steve&rsquo;s view", "Steve&rsquo;s own opinion, in his own words."),
    ("This site", "another page on this site that gives the detail."),
]

CHANGES_5_OCT = [
    "The FAQ was rewritten from scratch: 60 questions, each answer with its sources.",
    "The provider fee comparison was refreshed against the latest fee sheets, price pages and written provider confirmations. The table shows where each figure comes from. It shows each provider's yearly fee and initial costs separately, lowest yearly fee first. The PDF at the old November 2022 address now holds the 2026 table.",
    "New guides: how to set up a SSAS, loanbacks, who runs a SSAS, SSAS or SIPP, commercial property, contributions, and the disadvantages.",
    "The SSAS Test was rebuilt. It now sends its answers to Steve, and it no longer says whether a business qualifies.",
    "New About, Contact, Privacy policy and Cookie policy pages.",
    "The 2022 blog posts gained a dated notice at the top and dated notes on what has changed. The November 2022 post on final salary compensation claims was withdrawn.",
]

CHANGES_10_NOV = [
    "The provider fee comparison now uses Highstone's October 2026 fee sheet. Its fees, and Mattioli Woods' property and loan fees, were checked again on 10 November 2026.",
    "The About page and the fee comparison now say that a SSAS provider Steve introduces you to may pay him a fee.",
]

# Order and grouping for llms.txt (descriptions are read from each page's meta description).
LLMS_GROUPS = [
    ("Guides", ["/", "/faq/", "/ssas-pension-table-showing-best-ssas-providers/", "/how-to-set-up-a-ssas/", "/ssas-loanback/",
                "/who-runs-a-ssas/", "/ssas-vs-sipp/", "/ssas-commercial-property/", "/ssas-contributions/",
                "/ssas-disadvantages/", "/take-the-ssas-test/"]),
    ("About, method and policies", ["/about/", "/sources-and-corrections/", "/contact/", "/privacy-policy/", "/cookie-policy/"]),
    ("Archive", ["/blog/"]),
]


def parts():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  ul.plain { padding-left: 20px; }
  ul.plain li { margin-bottom: 8px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
    return style, header, footer


def write_page(out, title, description, ld_graph, body, noindex=False, canonical=None):
    style, header, footer = parts()
    o = ["<!doctype html>", '<html lang="en-GB">', "<head>", '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f"<title>{title}</title>", f'<meta name="description" content="{html.escape(description)}">']
    if noindex:
        o.append('<meta name="robots" content="noindex">')
    if canonical:
        o.append(f'<link rel="canonical" href="{canonical}">')
    if ld_graph:
        o += ['<script type="application/ld+json">',
              json.dumps({"@context": "https://schema.org", "@graph": ld_graph}, ensure_ascii=False, indent=1), "</script>"]
    o += [style, "</head>", "<body>", header, "", "<main>"] + body + ["</main>", "", footer, "</body>", "</html>"]
    text = "\n".join(o) + "\n"
    assert "—" not in text and "–" not in text, out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print("built", out.relative_to(ROOT))


def build_sources_page():
    path = "/sources-and-corrections/"
    url = SITE + path
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS",
         "publishingPrinciples": url, "inLanguage": "en-GB", "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/"},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": "Sources, method and corrections",
         "dateModified": UPDATED_ISO, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"},
         "author": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Sources, method and corrections", "item": url}]},
    ]
    b = ['  <p class="crumbs"><a href="/">Home</a> &rsaquo; Sources, method and corrections</p>',
         "  <h1>Sources, method and corrections</h1>",
         f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last updated {UPDATED}</p>',
         '  <div class="answer">',
         "    <p>Every page on this site is by Steve Hunt ACII TEP, who has worked in UK financial services since 1980. This page explains where the answers come from, how they are backed up, and what has been corrected.</p>",
         "  </div>",
         "",
         '  <h2 id="backed-up">How each answer is backed up</h2>',
         "  <p>Beside each answer is a Sources line, and most pages end with a full list of their sources. Every source carries a label, so you can see what kind of authority stands behind each statement:</p>",
         '  <ul class="plain">']
    for label, text in LABELS:
        b.append(f"    <li><strong>{label}:</strong> {text}</li>")
    b += ["  </ul>",
          "  <p>Where the law is clear, it comes first, linked to the official text.</p>",
          "",
          '  <h2 id="dates">Dates</h2>',
          "  <p>Each page shows the date it was last checked. That date changes only when the page has actually been reviewed. Tax rules change, so always check the date.</p>",
          "",
          '  <h2 id="blog">Steve&rsquo;s 2022 blog posts</h2>',
          '  <p>Steve&rsquo;s <a href="/blog/">blog posts</a> from 2022 are kept substantially as he wrote them, with typing errors corrected. Each one starts with a notice that it is an archived opinion piece, and ends with dated notes on what has changed since, with sources. Where the old wording could now mislead, a dated 2026 note sits beside it. One 2022 post was withdrawn.</p>',
          "",
          '  <h2 id="corrections">Corrections and updates</h2>',
          "  <h3>5 and 6 October 2026</h3>",
          "  <p>The site was rebuilt. Every page apart from the 2022 blog posts was written afresh, with a source for every answer.</p>",
          '  <ul class="plain">']
    for c in CHANGES_5_OCT:
        b.append(f"    <li>{c}</li>")
    b += ["  </ul>",
          "  <h3>10 November 2026</h3>",
          '  <ul class="plain">']
    for c in CHANGES_10_NOV:
        b.append(f"    <li>{c}</li>")
    b += ["  </ul>",
          "",
          '  <h2 id="mistake">Spotted a mistake?</h2>',
          '  <p>Please tell Steve, using the <a href="/contact/">contact form</a>, or email <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a>. Corrections are dated and listed on this page.</p>']
    write_page(ROOT / "sources-and-corrections" / "index.html", "Sources, method and corrections | My SSAS",
               "How every answer on My SSAS is backed up: the source labels, the dates, the 2022 blog posts, and a dated list of corrections.",
               graph, b, canonical=url)


def build_404():
    b = ["  <h1>Page not found</h1>",
         '  <div class="answer">',
         "    <p>Sorry, there is no page at this address. It may have moved when the site was rebuilt in October 2026.</p>",
         "  </div>",
         "  <p>Try one of these:</p>",
         '  <ul class="plain">',
         '    <li><a href="/">What is a SSAS pension?</a></li>',
         '    <li><a href="/faq/">SSAS pension FAQ</a>: 60 questions, each answer with its sources</li>',
         '    <li><a href="/ssas-pension-table-showing-best-ssas-providers/">SSAS provider fees compared, 2026</a></li>',
         '    <li><a href="/take-the-ssas-test/">The SSAS Test</a></li>',
         '    <li><a href="/blog/">Blog</a></li>',
         '    <li><a href="/contact/">Ask Steve a question about SSAS pensions</a></li>',
         "  </ul>"]
    write_page(ROOT / "404.html", "Page not found | My SSAS", "This page could not be found.", None, b, noindex=True)


def indexable_pages():
    pages = []
    for f in sorted(ROOT.rglob("index.html")):
        rel = f.relative_to(ROOT)
        if rel.parts[0].startswith("_"):
            continue
        t = f.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="noindex', t):
            continue
        path = "/" + "/".join(rel.parts[:-1]) + ("/" if len(rel.parts) > 1 else "")
        title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1)).replace(" | My SSAS", "").strip()
        desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))
        pages.append((path, title, desc))
    return pages


def build_sitemap(pages):
    order = {p: i for i, p in enumerate(["/", "/faq/", "/ssas-pension-table-showing-best-ssas-providers/"])}
    pages = sorted(pages, key=lambda x: (order.get(x[0], 9), x[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, _, _ in pages:
        lines.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{UPDATED_ISO}</lastmod></url>")
    lines.append(f"  <url><loc>{SITE}{PDF_PATH}</loc><lastmod>{UPDATED_ISO}</lastmod></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("built sitemap.xml with", len(pages) + 1, "addresses")


def build_robots():
    text = ("# My SSAS, by Steve Hunt ACII TEP.\n"
            "# Everything on this site is public information. All crawlers are welcome, including AI assistants.\n"
            "User-agent: *\n"
            "Allow: /\n\n"
            f"Sitemap: {SITE}/sitemap.xml\n")
    (ROOT / "robots.txt").write_text(text, encoding="utf-8")
    print("built robots.txt")


def build_llms(pages):
    info = {p: (t, d) for p, t, d in pages}
    o = ["# My SSAS", "",
         "> Plain English answers about SSAS pensions (small self-administered schemes) for UK business owners: what a SSAS is, how to set one up, loanbacks, commercial property, contributions, costs and the disadvantages. Every answer links to the law and HMRC guidance it relies on. By Steve Hunt ACII TEP. General information only, not advice.",
         "",
         "Author: Steve Hunt ACII TEP, Chartered Insurance Risk Manager and Trust and Estate Practitioner, in UK financial services since 1980.",
         f"About the author: {SITE}/about/",
         "LinkedIn: https://www.linkedin.com/in/steve~hunt",
         "YouTube: https://www.youtube.com/@SteveHuntACIITEP",
         "X: https://x.com/SHunt_ACII_TEP",
         "Steve's other site: https://inheritancetaxexplained.co.uk/",
         ""]
    for heading, paths in LLMS_GROUPS:
        o.append(f"## {heading}")
        o.append("")
        for p in paths:
            t, d = info[p]
            o.append(f"- [{t}]({SITE}{p}): {d}")
        o.append("")
    o += ["## Notes", "",
          f"- Every page shows the date it was last checked. This file was last updated on {UPDATED}.",
          "- Sources are labelled by the kind of authority they carry: Law, HMRC, the regulators, GOV.UK, provider evidence, or Steve's own analysis or view.",
          "- The 2022 blog posts are archived opinion pieces, kept with dated notes on what has changed.",
          "- For current rules, use the guides and the FAQ in preference to the archived 2022 blog posts. The archive keeps historical wording, and may contain figures or rules that have since changed.",
          "- The site does not give advice, and does not advise on pension transfers.", ""]
    text = "\n".join(o)
    assert "—" not in text and "–" not in text
    (ROOT / "llms.txt").write_text(text, encoding="utf-8")
    print("built llms.txt")


def main():
    build_sources_page()
    build_404()
    pages = indexable_pages()
    build_sitemap(pages)
    build_robots()
    build_llms(pages)


if __name__ == "__main__":
    main()
