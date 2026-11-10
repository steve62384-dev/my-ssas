#!/usr/bin/env python3
"""Build /ssas-loanback/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "ssas-loanback" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/ssas-loanback/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

S = {
    "s179": ("Law", "Finance Act 2004, s.179", "https://www.legislation.gov.uk/ukpga/2004/12/section/179"),
    "sch30": ("Law", "Finance Act 2004, Sch 30", "https://www.legislation.gov.uk/ukpga/2004/12/schedule/30"),
    "s161": ("Law", "Finance Act 2004, s.161(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/161"),
    "s150": ("Law", "Finance Act 2004, s.150(6)", "https://www.legislation.gov.uk/ukpga/2004/12/section/150"),
    "s186": ("Law", "Finance Act 2004, s.186", "https://www.legislation.gov.uk/ukpga/2004/12/section/186"),
    "s208": ("Law", "Finance Act 2004, ss.208 and 209", "https://www.legislation.gov.uk/ukpga/2004/12/section/208"),
    "s239": ("Law", "Finance Act 2004, ss.239 and 240", "https://www.legislation.gov.uk/ukpga/2004/12/section/239"),
    "si3449": ("Law", "SI 2005/3449 (minimum interest rate)", "https://www.legislation.gov.uk/uksi/2005/3449/contents"),
    "inv12": ("Law", "SI 2005/3378, regs 1(2) and 12", "https://www.legislation.gov.uk/uksi/2005/3378/regulation/12"),
    "pa36": ("Law", "Pensions Act 1995, s.36(3)", "https://www.legislation.gov.uk/ukpga/1995/26/section/36"),
    "ca859": ("Law", "Companies Act 2006, ss.859A, 859F and 859H", "https://www.legislation.gov.uk/ukpga/2006/46/part/25"),
    "lra27": ("Law", "Land Registration Act 2002, s.27(2)(f)", "https://www.legislation.gov.uk/ukpga/2002/9/section/27"),
    "ptm123100": ("HMRC", "PTM123100: loans, general principles", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123100"),
    "ptm123200": ("HMRC", "PTM123200: loans to sponsoring employers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123200"),
    "ptm123300": ("HMRC", "PTM123300: loans to members and connected parties", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123300"),
    "ptm022000": ("HMRC", "PTM022000: types of pension scheme", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm022000"),
    "ptm135100": ("HMRC", "PTM135100: scheme sanction charge", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm135100"),
    "trusteetax": ("HMRC", "Tax on investments for pension trustees", "https://www.gov.uk/guidance/pension-trustees-investments-and-tax"),
    "chcharge": ("GOV.UK", "Companies House: mortgages and loan guarantees", "https://www.gov.uk/make-changes-to-your-limited-company/mortgages-and-loan-guarantees"),
    "boe": ("Bank of England", "Bank Rate maintained at 3.75%, September 2026", "https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/september-2026"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "example": ("Steve's analysis", "The worked example, using HMRC's formula", "#worked-example"),
}
LABEL_ORDER = ["Law", "HMRC", "GOV.UK", "Bank of England", "Provider evidence", "Steve's analysis"]

SHORT = ("yes. A SSAS can lend money to the company that sponsors it. This is called a loanback. The loan can be up to "
         "50% of the cash and market value of the scheme's assets just before it is made. It must be secured by a first charge, carry at least "
         "HMRC's minimum interest rate, and be repaid within five years, with at least a set amount repaid each year. "
         "Pension law also only allows it if the SSAS meets the small scheme conditions. Break the rules and the tax "
         "charges are heavy.")
SHORT_SRC = ["s179", "sch30", "ptm123200", "inv12"]

TESTS = [
    ("How much can be lent?", "how-much",
     ["Up to 50% of the cash and the market value of the assets held for the scheme immediately before the loan is made. The test is done when the loan is made. It is not done again if the scheme's investments fall later, unless the loan terms change. A further loan is a new loan, and is tested again when it is made."],
     ["s179", "ptm123200"]),
    ("What security is needed?", "security",
     ["The loan must be secured for its whole term by a first charge on an asset. The asset can belong to the company or to someone else. No other charge on the asset can rank ahead of the scheme's. When the loan is made, the asset must be worth at least the loan plus interest.",
      "If the security is swapped for another asset, the new asset must be worth at least the lower of two figures: the old asset's value, or the amount still owed, including interest."],
     ["s179", "sch30", "ptm123200"]),
    ("What interest must the company pay?", "interest",
     ["At least 1% above the average base lending rate of six banks named in the regulations: Bank of Scotland, Barclays, HSBC, Lloyds Bank, NatWest and The Royal Bank of Scotland. The average is first rounded up to the next 0.25%. The minimum rate is reset on the 6th working day of each month, using the banks' rates 12 working days before. The loan can have a fixed rate, as long as it is at least the minimum when the loan is made.",
      "For illustration only: if all six named banks had a base lending rate of 3.75%, the minimum would be 4.75%. The Bank of England's Bank Rate was also 3.75% in September 2026, but that is not the legal test. The legal test uses the six banks' own base lending rates, on the right date."],
     ["si3449", "ptm123200", "boe"]),
    ("How long can the loan last?", "term",
     ["No more than five years from the date it is made. If the company is in genuine difficulty and money is still owed at the end, the loan can be rolled over once, for up to five more years. The existing security can carry on. A second roll-over brings the unauthorised payment tax charges."],
     ["s179", "ptm123200"]),
    ("How must it be repaid?", "repayment",
     ["By the end of each loan year, the company must have repaid at least an equal share of the total capital and interest. HMRC's formula is: (the loan plus all the interest) divided by the number of loan years, times the loan years so far. Equal yearly instalments of capital and interest meet this exactly. Paying more early is fine."],
     ["sch30", "ptm123200"]),
]

PENSION_LAW = [
    ("The small scheme conditions",
     "Pension law bans loans to the employer unless the SSAS meets the small scheme conditions. That means fewer than 12 members, all of them trustees (or all directors of a company that is the only trustee). Decisions must also be unanimous, unless the scheme has the required independent trustee or director. If a member is neither a trustee nor a director of the company that is the only trustee, the scheme does not meet this test.",
     ["inv12"]),
    ("Proper advice first",
     "As with other investments, the trustees must get and consider proper advice before making the loan, given or confirmed in writing.",
     ["pa36"]),
    ("A genuine investment",
     "HMRC says every loan must be a genuine investment of the scheme: prudent, secure and on a commercial basis. The company must get no special treatment. If it gets into financial trouble, the trustees must enforce the debt on the same basis as similar creditors would.",
     ["ptm123100"]),
]

EXAMPLE_ROWS = [  # year, payment, interest, capital, owed at year end
    (1, 34407, 7125, 27282, 122718),
    (2, 34407, 5829, 28578, 94140),
    (3, 34407, 4472, 29935, 64204),
    (4, 34407, 3050, 31357, 32847),
    (5, 34407, 1560, 32847, 0),
]

STEPS = [
    "Check the SSAS meets the small scheme conditions, and that the company is a sponsoring employer.",
    "Value the scheme immediately before the loan, to find the 50% limit.",
    "The trustees get and consider proper advice, in writing.",
    "Agree the terms in a written loan agreement: the amount, the interest rate (at least the minimum), the term and the repayments.",
    "Put the first-charge security in place, on an asset worth at least the loan plus interest. If a company gives the charge, register it at Companies House within 21 days, starting the day after it is created. Registering late needs a court order. If the security is registered land, the charge must also be registered at HM Land Registry.",
    "Pay the money to the company, and keep a record of every repayment.",
    "Collect the repayments on time. If the company falls behind, the trustees must chase the debt as any other lender would, using the security if needed.",
]
STEPS_SRC = ["inv12", "s179", "pa36", "ptm123200", "chcharge", "ca859", "lra27", "ptm123100"]

QA = [
    ("Can my SSAS lend money to me?",
     "No. A loan from a registered pension scheme to a member, or to anyone connected with a member, is an unauthorised payment and is taxed.",
     ["ptm123300", "s161"]),
    ("Can it lend to my other company?",
     "Only if the other company genuinely qualifies as a sponsoring employer. HMRC normally recognises it as one where one or more of its employees are members of the scheme, and their benefits relate to that job. Simply adding the company's name to the paperwork is not enough. If you control the other company and it is not a sponsoring employer, the loan is an unauthorised payment.",
     ["s150", "ptm022000", "ptm123300", "s161"]),
    ("What can the company spend the money on?",
     "HMRC's guidance does not say. But the loan must still be a genuine investment of the scheme: prudent, secure and commercial.",
     ["ptm123100", "ptm123200"]),
    ("Can a SIPP lend to my company in the same way?",
     "No. Only an occupational pension scheme, such as a SSAS, can make a loan to a sponsoring employer under these rules. A SIPP has no sponsoring employer.",
     ["ptm123200"]),
    ("Does the SSAS pay tax on the interest?",
     "Normally no. HMRC says the income and gains from most pension scheme investments are not taxable. The interest is paid to the SSAS, not to a bank.",
     ["s186", "trusteetax"]),
    ("What happens if the loan breaks a rule from the start?",
     "HMRC treats the part that breaks the rule as an unauthorised payment. In HMRC's own example, a £100,000 loan from a scheme worth £180,000 was £10,000 over the 50% limit of £90,000. The company faced a 40% charge on that £10,000, which is £4,000. The scheme administrator can also face a scheme sanction charge, normally 15% where the 40% charge has been paid.",
     ["ptm123200", "s208", "s239", "ptm135100"]),
    ("What does a loanback cost to set up?",
     "SSAS firms usually charge a fee for each loan. For example, Highstone charges £500 plus VAT for each loan. Mattioli Woods charges £280 an hour plus VAT to set a loan up, then £370 a year plus VAT. There may also be legal and valuation costs.",
     ["fees"]),
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


def money(n):
    return "£{:,}".format(n)


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  p.src { font-size: 14px; color: var(--muted); margin: 6px 0 0; word-break: break-word; }
  p.src .lead { font-weight: 700; margin-right: 4px; }
  p.src .lbl { font-weight: 600; }
  table.ex { min-width: 0; }
  @media (max-width: 600px) { table.ex { font-size: 13px; } table.ex th, table.ex td { padding: 7px 5px; } }
  table.ex td.num, table.ex th.num { text-align: right; white-space: nowrap; }
  table.ex tr.total td { font-weight: 700; border-top: 2px solid var(--line); }
  table.ex td:first-child { font-weight: 400; }
  ol.how li { margin-bottom: 8px; }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    for keys in [SHORT_SRC] + [t[3] for t in TESTS] + [p[2] for p in PENSION_LAW] + [STEPS_SRC] + [q[2] for q in QA] + [["example"]]:
        for k in keys:
            if k not in used:
                used.append(k)

    faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]
    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/",
         "sameAs": ["https://www.linkedin.com/in/steve~hunt", "https://www.youtube.com/@SteveHuntACIITEP",
                    "https://x.com/SHunt_ACII_TEP", "https://inheritancetaxexplained.co.uk/about-steve-hunt/"]},
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "Can my SSAS lend money to my company?",
         "description": "The SSAS loanback rules: the 50% limit, security, minimum interest, the five-year term, repayments, pension law's small scheme conditions, a worked example and what happens if it goes wrong.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions", "mainEntity": faq_entities},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS loanback rules", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>SSAS loanback rules: how a SSAS can lend to your company | My SSAS</title>")
    w('<meta name="description" content="The SSAS loanback rules in plain English: the 50% limit, first charge security, minimum interest, the five-year term and repayments, with a worked example and the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="Can my SSAS lend money to my company?">')
    w('<meta property="og:description" content="The SSAS loanback rules in plain English, with a worked example and the law linked. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS loanback rules</p>')
    w("  <h1>Can my SSAS lend money to my company?</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {SHORT}</p>")
    w("    " + src_line(SHORT_SRC))
    w("  </div>")
    w("")
    w('  <h2 id="hmrc-tests">HMRC\'s five tests</h2>')
    w("  <p>HMRC says a loan to a sponsoring employer must pass five tests to be an authorised employer loan. If it fails one, the tax charges below apply.</p>")
    for title, sid, paras, keys in TESTS:
        w(f'  <h3 id="{sid}">{html.escape(title)}</h3>')
        for p in paras:
            w(f"  <p>{p}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <h2 id="pension-law">Pension law adds three more points</h2>')
    for title, text, keys in PENSION_LAW:
        w(f"  <h3>{html.escape(title)}</h3>")
        w(f"  <p>{text}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <h2 id="worked-example">A worked example</h2>')
    w("  <p>Just before the loan, a SSAS is worth £400,000, so it can lend up to £200,000. It lends £150,000 to the company for five years, at a fixed 4.75% a year. The company repays in five equal yearly payments of £34,407. The security is a first charge over the company's premises, worth £250,000 with no other charge.</p>")
    w('  <div class="tablewrap">')
    w('    <table class="ex">')
    w('      <thead><tr><th>Year</th><th class="num">Payment</th><th class="num">Interest</th><th class="num">Capital</th><th class="num">Still owed</th></tr></thead>')
    w("      <tbody>")
    for y, pay, i, cap, owed in EXAMPLE_ROWS:
        w(f'        <tr><td>{y}</td><td class="num">{money(pay)}</td><td class="num">{money(i)}</td><td class="num">{money(cap)}</td><td class="num">{money(owed)}</td></tr>')
    w('        <tr class="total"><td>Total</td><td class="num">£172,036</td><td class="num">£22,036</td><td class="num">£150,000</td><td class="num"></td></tr>')
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    w('  <p class="note">Figures are rounded to the nearest pound.</p>')
    w("  <p>Does it pass the tests?</p>")
    w('  <ul class="plain">')
    w("    <li><strong>Amount:</strong> £150,000 is under the £200,000 limit.</li>")
    w("    <li><strong>Security:</strong> the loan plus all the interest is £172,035.67. The premises are worth £250,000, which is more.</li>")
    w("    <li><strong>Interest:</strong> 4.75% is at least the minimum, if the six named banks' base lending rates were 3.75% at the time.</li>")
    w("    <li><strong>Term:</strong> five years.</li>")
    w("    <li><strong>Repayments:</strong> HMRC's formula gives (£150,000 + £22,035.67) &divide; 5, which is about £34,407.13 a year. Equal payments of that amount meet it. The table rounds to whole pounds, so a real loan agreement would work the payments out to the penny, and adjust the last payment by a few pence.</li>")
    w("  </ul>")
    w("  <p>Over the five years, the company pays about £22,036 of interest to the SSAS rather than to a bank.</p>")
    w("  " + src_line(["example", "ptm123200", "si3449"]))
    w("")
    w('  <h2 id="steps">The steps</h2>')
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
    w("    <h2>A question about loanbacks?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read the <a href="/faq/">SSAS pension FAQ</a> or compare <a href="' + FEES + '">SSAS provider fees</a>.</p>')
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
                w("    <li>The worked example: our own arithmetic, using HMRC's repayment formula from PTM123200 and an assumed fixed rate of 4.75%. It is an illustration, not a recommendation.</li>")
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
