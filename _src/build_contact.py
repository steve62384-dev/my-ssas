#!/usr/bin/env python3
"""Build /contact/index.html for my-ssas.co.uk (template parts and form copied from the home page)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "contact" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/contact/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  ul.plain { padding-left: 20px; }
  ul.plain li { margin-bottom: 8px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
    form = re.search(r'  <form class="enquiry".*?</form>', home, re.S).group(0)
    assert "Formspree and our email providers" in form, "home form must carry the privacy note inside it"
    form = form.replace("New enquiry from my-ssas.co.uk (home page)", "New enquiry from my-ssas.co.uk (contact page)")
    form = form.replace('name="page" value="Home page"', 'name="page" value="Contact page"')
    assert "(contact page)" in form and 'value="Contact page"' in form

    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/",
         "sameAs": ["https://www.linkedin.com/in/steve~hunt", "https://www.youtube.com/@SteveHuntACIITEP",
                    "https://x.com/SHunt_ACII_TEP", "https://inheritancetaxexplained.co.uk/about-steve-hunt/"],
         "contactPoint": {"@type": "ContactPoint", "contactType": "enquiries", "telephone": "+44 1733 602071",
                          "email": "steve@my-ssas.co.uk", "areaServed": "GB", "availableLanguage": "en-GB"}},
        {"@type": "ContactPage", "@id": PAGE_URL + "#contact", "url": PAGE_URL,
         "name": "Ask Steve a question about SSAS pensions", "mainEntity": {"@id": SITE + "/#steve-hunt"},
         "dateModified": CHECKED_ISO, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Ask Steve", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>Ask Steve a question about SSAS pensions | My SSAS</title>")
    w('<meta name="description" content="Ask Steve Hunt ACII TEP a question about SSAS pensions. Use the form, call 01733 602 071 or email steve@my-ssas.co.uk.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="website">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="Ask Steve a question about SSAS pensions">')
    w('<meta property="og:description" content="Ask Steve Hunt ACII TEP a question about SSAS pensions.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; Ask Steve</p>')
    w("  <h1>Ask Steve a question about SSAS pensions</h1>")
    w(f'  <p class="byline">Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w("    <p>Send your question using the form. It goes to Steve, who will get back to you. This site gives general information only. It is not advice or a personal recommendation.</p>")
    w("  </div>")
    w("")
    w('  <h2 id="ask">Your question</h2>')
    w("  <!-- Formspree form \"My SSAS website enquiries\" (Steve's account, set up 6 October 2026). -->")
    w(form)
    w("")
    w('  <h2 id="other-ways">Other ways to reach Steve</h2>')
    w('  <ul class="plain">')
    w('    <li>Phone: <a href="tel:+441733602071">01733 602 071</a></li>')
    w('    <li>Email: <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a></li>')
    w("    <li>Post: Steve Hunt ACII TEP, Stable Cottage, Water Lane, South Witham, Grantham, Lincolnshire NG33 5PH</li>")
    w("  </ul>")
    w("")
    w('  <h2 id="next">What happens next</h2>')
    w("  <p>Steve will get back to you by email or phone. If your question needs advice or another service that this site does not provide, Steve may explain what kind of firm you would need. Your details go to another firm only if you agree.</p>")
    w("")
    w('  <h2 id="read-first">Want to read first?</h2>')
    w('  <ul class="plain">')
    w('    <li><a href="/faq/">SSAS pension FAQ</a>: 60 questions, each answer with its sources</li>')
    w('    <li><a href="/take-the-ssas-test/">The SSAS Test</a>: three quick questions, sent to Steve</li>')
    w(f'    <li><a href="{FEES}">SSAS provider fees compared, 2026</a></li>')
    w('    <li><a href="/about/">About Steve</a>: who writes this site, and how it is checked</li>')
    w("  </ul>")
    w("</main>")
    w("")
    w(footer)
    w("</body>")
    w("</html>")
    text = "\n".join(o) + "\n"
    assert "—" not in text and "–" not in text
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"built {OUT}, {len(text):,} chars")


if __name__ == "__main__":
    main()
