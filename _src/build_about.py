#!/usr/bin/env python3
"""Build /about/index.html for my-ssas.co.uk (template parts copied from the home page).

Facts come from Steve's approved About page on inheritancetaxexplained.co.uk (4 October 2026),
the fee page's Highstone disclosure, and Steve's own quote on the who-runs and SSAS or SIPP pages.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "about" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/about/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

CII_TITLES = "https://www.cii.co.uk/about-us/professional-standards/using-cii-designations-and-titles/"
CIRM_REG = "https://www.regulated-professions.service.gov.uk/professions/chartered-insurance-risk-manager"
STEP_URL = "https://www.step.org/"
LINKEDIN = "https://www.linkedin.com/in/steve~hunt"
YOUTUBE = "https://www.youtube.com/@SteveHuntACIITEP"
XURL = "https://x.com/SHunt_ACII_TEP"
ITE = "https://inheritancetaxexplained.co.uk/"
ITE_ABOUT = "https://inheritancetaxexplained.co.uk/about-steve-hunt/"

PAGES = [
    ("/", "What is a SSAS pension?", "the plain explanation, and the rules in one table"),
    ("/faq/", "SSAS pension FAQ", "60 questions, each answer with its sources"),
    (FEES, "SSAS provider fees compared, 2026", "yearly fees and initial costs from provider fee schedules, price pages and written confirmations"),
    ("/how-to-set-up-a-ssas/", "How to set up a SSAS", "the steps, how long it takes and what it costs"),
    ("/ssas-loanback/", "SSAS loanback rules", "lending to your company, with a worked example"),
    ("/who-runs-a-ssas/", "Who runs a SSAS", "trustees, the scheme administrator and the regulators"),
    ("/ssas-vs-sipp/", "SSAS or SIPP", "the differences, and moving between them"),
    ("/ssas-commercial-property/", "SSAS commercial property", "buying your business premises, with a worked example"),
    ("/ssas-contributions/", "SSAS contributions", "how much can go in, and the tax relief"),
    ("/ssas-disadvantages/", "SSAS disadvantages", "the honest list"),
    ("/take-the-ssas-test/", "The SSAS Test", "three quick questions, sent to Steve"),
]


def a(url, text, ext=False, rel=None):
    t = html.escape(text, quote=False)
    attrs = f'href="{html.escape(url)}"'
    if ext:
        attrs += ' target="_blank" rel="noopener"'
    elif rel:
        attrs += f' rel="{rel}"'
    return f"<a {attrs}>{t}</a>"


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  ul.plain { padding-left: 20px; }
  ul.plain li { margin-bottom: 8px; }
  blockquote.view { margin: 12px 0; padding: 12px 16px; border-left: 4px solid var(--teal, #0f7c84); background: var(--soft); font-size: 18px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    cii = {"@type": "Organization", "name": "The Chartered Insurance Institute", "url": "https://www.cii.co.uk/"}
    step = {"@type": "Organization", "name": "STEP, the Society of Trust and Estate Practitioners", "url": STEP_URL}
    person = {
        "@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
        "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP",
        "jobTitle": "UK financial services professional",
        "description": "UK financial services professional since 1980. Chartered Insurance Risk Manager, Associate of the Chartered Insurance Institute (ACII) and Trust and Estate Practitioner (TEP). Explains SSAS pensions in plain English, with the law behind every answer.",
        "url": PAGE_URL, "mainEntityOfPage": PAGE_URL,
        "sameAs": [LINKEDIN, YOUTUBE, XURL, ITE_ABOUT],
        "knowsAbout": ["Small self-administered schemes (SSAS)", "Occupational pension schemes", "Pensions tax",
                       "Pension scheme loans to employers", "Commercial property in pension schemes",
                       "Inheritance tax", "Trusts and estate planning"],
        "memberOf": [cii, step],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "ACII, Associate of the Chartered Insurance Institute",
             "credentialCategory": "Professional membership", "recognizedBy": cii},
            {"@type": "EducationalOccupationalCredential", "name": "Chartered Insurance Risk Manager",
             "credentialCategory": "Chartered title", "recognizedBy": cii},
            {"@type": "EducationalOccupationalCredential", "name": "TEP, Trust and Estate Practitioner (STEP)",
             "credentialCategory": "Professional membership", "recognizedBy": step},
        ],
    }
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        person,
        {"@type": "ProfilePage", "@id": PAGE_URL + "#profile", "url": PAGE_URL, "name": "About Steve Hunt ACII TEP",
         "mainEntity": {"@id": SITE + "/#steve-hunt"}, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "About Steve", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>About Steve Hunt ACII TEP | My SSAS</title>")
    w('<meta name="description" content="Who writes My SSAS, and how it is checked. Steve Hunt is a Chartered Insurance Risk Manager, ACII and TEP, in UK financial services since 1980.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="profile">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="About Steve Hunt ACII TEP">')
    w('<meta property="og:description" content="Who writes My SSAS, and how every answer is backed up.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; About Steve</p>')
    w("  <h1>Steve Hunt ACII TEP</h1>")
    w(f'  <p class="byline">Who writes this site, and how it is checked &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w("    <p>Steve Hunt is a Chartered Insurance Risk Manager, an Associate of the Chartered Insurance Institute (ACII), and a Trust and Estate Practitioner (TEP), a full member of STEP. He has worked in UK financial services since 1980, in pensions, protection and estate planning. On this site he explains SSAS pensions in plain English, with the law behind every answer.</p>")
    w("  </div>")
    w("")
    w('  <h2 id="qualifications">Qualifications</h2>')
    w('  <ul class="plain">')
    w(f"    <li><strong>ACII:</strong> Associate of the Chartered Insurance Institute, the professional body for the insurance and financial planning profession. {a(CII_TITLES, "The Institute's designations and titles", ext=True)}.</li>")
    w(f"    <li><strong>Chartered Insurance Risk Manager:</strong> a chartered title awarded by the Chartered Insurance Institute to qualified members. {a(CIRM_REG, 'The title on the GOV.UK register of regulated professions', ext=True)}.</li>")
    w(f"    <li><strong>TEP:</strong> Trust and Estate Practitioner. Only full members of STEP, the Society of Trust and Estate Practitioners, can use these letters. {a(STEP_URL, 'STEP', ext=True)}.</li>")
    w("  </ul>")
    w("")
    w('  <h2 id="experience">Experience</h2>')
    w("  <p>Steve began his career at MGM Assurance in 1980. He has worked in UK financial services ever since, in pensions, protection and estate planning.</p>")
    w("")
    w('  <h2 id="view">Steve\'s view of a SSAS</h2>')
    w('  <blockquote class="view">&ldquo;It is Self-Invested with a capital S and a capital I.&rdquo;</blockquote>')
    w('  <p>His full explanation, and why a SSAS is so different from a SIPP, is on the <a href="/ssas-vs-sipp/">SSAS or SIPP</a> page.</p>')
    w("")
    w('  <h2 id="covers">What this site covers</h2>')
    w('  <ul class="plain">')
    for url, title, desc in PAGES:
        w(f'    <li><a href="{html.escape(url)}">{html.escape(title)}</a>: {html.escape(desc)}</li>')
    w("  </ul>")
    w("")
    w('  <h2 id="checked">How the answers are backed up</h2>')
    w("  <p>Every answer gives its sources, each labelled by the kind of authority it carries: the law, HMRC's published guidance, The Pensions Regulator or another official body, dated provider evidence, or Steve's own analysis. Where an answer is Steve's own arithmetic or reasoning, it is labelled Steve's analysis. Each page shows the date it was last checked.</p>")
    w('  <p>If you spot something that is wrong or out of date, please <a href="/contact/">tell Steve</a>, and it will be corrected.</p>')
    w("")
    w('  <h2 id="links">Steve\'s links with firms</h2>')
    w(f'  <p>Steve currently refers SSAS clients to Highstone, run by Paul Davies. If you go ahead with a SSAS provider Steve introduces you to, the provider may pay Steve a fee. Steve and Paul do refer clients to each other. No provider pays to be listed on this site. The <a href="{FEES}">fee comparison</a> explains how the providers are compared.</p>')
    w("  <p>This site gives general information only. It is not advice or a personal recommendation. If you ask Steve a question, your details go to another firm only if you agree.</p>")
    w("")
    w('  <h2 id="elsewhere">Elsewhere</h2>')
    w('  <ul class="plain">')
    w(f"    <li>{a(LINKEDIN, 'Steve Hunt on LinkedIn', rel='me')}</li>")
    w(f"    <li>{a(YOUTUBE, 'Steve Hunt ACII TEP on YouTube', rel='me')}</li>")
    w(f"    <li>{a(XURL, 'Steve Hunt ACII TEP on X', rel='me')}</li>")
    w(f"    <li>{a(ITE, 'Inheritance Tax Explained', rel='me')}: Steve's other site, on inheritance tax, pensions and trusts</li>")
    w("  </ul>")
    w("")
    w('  <div class="choice">')
    w("    <h2>Ask Steve a question</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. Or call Steve on <a href="tel:+441733602071">01733 602 071</a>, or email <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a>.</p>')
    w('    <a class="ask" href="/contact/">Ask Steve a question about SSAS pensions</a>')
    w("  </div>")
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
