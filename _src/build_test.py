#!/usr/bin/env python3
"""Build /take-the-ssas-test/index.html for my-ssas.co.uk (template parts copied from the home page).

The SSAS Test is three quick questions plus contact details, all inside one form,
so the answers reach Steve with the enquiry (the old site never sent them).
No eligibility verdicts and no invitation to transfer: each question just says why we ask.
"""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "take-the-ssas-test" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/take-the-ssas-test/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"
LEG = "https://www.legislation.gov.uk/ukpga/2004/12/section/"
PTM = "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/"

S = {
    "fa150": ("Law", "Finance Act 2004, s.150(5) and (6)", LEG + "150"),
    "fa153": ("Law", "Finance Act 2004, s.153(5)(h)", LEG + "153"),
    "ptm022000": ("HMRC", "PTM022000: types of pension scheme", PTM + "ptm022000"),
    "ptm032200": ("HMRC", "PTM032200: HMRC's decision", PTM + "ptm032200"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "analysis": ("Steve's analysis", "The flat fee and 1% comparison", "#q3"),
}
LABEL_ORDER = ["Law", "HMRC", "Provider evidence", "Steve's analysis"]

QUESTIONS = [
    ("q1", "1. What kind of business do you have?", "Business type", [
        "Private limited company (Ltd)",
        "Public limited company (PLC)",
        "Limited liability partnership (LLP)",
        "Sole trader or partnership",
        "Something else",
        "I do not have a business",
    ], "A SSAS is set up by an employer. For most people reading this, that is their own company. Any employer that sets up or joins the scheme is called a sponsoring employer.",
        ["fa150", "ptm022000"]),
    ("q2", "2. Has the business been trading for the last 12 months?", "Trading in the last 12 months", [
        "Yes, it has been trading",
        "It is less than a year old",
        "No, it has been dormant",
        "Not sure",
    ], "HMRC can refuse to register a new SSAS if a sponsoring company has been dormant. That means dormant for a whole month in a row, in the year before HMRC decides.",
        ["fa153", "ptm032200"]),
    ("q3", "3. Roughly how much is in your pensions now?", "Pensions now", [
        "Under £150,000",
        "£150,000 to £500,000",
        "Over £500,000",
        "Not sure, or I would rather not say",
    ], "SSAS fees are flat, so they weigh more on a smaller pension. A flat fee of £1,500 a year costs less than a 1% yearly charge once a pension is above £150,000, and more below it. Some providers also set their own minimum size.",
        ["fees", "analysis"]),
]


def link(title, url):
    t = html.escape(title, quote=False)
    if url.startswith("http"):
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{t}</a>'
    return f'<a href="{html.escape(url)}">{t}</a>'


def src_line(keys):
    groups = OrderedDict()
    for k in keys:
        label, title, url = S[k]
        groups.setdefault(label, []).append(link(title, url))
    parts = [f'<span class="lbl">{html.escape(l)}:</span> ' + "; ".join(v) for l, v in groups.items()]
    return '<p class="src"><span class="lead">Sources</span> ' + " &middot; ".join(parts) + "</p>"


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  p.src { font-size: 14px; color: var(--muted); margin: 6px 0 0; word-break: break-word; }
  p.src .lead { font-weight: 700; margin-right: 4px; }
  p.src .lbl { font-weight: 600; }
  form.quiz { max-width: 620px; }
  form.quiz fieldset { border: 0; border-bottom: 1px solid var(--line); padding: 0 0 16px; margin: 0 0 16px; min-width: 0; }
  form.quiz fieldset:last-of-type { border-bottom: 0; margin-bottom: 4px; }
  form.quiz legend { font-weight: 700; font-size: 18px; line-height: 1.35; padding: 0; margin: 0 0 8px; }
  form.quiz label.opt { display: flex; align-items: center; gap: 10px; font-weight: 400; margin: 6px 0; cursor: pointer; }
  form.quiz label.opt input { width: auto; margin: 0; flex: none; }
  form.quiz p.why { font-size: 15px; margin: 10px 0 0; }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    for q in QUESTIONS:
        for k in q[5]:
            if k not in used:
                used.append(k)

    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/",
         "sameAs": ["https://www.linkedin.com/in/steve~hunt", "https://www.youtube.com/@SteveHuntACIITEP",
                    "https://x.com/SHunt_ACII_TEP", "https://inheritancetaxexplained.co.uk/about-steve-hunt/"]},
        {"@type": "WebPage", "@id": PAGE_URL + "#webpage", "url": PAGE_URL, "name": "The SSAS Test",
         "description": "Three quick questions about your business and your pensions, sent to Steve Hunt ACII TEP with your question.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "The SSAS Test", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>Take the SSAS Test | My SSAS</title>")
    w('<meta name="description" content="The SSAS Test: three quick questions about your business and your pensions. Each one says why we ask, with the rule behind it. Your answers go to Steve Hunt ACII TEP.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="website">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="Take the SSAS Test">')
    w('<meta property="og:description" content="Three quick questions about your business and your pensions. Your answers go to Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; The SSAS Test</p>')
    w("  <h1>The SSAS Test</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w("    <p>Three quick questions about your business and your pensions. Each one says why we ask, with the rule behind it. Then add your details, and your answers go to Steve, who will get back to you.</p>")
    w("    <p>The test does not tell you whether to set up a SSAS or move a pension. It is general information, not advice.</p>")
    w("  </div>")
    w("")
    w("  <!-- Formspree form \"My SSAS website enquiries\" (Steve's account, set up 6 October 2026). -->")
    w('  <form class="enquiry quiz" action="https://formspree.io/f/xqpeayje" method="POST">')
    for qid, legend, field, options, why, keys in QUESTIONS:
        w(f'    <fieldset id="{qid}">')
        w(f"      <legend>{html.escape(legend)}</legend>")
        for i, opt in enumerate(options):
            req = " required" if i == 0 else ""
            w(f'      <label class="opt"><input type="radio" name="{html.escape(field)}" value="{html.escape(opt)}"{req}> {html.escape(opt)}</label>')
        w(f'      <p class="why"><strong>Why we ask:</strong> {html.escape(why, quote=False)}</p>')
        w("      " + src_line(keys))
        w("    </fieldset>")
    w('    <fieldset id="details">')
    w("      <legend>4. Your details</legend>")
    w('      <label for="name">Your name</label>')
    w('      <input id="name" name="name" type="text" autocomplete="name" required>')
    w('      <label for="business_name">Business name</label>')
    w('      <input id="business_name" name="Business name" type="text" autocomplete="organization">')
    w('      <label for="email">Email address</label>')
    w('      <input id="email" name="email" type="email" autocomplete="email" required>')
    w('      <label for="phone">Phone number</label>')
    w('      <input id="phone" name="phone" type="tel" autocomplete="tel">')
    w('      <label for="best_time">Best time to call</label>')
    w('      <select id="best_time" name="best_time">')
    for t in ["Any time", "Morning", "Afternoon", "Evening"]:
        w(f"        <option>{t}</option>")
    w("      </select>")
    w('      <label for="question">Your question (optional)</label>')
    w('      <textarea id="question" name="question"></textarea>')
    w("    </fieldset>")
    w('    <input type="hidden" name="_subject" value="New SSAS Test from my-ssas.co.uk">')
    w('    <input type="hidden" name="page" value="The SSAS Test">')
    w('    <div class="hp" aria-hidden="true"><label for="gotcha">Leave this empty</label><input id="gotcha" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>')
    w('    <p class="note">Your answers and details go to Steve Hunt and Lisa Newmark, so Steve can answer you. Formspree and our email providers handle the form for us. We will not pass your details to another firm for advice or other services unless you agree. The <a href="/privacy-policy/">privacy policy</a> explains the legal basis, how your details are stored and kept, your rights, and any processing outside the UK.</p>')
    w('    <p><button class="ask" type="submit">Send my answers to Steve</button></p>')
    w("  </form>")
    w('  <p>Or call Steve on <a href="tel:+441733602071">01733 602 071</a>, or email <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a>.</p>')
    w('  <p>To read more first, see <a href="/how-to-set-up-a-ssas/">how to set up a SSAS</a>, <a href="/ssas-disadvantages/">the disadvantages</a>, or the <a href="/faq/">SSAS pension FAQ</a>.</p>')
    w("")
    w('  <h2 id="sources">Sources</h2>')
    w('  <div class="srclist">')
    for label in LABEL_ORDER:
        items = [S[k] for k in used if S[k][0] == label]
        if not items:
            continue
        w(f"  <h3>{html.escape(label)}</h3>")
        w("  <ul>")
        for _, title, url in items:
            if label == "Steve's analysis":
                w("    <li>The flat fee and 1% comparison: our own arithmetic. £1,500 is 1% of £150,000, so a £1,500 flat fee is cheaper than a 1% charge above that size and dearer below it. It is an illustration, not a recommendation.</li>")
            else:
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
    text = "\n".join(o) + "\n"
    assert "—" not in text and "–" not in text
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"built {OUT}, {len(text):,} chars, {len(used)} sources")


if __name__ == "__main__":
    main()
