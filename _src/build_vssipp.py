#!/usr/bin/env python3
"""Build /ssas-vs-sipp/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_src"))
from build_whoruns import STEVE  # Steve's words, Clara-checked, kept identical on both pages

HOME = ROOT / "index.html"
OUT = ROOT / "ssas-vs-sipp" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/ssas-vs-sipp/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

S = {
    "s150": ("Law", "Finance Act 2004, s.150(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/150"),
    "pa34": ("Law", "Pensions Act 1995, s.34(1)", "https://www.legislation.gov.uk/ukpga/1995/26/section/34"),
    "sch29a": ("Law", "Finance Act 2004, Sch 29A, paras 1 and 2", "https://www.legislation.gov.uk/ukpga/2004/12/schedule/29A"),
    "s182": ("Law", "Finance Act 2004, ss.182 to 185", "https://www.legislation.gov.uk/ukpga/2004/12/section/182"),
    "s196": ("Law", "Finance Act 2004, s.196", "https://www.legislation.gov.uk/ukpga/2004/12/section/196"),
    "s228": ("Law", "Finance Act 2004, s.228", "https://www.legislation.gov.uk/ukpga/2004/12/section/228"),
    "s150a": ("Law", "Inheritance Tax Act 1984, s.150A", "https://www.legislation.gov.uk/ukpga/1984/51/section/150A"),
    "s279": ("Law", "Finance Act 2004, ss.165 and 279", "https://www.legislation.gov.uk/ukpga/2004/12/section/279"),
    "sch29": ("Law", "Finance Act 2004, Sch 29", "https://www.legislation.gov.uk/ukpga/2004/12/schedule/29"),
    "s161": ("Law", "Finance Act 2004, s.161(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/161"),
    "s208": ("Law", "Finance Act 2004, ss.208 and 209", "https://www.legislation.gov.uk/ukpga/2004/12/section/208"),
    "ptm134200": ("HMRC", "PTM134200: who is liable for the unauthorised payments charge", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm134200"),
    "si1237": ("Law", "SI 2021/1237, regs 8 to 11", "https://www.legislation.gov.uk/uksi/2021/1237/contents"),
    "ptm123200": ("HMRC", "PTM123200: loans to sponsoring employers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123200"),
    "ptm123300": ("HMRC", "PTM123300: loans to members and connected parties", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123300"),
    "ptm124000": ("HMRC", "PTM124000: borrowing", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm124000"),
    "ptm100010": ("HMRC", "PTM100010: transfers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm100010"),
    "ptm121000": ("HMRC", "PTM121000: investments, essential principles", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm121000"),
    "tprabout": ("TPR", "About us", "https://www.thepensionsregulator.gov.uk/en/about-us"),
    "tprtransfer": ("TPR", "Dealing with transfer requests", "https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/administration-detailed-guidance/dealing-with-transfer-requests"),
    "tprtoolkit": ("TPR", "Trustee toolkit, tutorial 5: trustee liabilities and protections", "https://trusteetoolkit.thepensionsregulator.gov.uk/pluginfile.php/133/mod_data/content/2375/The%20trustees%20role%20-%20Tutorial%205%20Trustee%20liabilities%20and%20protections.pdf"),
    "fca1866": ("FCA", "Glossary: establishing, operating or winding up a personal pension scheme", "https://handbook.fca.org.uk/glossary/G1866"),
    "perg12": ("FCA", "PERG 12.2: personal pension schemes", "https://handbook.fca.org.uk/handbook/perg12/perg12s2"),
    "fcadd": ("FCA", "Dear CEO letter: due diligence for SIPP investments, 30 October 2018", "https://www.fca.org.uk/publication/dear-ceo-letters/dear-ceo-letter-due-diligence-requirements-for-self-invested-pension-plan-sipp-investments.pdf"),
    "fscs": ("FSCS", "Pensions", "https://www.fscs.org.uk/what-we-cover/pensions/"),
    "dwp": ("DWP", "Protecting pension savers: options assessment, 9 June 2026", "https://www.gov.uk/government/consultations/protecting-pension-savers-proposals-to-amend-the-occupational-and-personal-pension-schemes-conditions-for-transfers-regulations-2021/options-assessment"),
    "mhssas": ("MoneyHelper", "SSAS pensions explained", "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/defined-contribution-small-self-administered-pension-schemes"),
    "mhsipp": ("MoneyHelper", "SIPPs explained", "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/self-invested-personal-pensions"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "steve": ("Steve's view", "Steve Hunt, 5 October 2026", "#steves-view"),
}
LABEL_ORDER = ["Law", "HMRC", "TPR", "FCA", "FSCS", "DWP", "MoneyHelper", "Provider evidence", "Steve's view"]

SHORT = ("a SSAS is a company pension scheme that your company sets up. Its members are usually its trustees, so "
         "they control how the money is invested. A SIPP is a personal pension run by a SIPP firm: you choose your "
         "investments, but only from what the SIPP firm will accept. A SSAS that meets the small scheme conditions and "
         "HMRC's rules can lend money to its sponsoring company. A SIPP cannot do that for a company connected with "
         "its member. For a money purchase SSAS and a SIPP, the main tax rules on paying in and taking money out are "
         "broadly the same.")
SHORT_SRC = ["s150", "mhssas", "mhsipp", "fca1866", "fcadd", "ptm123200", "s228"]

COMPARE = [  # (row, SSAS, SIPP, source keys)
    ("What kind of pension", "A company (occupational) pension scheme", "A personal pension", ["s150", "perg12"]),
    ("Who sets it up", "A sponsoring employer, usually your company", "You open one with a SIPP firm", ["s150", "mhsipp"]),
    ("Who is in control", "The trustees, usually you and your fellow members", "The SIPP firm, and its trustee where there is one. You choose investments from what it will accept", ["pa34", "mhssas", "fcadd"]),
    ("Who is responsible if the rules are broken", "The trustees run the scheme and can be personally liable for breaches. Members can also face tax charges for unauthorised payments", "The SIPP firm is responsible for running the scheme under FCA rules. The member can still face tax charges for unauthorised payments", ["tprtoolkit", "fca1866", "s208", "ptm134200"]),
    ("Who regulates it", "The Pensions Regulator, and HMRC for tax", "The FCA regulates the SIPP firm, and HMRC for tax", ["tprabout", "fca1866"]),
    ("Can it buy commercial property?", "Yes", "Yes, if the SIPP firm accepts it", ["mhssas", "mhsipp"]),
    ("Can it lend to your company?", "Yes, if the small scheme conditions and HMRC's employer loan rules are met", "No: a loan to a company connected with you is an unauthorised payment", ["ptm123200", "ptm123300", "s161"]),
    ("Can it borrow?", "Up to 50%, under the pension tax borrowing rules", "Up to 50%, under the pension tax borrowing rules", ["s182", "ptm124000"]),
    ("Homes and things like art or classic cars", "Heavy tax charges", "Heavy tax charges", ["sch29a"]),
    ("If the firm running it fails", "The scheme itself is not FSCS protected if its administrator fails. Its assets are held on trust. Eligible bank deposits can have separate FSCS protection", "The FSCS can pay up to £85,000 per person if a SIPP operator failed after 1 April 2019", ["fscs"]),
    ("Fees", "Flat fees: £800 to £2,420 a year plus VAT for two members, for the ten providers whose current fees we could check. Most also charge initial costs", "Vary from firm to firm", ["fees", "mhsipp"]),
]

SAME = [
    ("The annual allowance", "£60,000 a year across all your pensions, with the same carry forward rules.", ["s228"]),
    ("Company tax relief", "Your company's contributions to either can normally be deducted for corporation tax.", ["s196"]),
    ("Taking money out", "The same ages, the same tax-free cash rules and the same income tax rules.", ["s279", "sch29"]),
    ("Death benefits and inheritance tax", "From 6 April 2027, most unused funds and pension death benefits from either can be included in the estate for inheritance tax, subject to the exclusions in the law.", ["s150a"]),
]

MOVING = [
    ("Moving a SIPP into a SSAS", "sipp-to-ssas",
     ["The law allows money to move from one registered pension scheme to another, as a recognised transfer. Before the money goes, the SIPP firm must run the legal scam checks. Because a SSAS is an occupational scheme, you normally need to show a real job link with its employer. The evidence is usually a letter from the employer, a schedule of contributions, and three months of payslips or similar salary evidence. A red flag stops the transfer under these rules. An amber flag means you must first have a safeguarding guidance session with MoneyHelper.",
      "In June 2026 the government proposed a new red flag for transfers into a SSAS where you cannot show a real job link. It is a proposal, not yet law."],
     ["ptm100010", "si1237", "tprtransfer", "dwp"]),
    ("Moving a SSAS into a SIPP", "ssas-to-sipp",
     ["This can also be a recognised transfer. Assets such as business property can move across as they are, if the SIPP firm accepts them, or they can be sold first and the cash moved. A loan from the SSAS to your company cannot move into a SIPP, because a SIPP lending to a company connected with you would be an unauthorised payment. If the SSAS carries on, the loan may stay in it, if the scheme rules and the transfer values allow. If the SSAS is being wound up, the loan must be repaid or dealt with first."],
     ["ptm100010", "ptm123200", "ptm123300", "s161"]),
]

ASK_YOURSELF = [
    "Control and responsibility: SSAS trustees decide how the money is invested, and are responsible for it. A SIPP firm runs a SIPP.",
    "Loans to your company: only a SSAS can make them, under strict rules.",
    "Fees: SSAS fees are flat. SIPP fees vary from firm to firm.",
    "Decisions: in a SSAS with several members, the trustees make decisions together.",
    "A company behind it: a SSAS needs a sponsoring employer. A SIPP does not.",
]

QA = [
    ("What is the main difference between a SSAS and a SIPP?",
     "The main difference is who runs the pension. In a SSAS the members are usually the trustees, so they decide how the money is invested, and are responsible for it. In a SIPP, the SIPP firm runs the scheme, and you choose your investments from what it will accept.",
     ["mhssas", "pa34", "fcadd"]),
    ("Can a SIPP lend money to my company?",
     "No. Only an occupational pension scheme, such as a SSAS, can lend to its sponsoring employer under HMRC's rules. A SIPP lending to a company connected with you would be an unauthorised payment.",
     ["ptm123200", "ptm123300"]),
    ("Can I move my SIPP into a SSAS?",
     "The law allows it, as a recognised transfer, if the SSAS accepts it. The SIPP firm must first run the legal scam checks, including proof of a real job link with the SSAS's employer. Moving a pension can mean losing valuable benefits, and this site does not advise on transfers.",
     ["ptm100010", "si1237", "tprtransfer"]),
    ("Are SSASs and SIPPs taxed differently?",
     "For a money purchase SSAS and a SIPP, the main pension tax rules are broadly the same: the standard annual allowance, the rules for taking money out, and the main death benefit rules. A final salary (defined benefit) SSAS works differently in some areas, including how its annual allowance is measured.",
     ["s228", "s150a"]),
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
  .quote { border-left: 5px solid var(--teal); background: var(--soft); padding: 16px 20px; border-radius: 6px; margin: 18px 0; }
  .quote p { margin: 0 0 10px; font-size: 18px; }
  .quote .who { font-size: 15px; color: var(--muted); margin: 6px 0 0; }
  table.cmp { min-width: 0; }
  table.cmp th:first-child { width: 26%; }
  @media (max-width: 600px) { table.cmp { font-size: 14px; } table.cmp th, table.cmp td { padding: 8px 6px; } }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    groups = [SHORT_SRC, ["steve"]] + [c[3] for c in COMPARE] + [s[2] for s in SAME] + [m[3] for m in MOVING] + [q[2] for q in QA] + [["ptm121000"]]
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
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "SSAS or SIPP: what is the difference?",
         "description": "The difference between a SSAS and a SIPP: who is in control, who regulates them, loans to your company, property, fees and FSCS protection, and moving between them.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS or SIPP", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>SSAS or SIPP: what is the difference? | My SSAS</title>")
    w('<meta name="description" content="SSAS or SIPP? Who is in control, who regulates them, loans to your company, property, fees and FSCS protection, and moving between them, in plain English with the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="SSAS or SIPP: what is the difference?">')
    w('<meta property="og:description" content="Self-invested with a small s and a small i, or with a capital S and a capital I? The real difference between a SIPP and a SSAS. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS or SIPP</p>')
    w("  <h1>SSAS or SIPP: what is the difference?</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {SHORT}</p>")
    w("    " + src_line(SHORT_SRC))
    w("  </div>")
    w("")
    w('  <h2 id="steves-view">The big, big difference</h2>')
    w('  <div class="quote">')
    for p in STEVE:
        w(f"    <p>{html.escape(p, quote=False)}</p>")
    w('    <p class="who">Steve Hunt ACII TEP, in his own words</p>')
    w("  </div>")
    w("  " + src_line(["steve", "pa34", "fcadd"]))
    w("")
    w('  <h2 id="side-by-side">Side by side</h2>')
    w('  <div class="tablewrap">')
    w('    <table class="cmp">')
    w("      <thead><tr><th></th><th>SSAS</th><th>SIPP</th></tr></thead>")
    w("      <tbody>")
    for row, a, b, _ in COMPARE:
        w(f"        <tr><td>{html.escape(row)}</td><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>")
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    cmpkeys = []
    for _, _, _, keys in COMPARE:
        for k in keys:
            if k not in cmpkeys:
                cmpkeys.append(k)
    w('  <p class="note">Borrowing: for a money purchase pension, the 50% test is applied to the relevant arrangement, and any existing borrowing counts.</p>')
    w("  " + src_line(cmpkeys))
    w("")
    w('  <h2 id="the-same">What is the same</h2>')
    w("  <p>For a money purchase SSAS and a SIPP, many of the main pension tax rules are the same. A final salary (defined benefit) SSAS works differently in some areas.</p>")
    w('  <ul class="plain">')
    for title, text, _ in SAME:
        w(f"    <li><strong>{html.escape(title)}:</strong> {html.escape(text, quote=False)}</li>")
    w("  </ul>")
    w("  " + src_line(["s228", "s196", "s279", "sch29", "s150a", "ptm121000"]))
    for title, sid, paras, keys in MOVING:
        w("")
        w(f'  <h2 id="{sid}">{html.escape(title)}</h2>')
        for p in paras:
            w(f"  <p>{html.escape(p, quote=False)}</p>")
        w("  " + src_line(keys))
    w('  <p class="note">This is information only. It is not a recommendation to move a pension. Moving a pension can mean losing valuable benefits, and this site does not advise on transfers.</p>')
    w("")
    w('  <h2 id="things-to-compare">Things to compare</h2>')
    w('  <ul class="plain">')
    for item in ASK_YOURSELF:
        w(f"    <li>{html.escape(item, quote=False)}</li>")
    w("  </ul>")
    w("")
    w('  <h2 id="questions">Common questions</h2>')
    for q, a, keys in QA:
        w(f"  <h3>{html.escape(q, quote=False)}</h3>")
        w(f"  <p>{html.escape(a, quote=False)}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <div class="choice">')
    w("    <h2>A question about SSAS or SIPP?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read <a href="/who-runs-a-ssas/">who runs a SSAS</a>, the <a href="/faq/">SSAS pension FAQ</a>, or compare <a href="' + FEES + '">SSAS provider fees</a>.</p>')
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
            if label == "Steve's view":
                w("    <li>Steve Hunt ACII TEP, in his own words (5 October 2026): the quote above. It is his view, based on his experience, not a statement of law.</li>")
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
    print(f"built {OUT}, {len(text):,} bytes, {len(used)} sources")


if __name__ == "__main__":
    main()
