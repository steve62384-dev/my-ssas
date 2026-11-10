#!/usr/bin/env python3
"""Build /ssas-contributions/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "ssas-contributions" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/ssas-contributions/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"
LEG = "https://www.legislation.gov.uk/ukpga/2004/12/section/"
PTM = "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/"

S = {
    "s188": ("Law", "Finance Act 2004, ss.188 and 189", LEG + "188"),
    "s190": ("Law", "Finance Act 2004, s.190", LEG + "190"),
    "s191": ("Law", "Finance Act 2004, ss.191 to 194", LEG + "191"),
    "s196": ("Law", "Finance Act 2004, ss.196 and 197", LEG + "196"),
    "cta54": ("Law", "Corporation Tax Act 2009, s.54", "https://www.legislation.gov.uk/ukpga/2009/4/section/54"),
    "s227": ("Law", "Finance Act 2004, s.227", LEG + "227"),
    "s228": ("Law", "Finance Act 2004, ss.228 and 228ZA", LEG + "228"),
    "s228a": ("Law", "Finance Act 2004, s.228A", LEG + "228A"),
    "s237a": ("Law", "Finance Act 2004, ss.237A to 237E", LEG + "237A"),
    "itepa308": ("Law", "Income Tax (Earnings and Pensions) Act 2003, s.308", "https://www.legislation.gov.uk/ukpga/2003/1/section/308"),
    "sscr": ("Law", "Social Security (Contributions) Regulations 2001, Sch 3, Part VI, para 2", "https://www.legislation.gov.uk/uksi/2001/1004/schedule/3/part/VI"),
    "nic2026": ("Law", "National Insurance Contributions (Employer Pensions Contributions) Act 2026, ss.1 to 3", "https://www.legislation.gov.uk/ukpga/2026/15/contents"),
    "ptm042100": ("HMRC", "PTM042100: paying contributions with assets", PTM + "ptm042100"),
    "ptm043200": ("HMRC", "PTM043200: tax relief for employers", PTM + "ptm043200"),
    "ptm043400": ("HMRC", "PTM043400: spreading", PTM + "ptm043400"),
    "ptm044100": ("HMRC", "PTM044100: tax relief for members, conditions", PTM + "ptm044100"),
    "ptm044210": ("HMRC", "PTM044210: methods of giving relief", PTM + "ptm044210"),
    "ptm044220": ("HMRC", "PTM044220: relief at source", PTM + "ptm044220"),
    "ptm055100": ("HMRC", "PTM055100: carry forward", PTM + "ptm055100"),
    "ptm056110": ("HMRC", "PTM056110: rate of the annual allowance charge", PTM + "ptm056110"),
    "ptm056410": ("HMRC", "PTM056410: scheme pays", PTM + "ptm056410"),
    "ptm056510": ("HMRC", "PTM056510: money purchase annual allowance", PTM + "ptm056510"),
    "ptm057100": ("HMRC", "PTM057100: tapered annual allowance", PTM + "ptm057100"),
    "bim46035": ("HMRC", "BIM46035: company pension contributions", "https://www.gov.uk/hmrc-internal-manuals/business-income-manual/bim46035"),
    "eim01570": ("HMRC", "EIM01570: employer's contributions", "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim01570"),
    "nim02716": ("HMRC", "NIM02716: employer's payments into registered pension schemes", "https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim02716"),
    "nim13130": ("HMRC", "NIM13130: Class 1A on benefits for family or household members", "https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim13130"),
    "aa": ("GOV.UK", "Tax on your private pension contributions: annual allowance", "https://www.gov.uk/tax-on-your-private-pension/annual-allowance"),
    "rates": ("GOV.UK", "Rates and allowances: pension schemes", "https://www.gov.uk/government/publications/rates-and-allowances-pension-schemes/pension-schemes-rates"),
    "example": ("Steve's analysis", "The worked example", "#worked-example"),
}
LABEL_ORDER = ["Law", "HMRC", "GOV.UK", "Steve's analysis"]

SHORT = ("your company and you can both pay in. For most people the annual allowance is £60,000 a year, across all "
         "their pensions. You may be able to add allowance you did not use in the last 3 tax years. Your company "
         "normally gets Corporation Tax relief on what it pays, and its payments are not limited by your salary. You "
         "get tax relief on your own payments up to your UK earnings for the year. If more than your allowance goes "
         "in, a tax charge normally applies.")
SHORT_SRC = ["aa", "rates", "s228a", "ptm043200", "ptm044100"]

SECTIONS = [
    ("Your company's payments", "company", [
        ("No salary limit", "Your company, the sponsoring employer, can pay in for you. Its payments are not limited by your salary. They are not taxed as your pay, and there is no National Insurance on them. A 2026 Act lets the government charge National Insurance on salary or bonus given up for pension payments (salary sacrifice), above a yearly limit. The first limit must be £2,000. This is due to start on 6 April 2029. Ordinary company payments, not made in exchange for salary or bonus, are not affected.",
         ["ptm044100", "itepa308", "eim01570", "sscr", "nim02716", "nic2026"]),
        ("Corporation Tax relief", "Your company can normally deduct its payments from its profits. It gets the relief for the accounting period in which it actually pays. Apart from the spreading rules below, the relief cannot be moved to another period. HMRC accepts the relief unless there is a non-business reason for the payment. HMRC looks at the whole pay package of a director, or of a relative or friend who works in the business. It can refuse relief if the package is more than an unconnected person would get for similar work.",
         ["s196", "cta54", "ptm043200", "bim46035"]),
        ("Spreading very large payments", "Very large increases can be spread. This happens if this period's payments are more than 2.1 times the last period's. HMRC then works out the excess over 1.1 times the last period's payments. If that excess is £500,000 or more, the relief on it is spread over 2, 3 or 4 years.",
         ["s196", "ptm043400"]),
    ]),
    ("Your own payments", "your-payments", [
        ("How much gets tax relief", "You get tax relief on your own payments up to your UK earnings for the year, such as salary or self-employed profits. Dividends do not count. You must also be a relevant UK individual, for example UK resident at some time in the tax year. If you earn less than £3,600, you can still get tax relief on payments of up to £3,600 a year, including the relief. But this only works if your SSAS uses relief at source. There is no tax relief on your payments once you are 75.",
         ["s188", "s190", "s191", "ptm044100", "ptm044220"]),
        ("How the relief is given", "There are three ways: relief at source, net pay through the payroll, or a claim to HMRC. You cannot choose: it depends on what your SSAS is allowed to operate. With relief at source, the SSAS claims tax relief from HMRC and adds it to your pension. If you are due more relief, for example as a higher rate taxpayer, you claim the extra from HMRC, often through your tax return.",
         ["s191", "ptm044210", "ptm044220"]),
        ("Payments by someone else", "Someone else, such as a relative, can pay in for you. Their payment is treated as yours for tax relief, within the same limits.",
         ["s188", "ptm044100"]),
    ]),
    ("The annual allowance", "annual-allowance", [
        ("£60,000 a year", "For most people the annual allowance is £60,000 a year, across all their pensions. For a money purchase SSAS, it counts all the contributions paid in for you during the tax year, including any tax relief added. That includes payments by you, your company and anyone else. The tax year runs from 6 April to 5 April. Money moved in from another pension (a transfer) is not a contribution.",
         ["s228", "aa", "rates"]),
        ("Carry forward", "You can add annual allowance you did not use in the last 3 tax years. You must have been a member of a registered pension scheme at some time in each of those years. It does not matter if nothing was paid in. This year's allowance is used first, then the spare allowance from the oldest year.",
         ["s228a", "ptm055100"]),
        ("Lower allowances", "The allowance is lower if your threshold income is over £200,000 and your adjusted income is over £260,000. It never goes below £10,000. It is also £10,000 for money purchase savings once you trigger the money purchase annual allowance. One way to trigger it is to take taxable income from a pension pot flexibly. Not every withdrawal triggers it. Carry forward cannot be added to that £10,000.",
         ["s228", "ptm057100", "ptm056510", "rates"]),
        ("If too much goes in", "If more goes in than your allowance, including any carry forward, you may have a tax charge. The excess is added on top of your taxable income, so parts of it can be taxed at different rates. You report the charge on your self assessment tax return. You have the right to ask the scheme to pay the charge from your pension if two things are true. The charge is over £2,000, and more than the standard allowance went into that scheme alone. Some schemes will also pay it in other cases.",
         ["s227", "s237a", "ptm056110", "ptm056410"]),
    ]),
]

EXAMPLE_ROWS = [
    ("This tax year's allowance (2026/27)", "£60,000"),
    ("Unused from 2023/24", "£60,000"),
    ("Unused from 2024/25", "£60,000"),
    ("Unused from 2025/26", "£60,000"),
    ("Total that can go in without a charge", "£240,000"),
]

STEPS = [
    "Work out your annual allowance for this tax year, including any carry forward and any lower allowance.",
    "Decide who pays: your company, you, someone else, or a mix.",
    "Pay money, not assets, into the SSAS's bank account.",
    "Watch the dates. The annual allowance counts what is paid in the tax year. Your company gets relief for the accounting period in which it pays.",
    "If you pay in yourself, check how your SSAS gives tax relief, and claim any extra relief you are due from HMRC.",
]
STEPS_SRC = ["s228a", "ptm042100", "s196", "aa", "ptm044210"]

QA = [
    ("Can my company pay in if I take a small salary?",
     "Yes. Your company's payments are not limited by your salary. The limits that matter are the annual allowance and HMRC's business test for Corporation Tax relief.",
     ["ptm044100", "ptm043200", "bim46035", "aa"]),
    ("Do dividends count for tax relief on my own payments?",
     "No. Only earnings such as salary or self-employed profits count. Dividends do not.",
     ["s188", "ptm044100"]),
    ("Can my company pay in property or shares instead of cash?",
     "Not normally as a contribution that gets tax relief. But HMRC does accept one route. Your company first agrees to pay a set cash sum. It then sells an asset to the SSAS at market value, and the two amounts are set off. Each step must be agreed, and recorded at the time. If the asset is worth less than the cash sum, the rest must be paid in cash.",
     ["ptm042100"]),
    ("Can I pay in after 75?",
     "Yes, but you get no tax relief on your own payments once you are 75.",
     ["s188", "ptm044100"]),
    ("Can my company pay in for family members?",
     "If they work for the company, yes, as part of their pay package. HMRC can refuse the company's relief if their total pay, including the pension, is more than their work justifies. If they do not work for the company, and the company pays because of your job, the payment is normally taxed on you. The company normally pays Class 1A National Insurance on it too.",
     ["bim46035", "eim01570", "nim13130"]),
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


EXAMPLE_SRC = ["example", "s228a", "ptm055100", "s196", "ptm043400", "bim46035"]


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  p.src { font-size: 14px; color: var(--muted); margin: 6px 0 0; word-break: break-word; }
  p.src .lead { font-weight: 700; margin-right: 4px; }
  p.src .lbl { font-weight: 600; }
  table.ex { min-width: 0; max-width: 520px; }
  table.ex td.num { text-align: right; white-space: nowrap; font-weight: 600; }
  table.ex td:first-child { font-weight: 400; }
  table.ex tr.total td { font-weight: 700; }
  ol.how li { margin-bottom: 8px; }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    groups = [SHORT_SRC] + [k for _, _, items in SECTIONS for (_, _, k) in items] + [EXAMPLE_SRC, STEPS_SRC] + [q[2] for q in QA]
    for keys in groups:
        for k in keys:
            if k not in used:
                used.append(k)

    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/",
         "sameAs": ["https://www.linkedin.com/in/steve~hunt", "https://www.youtube.com/@SteveHuntACIITEP",
                    "https://x.com/SHunt_ACII_TEP", "https://inheritancetaxexplained.co.uk/about-steve-hunt/"]},
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "How much can I pay into my SSAS?",
         "description": "SSAS contributions: who can pay in, the £60,000 annual allowance, carry forward, tax relief for you and your company, spreading, and a worked example.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS contributions", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>SSAS contributions: how much can go in, and the tax relief | My SSAS</title>")
    w('<meta name="description" content="How much can I pay into my SSAS? Who can pay in, the £60,000 annual allowance, carry forward, tax relief for you and your company, with a worked example and the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="How much can I pay into my SSAS?">')
    w('<meta property="og:description" content="SSAS contributions in plain English, with a worked example and the law linked. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS contributions</p>')
    w("  <h1>How much can I pay into my SSAS?</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {SHORT}</p>")
    w("    " + src_line(SHORT_SRC))
    w("  </div>")
    for title, sid, items in SECTIONS:
        w("")
        w(f'  <h2 id="{sid}">{html.escape(title)}</h2>')
        for h3, text, keys in items:
            w(f"  <h3>{html.escape(h3)}</h3>")
            w(f"  <p>{html.escape(text, quote=False)}</p>")
            w("  " + src_line(keys))
    w("")
    w('  <h2 id="worked-example">A worked example</h2>')
    w("  <p>Jane is a director of her own company. She was a member of a registered pension scheme in each of the last 3 tax years. But nothing was paid into any pension for her in those years, by anyone. Her income is under the taper limits, and she has not triggered the money purchase annual allowance.</p>")
    w('  <div class="tablewrap">')
    w('    <table class="ex">')
    w("      <tbody>")
    for i, (item, amount) in enumerate(EXAMPLE_ROWS):
        cls = ' class="total"' if i == len(EXAMPLE_ROWS) - 1 else ""
        w(f'        <tr{cls}><td>{html.escape(item)}</td><td class="num">{amount}</td></tr>')
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    w("  <p>Her company pays £240,000 into the SSAS for her before 5 April 2027. If HMRC accepts the payment is for the business, the company gets relief for the accounting period in which it pays. That cuts its taxable profit by £240,000, so it pays less Corporation Tax. HMRC looks at her whole pay package, and its history. Spreading does not apply, because the excess is under £500,000.</p>")
    w("  " + src_line(EXAMPLE_SRC))
    w("")
    w('  <h2 id="steps">Before you pay in</h2>')
    w('  <ol class="how">')
    for st in STEPS:
        w(f"    <li>{html.escape(st, quote=False)}</li>")
    w("  </ol>")
    w("  " + src_line(STEPS_SRC))
    w("")
    w('  <h2 id="questions">Common questions</h2>')
    for q, a, keys in QA:
        w(f"  <h3>{html.escape(q, quote=False)}</h3>")
        w(f"  <p>{html.escape(a, quote=False)}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <div class="choice">')
    w("    <h2>A question about paying into a SSAS?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read <a href="/how-to-set-up-a-ssas/">how to set up a SSAS</a>, about <a href="/ssas-commercial-property/">SSAS commercial property</a>, or the <a href="/faq/">SSAS pension FAQ</a>.</p>')
    w('    <a class="ask" href="/contact/">Ask Steve a question about SSAS pensions</a>')
    w("  </div>")
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
                w("    <li>The worked example: our own arithmetic, using the £60,000 annual allowance for each of the four tax years and the carry forward rules, with Jane's pension input amount nil in each of the 3 earlier years. Jane is made up for the example. It is an illustration, not a recommendation.</li>")
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
