#!/usr/bin/env python3
"""Build /ssas-commercial-property/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "ssas-commercial-property" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/ssas-commercial-property/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

S = {
    "sch29a": ("Law", "Finance Act 2004, Sch 29A, paras 7, 8, 10 and 14", "https://www.legislation.gov.uk/ukpga/2004/12/schedule/29A"),
    "s174a": ("Law", "Finance Act 2004, s.174A", "https://www.legislation.gov.uk/ukpga/2004/12/section/174A"),
    "s185a": ("Law", "Finance Act 2004, ss.185A to 185G", "https://www.legislation.gov.uk/ukpga/2004/12/section/185A"),
    "s162": ("Law", "Finance Act 2004, s.162", "https://www.legislation.gov.uk/ukpga/2004/12/section/162"),
    "s182": ("Law", "Finance Act 2004, ss.182 to 185", "https://www.legislation.gov.uk/ukpga/2004/12/section/182"),
    "inv7": ("Law", "SI 2005/3378, reg 7(1)", "https://www.legislation.gov.uk/uksi/2005/3378/regulation/7"),
    "mees": ("Law", "SI 2015/962 (minimum energy efficiency standards)", "https://www.legislation.gov.uk/uksi/2015/962/contents"),
    "ptm121000": ("HMRC", "PTM121000: investments, essential principles", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm121000"),
    "ptm125200": ("HMRC", "PTM125200: residential property", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm125200"),
    "ptm125300": ("HMRC", "PTM125300: direct holdings of taxable property", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm125300"),
    "ptm133700": ("HMRC", "PTM133700: value shifting", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm133700"),
    "ptm123100": ("HMRC", "PTM123100: loans, general principles", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123100"),
    "ptm124000": ("HMRC", "PTM124000: borrowing", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm124000"),
    "bim46801": ("HMRC", "BIM46801: rent and rates", "https://www.gov.uk/hmrc-internal-manuals/business-income-manual/bim46801"),
    "bim20205": ("HMRC", "BIM20205: badges of trade", "https://www.gov.uk/hmrc-internal-manuals/business-income-manual/bim20205"),
    "trusteetax": ("HMRC", "Tax on investments for pension trustees", "https://www.gov.uk/guidance/pension-trustees-investments-and-tax"),
    "vat742": ("HMRC", "Land and property (VAT Notice 742)", "https://www.gov.uk/guidance/vat-on-land-and-property-notice-742"),
    "vat742a": ("HMRC", "Opting to tax land and buildings (VAT Notice 742A)", "https://www.gov.uk/guidance/opting-to-tax-land-and-buildings-notice-742a"),
    "sdltrates": ("GOV.UK", "Stamp Duty Land Tax: non-residential and mixed rates", "https://www.gov.uk/stamp-duty-land-tax/nonresidential-and-mixed-rates"),
    "sdlt": ("GOV.UK", "Stamp Duty Land Tax", "https://www.gov.uk/stamp-duty-land-tax"),
    "cgt": ("GOV.UK", "Capital Gains Tax for business", "https://www.gov.uk/capital-gains-tax-businesses"),
    "epc": ("GOV.UK", "Energy Performance Certificates for your business premises", "https://www.gov.uk/energy-performance-certificate-commercial-property"),
    "meesguide": ("GOV.UK", "Non-domestic private rented property: minimum energy efficiency standard, landlord guidance", "https://www.gov.uk/guidance/non-domestic-private-rented-property-minimum-energy-efficiency-standard-landlord-guidance"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "example": ("Steve's analysis", "The worked example", "#worked-example"),
}
LABEL_ORDER = ["Law", "HMRC", "GOV.UK", "Provider evidence", "Steve's analysis"]

SHORT = ("yes. A SSAS can buy commercial property, including the building your company uses. Your company can then "
         "rent it at a full market rent, and the rent goes into the pension. The SSAS can buy from you or your "
         "company, but only at market value. It can borrow up to half of its net value to help. Homes are different: "
         "a SSAS that holds a home faces heavy tax charges.")
SHORT_SRC = ["ptm121000", "sch29a", "ptm124000"]

SECTIONS = [
    ("What a SSAS can buy", "what-it-can-buy", [
        ("Commercial property", "A SSAS can buy commercial property, such as offices, shops, factories, warehouses and land. That includes the building your company uses. Commercial property is not taxable property, so the heavy charges for homes do not apply.", ["ptm121000", "sch29a"]),
        ("Not homes", "Homes are taxable property, wherever they are in the world. A SSAS that holds one faces heavy tax charges when it buys, every year it holds it, and on any gain when it sells. Some buildings do not count as homes, such as qualifying care homes, student halls, hospitals and a whole hotel.", ["s174a", "s185a", "sch29a", "ptm125200", "ptm125300"]),
        ("A flat above a shop", "A flat counts as a home, even if it is part of a commercial building, unless an exception applies. One exception is a flat used with business premises the SSAS owns, such as a flat above a shop. The person living there must not be a member or connected with a member. Another is a flat or house for an employee who must live there as a condition of the job. That employee must not be a member, connected with a member, or connected with the employer.", ["sch29a", "ptm125200"]),
    ]),
    ("Buying from you or your company", "buying-from-you", [
        ("Market value only", "The SSAS can buy from you, your company or anyone connected with you, but only at the price an unconnected buyer would pay. If it pays more than the property is worth, HMRC treats the extra as an unauthorised payment and taxes it. The same applies if it later sells to you or your company for less than the property is worth.", ["ptm121000", "ptm133700"]),
        ("Tax for the seller", "If you sell a property at a gain, you may have Capital Gains Tax to pay. A limited company normally pays Corporation Tax on its gains instead.", ["cgt"]),
        ("Stamp duty land tax", "The SSAS pays stamp duty land tax on the purchase in England and Northern Ireland. Scotland and Wales have their own versions. The return must be sent, and the tax paid, within 14 days of completion. A solicitor usually does this.", ["sdltrates", "sdlt"]),
        ("VAT", "Selling or letting commercial property is normally exempt from VAT. But if the owner has opted to tax the building, VAT is normally charged on the price and the rent. The freehold sale of a new commercial building, one completed less than three years ago, normally has VAT on it too. An option to tax does not pass to the buyer: the buyer decides whether to opt. Check the VAT position before the SSAS buys.", ["vat742", "vat742a"]),
    ]),
    ("Renting it to your company", "renting-it", [
        ("Full market rent", "Your company can rent the building from the SSAS, but it must pay the full commercial rent. If it pays less, HMRC taxes the shortfall as an unauthorised payment. If rent is left unpaid and not collected on normal terms, it can be treated as a loan to the company. A loan to the company must meet strict rules.", ["ptm121000", "ptm123100", "s162"]),
        ("Where the rent goes", "The rent is paid to the SSAS, and the income from most pension scheme investments is not taxed. For your company, rent paid for premises it uses for its business is normally an allowable expense, under the wholly and exclusively rule.", ["trusteetax", "bim46801"]),
        ("Energy rating", "The SSAS trustees are the landlord. In England and Wales, the minimum energy rules normally stop a landlord letting a commercial building with an EPC rating below E. This does not apply if a valid exemption is registered. A commercial building normally needs an EPC when it is sold or let.", ["epc", "meesguide", "mees"]),
    ]),
    ("Borrowing to buy", "borrowing", [
        ("How much", "A SSAS can borrow up to 50% of its net value just before the new borrowing, counting any borrowing it already has. In a money purchase SSAS, the test is worked out for each member's arrangement. HMRC lets it borrow for any purpose the trustees are satisfied will benefit the scheme.", ["s182", "ptm124000"]),
        ("If it borrows too much", "If new borrowing takes the scheme over the limit, the excess normally faces a 40% scheme sanction charge. Pension law's own limit on borrowing does not apply to schemes with fewer than 100 members.", ["ptm124000", "inv7"]),
    ]),
]

EXAMPLE_ROWS = [
    ("Price of the premises", "£550,000"),
    ("Stamp duty land tax (England)", "£17,000"),
    ("Borrowed (the 50% limit)", "£200,000"),
    ("Paid from the SSAS's own money", "£367,000"),
    ("Left in the SSAS, before fees", "£33,000"),
]

STEPS = [
    "Check the property is commercial, with no home in it unless an exception applies.",
    "Get the price checked by an independent valuer, so you can show it is market value.",
    "Check the VAT position, including whether the seller has opted to tax and whether the building is new.",
    "Arrange any borrowing within the 50% limit.",
    "The trustees buy the property through a solicitor, who usually sends the stamp duty return and pays the tax within 14 days.",
    "The trustees grant your company a lease at a full market rent.",
    "Collect the rent on time, keep the EPC up to date, and meet the minimum energy standard.",
]
STEPS_SRC = ["sch29a", "ptm121000", "vat742", "vat742a", "ptm124000", "sdlt", "epc", "meesguide"]

QA = [
    ("Can my company use the building rent free?",
     "No. Your company must pay the full commercial rent. If it pays less, HMRC taxes the shortfall as an unauthorised payment.",
     ["ptm121000"]),
    ("Can my SSAS buy property from me?",
     "Yes, but only at market value. You may have Capital Gains Tax to pay on any gain, and the SSAS pays stamp duty land tax.",
     ["ptm121000", "cgt", "sdltrates"]),
    ("Can my SSAS buy a holiday let or a buy-to-let flat?",
     "Not without heavy tax charges. Homes are taxable property for a SSAS, wherever they are.",
     ["sch29a", "ptm125300"]),
    ("Can my SSAS build or convert property?",
     "It can put up a commercial building to rent out. But building to sell at a profit may be trading, and trading profits do not get the pension tax exemptions. Once a building is ready to live in while the SSAS owns it, it counts as a home.",
     ["ptm121000", "bim20205", "ptm125200"]),
    ("What does buying a property cost?",
     "As well as the price and stamp duty land tax, SSAS firms usually charge a fee for each purchase. For example, Highstone charges £750 and Mattioli Woods £1,190, both plus VAT. Some firms also charge a yearly fee for each property: Mattioli Woods charges £740 a year plus VAT. There are also legal and valuation costs.",
     ["fees", "sdltrates"]),
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
  table.ex { min-width: 0; max-width: 520px; }
  table.ex td.num { text-align: right; white-space: nowrap; font-weight: 600; }
  table.ex td:first-child { font-weight: 400; }
  ol.how li { margin-bottom: 8px; }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    groups = [SHORT_SRC] + [k for _, _, items in SECTIONS for (_, _, k) in items] + [["example", "sdltrates", "ptm124000"], STEPS_SRC] + [q[2] for q in QA]
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
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "Can my SSAS buy my business premises?",
         "description": "SSAS commercial property: what a SSAS can buy, buying from you, renting to your company, borrowing, stamp duty, VAT and a worked example.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS and commercial property", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>SSAS commercial property: buying your business premises | My SSAS</title>")
    w('<meta name="description" content="Can my SSAS buy my business premises? What a SSAS can buy, buying from you, renting to your company, borrowing, stamp duty and VAT, with a worked example and the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="Can my SSAS buy my business premises?">')
    w('<meta property="og:description" content="SSAS commercial property in plain English, with a worked example and the law linked. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS and commercial property</p>')
    w("  <h1>Can my SSAS buy my business premises?</h1>")
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
    w("  <p>A SSAS with one member holds £400,000 and has no borrowing. Just before it borrows, it can borrow up to half of that: £200,000. It buys the company's premises in England for £550,000, the price an independent valuer confirms is market value. The building is not new and the seller has not opted to tax, so there is no VAT on the price.</p>")
    w("  <p>Stamp duty land tax is nothing on the first £150,000, 2% on the next £100,000 (£2,000) and 5% on the remaining £300,000 (£15,000). That makes £17,000.</p>")
    w('  <div class="tablewrap">')
    w('    <table class="ex">')
    w("      <tbody>")
    for item, amount in EXAMPLE_ROWS:
        w(f'        <tr><td>{html.escape(item)}</td><td class="num">{amount}</td></tr>')
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    w("  <p>The company then pays the SSAS a full market rent, set by a valuer. The SSAS uses the rent to repay its loan and to build up the pension, and pays no tax on the rent. The company can normally deduct the rent as a business expense. The SSAS will also pay legal, valuation and SSAS firm fees.</p>")
    w("  " + src_line(["example", "sdltrates", "ptm124000", "trusteetax", "bim46801"]))
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
    w("    <h2>A question about SSAS property?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read about <a href="/ssas-loanback/">SSAS loanbacks</a>, the <a href="/faq/">SSAS pension FAQ</a>, or compare <a href="' + FEES + '">SSAS provider fees</a>.</p>')
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
                w("    <li>The worked example: our own arithmetic, using the stamp duty land tax rates for non-residential property and HMRC's 50% borrowing limit. The prices are made up for the example. It is an illustration, not a recommendation.</li>")
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
