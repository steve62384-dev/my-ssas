#!/usr/bin/env python3
"""Build /ssas-disadvantages/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "ssas-disadvantages" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/ssas-disadvantages/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"
LEG = "https://www.legislation.gov.uk/ukpga/2004/12/section/"
PA95 = "https://www.legislation.gov.uk/ukpga/1995/26/section/"
PTM = "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/"
TPRDOC = "https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/"
DWP = "https://www.gov.uk/government/consultations/protecting-pension-savers-proposals-to-amend-the-occupational-and-personal-pension-schemes-conditions-for-transfers-regulations-2021"

S = {
    "pa33": ("Law", "Pensions Act 1995, s.33", PA95 + "33"),
    "pa36": ("Law", "Pensions Act 1995, s.36(3)", PA95 + "36"),
    "pa49": ("Law", "Pensions Act 1995, s.49(1)", PA95 + "49"),
    "pa2004s256": ("Law", "Pensions Act 2004, s.256", "https://www.legislation.gov.uk/ukpga/2004/35/section/256"),
    "fa153": ("Law", "Finance Act 2004, s.153(5)", LEG + "153"),
    "fa161": ("Law", "Finance Act 2004, s.161(5)", LEG + "161"),
    "fa179": ("Law", "Finance Act 2004, s.179", LEG + "179"),
    "fa208": ("Law", "Finance Act 2004, ss.208, 209, 239 and 240", LEG + "240"),
    "fa242": ("Law", "Finance Act 2004, ss.158 and 242", LEG + "242"),
    "fa270": ("Law", "Finance Act 2004, s.270", LEG + "270"),
    "inv1": ("Law", "SI 2005/3378, regs 1(2) and 12", "https://www.legislation.gov.uk/uksi/2005/3378/regulation/1"),
    "inv7": ("Law", "SI 2005/3378, regs 6 and 7", "https://www.legislation.gov.uk/uksi/2005/3378/regulation/7"),
    "audit": ("Law", "SI 1996/1715, reg 3(1)(h)", "https://www.legislation.gov.uk/uksi/1996/1715/regulation/3"),
    "si2021": ("Law", "SI 2021/1237", "https://www.legislation.gov.uk/uksi/2021/1237/contents"),
    "ptm022000": ("HMRC", "PTM022000: types of pension scheme", PTM + "ptm022000"),
    "ptm032200": ("HMRC", "PTM032200: HMRC's decision", PTM + "ptm032200"),
    "ptm033200": ("HMRC", "PTM033200: de-registration", PTM + "ptm033200"),
    "ptm033300": ("HMRC", "PTM033300: consequences of de-registration", PTM + "ptm033300"),
    "ptm100010": ("HMRC", "PTM100010: transfers", PTM + "ptm100010"),
    "ptm121000": ("HMRC", "PTM121000: investments, essential principles", PTM + "ptm121000"),
    "ptm123100": ("HMRC", "PTM123100: loans, general principles", PTM + "ptm123100"),
    "ptm123200": ("HMRC", "PTM123200: loans to sponsoring employers", PTM + "ptm123200"),
    "ptm131000": ("HMRC", "PTM131000: unauthorised payments", PTM + "ptm131000"),
    "ptm135100": ("HMRC", "PTM135100: scheme sanction charge", PTM + "ptm135100"),
    "ptm160200": ("HMRC", "PTM160200: keeping records", PTM + "ptm160200"),
    "hmrcreports": ("HMRC", "Send pension scheme reports", "https://www.gov.uk/guidance/pension-administrators-reporting-to-hmrc"),
    "regadmin": ("HMRC", "Register as a pension scheme administrator", "https://www.gov.uk/guidance/pension-administrators-register-as-an-administrator"),
    "nl180": ("HMRC", "Pension schemes newsletter 180, April 2026", "https://www.gov.uk/government/publications/pension-schemes-newsletter-180-april-2026/newsletter-180-april-2026"),
    "toolkit5": ("TPR", "Trustee toolkit, tutorial 5: trustee liabilities and protections", "https://trusteetoolkit.thepensionsregulator.gov.uk/pluginfile.php/133/mod_data/content/2375/The%20trustees%20role%20-%20Tutorial%205%20Trustee%20liabilities%20and%20protections.pdf"),
    "tprreturn": ("TPR", "DC scheme return", "https://www.thepensionsregulator.gov.uk/en/trustees/submit-reports-payments-and-requests-to-us/scheme-return/dc-scheme-return"),
    "tprtransfer": ("TPR", "Dealing with transfer requests", TPRDOC + "administration-detailed-guidance/dealing-with-transfer-requests"),
    "tprwindup": ("TPR", "Winding up a defined contribution scheme: deciding whether to wind up", TPRDOC + "winding-up-or-transferring-a-scheme-detailed-guidance/winding-up-a-defined-contribution-scheme/decide-whether-the-scheme-should-be-wound-up"),
    "tprprivate": ("TPR", "Private markets investment", TPRDOC + "funding-and-investment-detailed-guidance/private-markets-investment"),
    "tprdcinv": ("TPR", "Investment governance in DC schemes", TPRDOC + "funding-and-investment-detailed-guidance/investment-guide-for-dc-pension-schemes"),
    "fcahartley": ("FCA", "Hartley Pensions Limited enters administration", "https://www.fca.org.uk/news/news-stories/hartley-pensions-limited-enters-administration"),
    "fscspen": ("FSCS", "Pensions", "https://www.fscs.org.uk/what-we-cover/pensions/"),
    "fscsdep": ("FSCS", "Deposit limit", "https://www.fscs.org.uk/what-we-cover/banks-building-societies-credit-unions/deposit-limit/"),
    "pra64": ("PRA", "PRA Rulebook: Depositor Protection, rule 6.4", "https://www.prarulebook.co.uk/pra-rules/depositor-protection"),
    "dwpcons": ("DWP", "Protecting pension savers: consultation, 9 June 2026", DWP),
    "dwpopt": ("DWP", "Protecting pension savers: options assessment, 9 June 2026", DWP + "/options-assessment"),
    "moneyhelper": ("MoneyHelper", "SSAS pensions explained", "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/defined-contribution-small-self-administered-pension-schemes"),
    "uhy": ("Administrators", "Hartley Pensions: progress report, 29 January to 28 July 2026", "https://www.uhy-uk.com/sites/default/files/2026-08/Administrators%20progress%20report%20-%20JULY%202026.pdf"),
    "sdltrates": ("GOV.UK", "Stamp Duty Land Tax: non-residential and mixed rates", "https://www.gov.uk/stamp-duty-land-tax/nonresidential-and-mixed-rates"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "analysis": ("Steve's analysis", "The flat fee and 1% comparison", "#questions"),
}
LABEL_ORDER = ["Law", "HMRC", "TPR", "FCA", "FSCS", "PRA", "DWP", "MoneyHelper", "Administrators", "GOV.UK",
               "Provider evidence", "Steve's analysis"]

SHORT = ("a SSAS gives you control, but it comes with cost, work and risk. The fees are flat, so they weigh more on a "
         "small pension. You are usually a trustee, so you carry legal duties and can be personally liable. Breaking "
         "the tax rules is costly. A SSAS that lends to your company or owns its premises ties your pension to your "
         "business. And the scheme itself is not protected by the FSCS.")
SHORT_SRC = ["fees", "toolkit5", "ptm131000", "ptm123200", "fscspen"]

SECTIONS = [
    ("Cost", "cost", [
        ("Flat fees", "We checked the current fees of ten providers. For a SSAS with two members, the yearly fee is £800 to £2,420 plus VAT. Most also charge initial costs, and extra for buying property or making a loan. The fees are flat, so the smaller the pension, the bigger the fee is as a share of it.",
         ["fees"]),
        ("Other costs", "Buying property also brings legal and valuation fees, and stamp duty land tax. Before most investments, the trustees must get and consider proper advice, given or confirmed in writing. That advice can cost money too.",
         ["sdltrates", "pa36"]),
    ]),
    ("Responsibility", "responsibility", [
        ("You carry the legal duties", "In a SSAS you are usually a trustee. A trustee can have to pay personally for a loss caused by their own breach of trust. More than one trustee can be liable for the same loss. The trust deed cannot remove liability for failing to take proper care with investments. Some fines and penalties on a trustee cannot be paid from the scheme's money.",
         ["toolkit5", "pa33", "pa2004s256"]),
        ("Breaking the tax rules is costly", "An unauthorised payment normally causes a 40% tax charge on the member or employer. A further 15% surcharge can apply if enough unauthorised payments are made. The scheme administrator can also face a scheme sanction charge: normally 15% where the 40% charge has been paid, but up to 40% otherwise. In serious cases HMRC can de-register the scheme, if one of the grounds in the law applies. One example is when the scheme's chargeable payments pass a set limit. The scheme administrator then faces a charge of 40% of the cash and the market value of the assets held just before.",
         ["fa208", "ptm131000", "ptm135100", "fa242", "ptm033200", "ptm033300"]),
        ("Paperwork and deadlines", "Someone must keep clear records, for the tax year they relate to and six more years. The scheme must report to HMRC when certain events happen, and send returns when asked. A money purchase SSAS with 2 to 11 members normally completes a scheme return for The Pensions Regulator every three years. Scheme money must be kept in its own bank account, apart from the employer's money. Since 6 April 2026, the scheme administrator must be UK resident.",
         ["ptm160200", "hmrcreports", "tprreturn", "pa49", "regadmin", "fa270"]),
        ("Trustees have to agree", "To lend to your company, or to be let off having an auditor, a SSAS must meet the small scheme conditions. One way is for every decision to be unanimous among the member trustees. Where a company is the only trustee, every decision must be unanimous among the directors who are members. So one member trustee, or one member director, can block a decision. The other way is to have the required independent trustee or director.",
         ["inv1", "audit"]),
    ]),
    ("Risk", "risk", [
        ("Your pension and your business are tied together", "A SSAS can lend your company up to 50% of the cash and market value of its assets. It can also own your company's premises. If the company struggles, the pension can suffer too. A loan may not be repaid on time, and rolling it over more than once brings tax charges. Rent left unpaid, and not collected on normal terms, can be treated as a loan to the company. Pension law expects the trustees to think about spreading the risk.",
         ["fa179", "ptm123200", "ptm121000", "ptm123100", "inv7"]),
        ("Property can be slow to sell", "The Pensions Regulator says most private market assets, such as property, cannot easily or quickly be turned into cash. A quick sale may mean a lower price. So the trustees must plan for the cash the scheme will need, for example to pay benefits or transfers out.",
         ["tprprivate", "tprdcinv"]),
        ("No FSCS cover for the scheme", "The scheme itself is not protected by the FSCS if it fails. Cash a SSAS holds in a UK bank can be protected. For a money purchase SSAS, the FSCS can treat each eligible member separately, up to £120,000 per member per banking licence. A member's own savings at the same bank count towards the same limit.",
         ["fscspen", "fscsdep", "pra64"]),
        ("If the SSAS firm fails", "The scheme's money and assets are held on trust. They are kept apart from the SSAS firm's own money, even if the firm is also a trustee. But moving to a new firm can be slow and costly. Hartley Pensions went into administration on 29 July 2022. In July 2026, four years on, its administrators were still working on a sale or transfer of its SSAS business.",
         ["fcahartley", "uhy"]),
        ("Scammers target SSASs", "MoneyHelper warns that, because SSASs are not regulated by the FCA, scammers often use them to reach scam investments. Being asked to join the SSAS of a company you have no real link to is a warning sign. Inventing a job link to join is fraud. In June 2026 the government said up to 1 in 10 transfers into SSASs could be fraud.",
         ["moneyhelper", "dwpopt"]),
    ]),
    ("Getting started", "getting-started", [
        ("HMRC refuses some new schemes", "HMRC must register a new scheme unless certain problems apply. Examples are wrong or false information, or a scheme administrator who is not fit and proper. HMRC received 2,421 applications to register new pension schemes in 2025/26. It registered 54% and refused 33%. Those figures cover all kinds of scheme, not just SSASs.",
         ["fa153", "ptm032200", "nl180"]),
        ("Transfers in face extra checks", "Before your old scheme lets money move into a SSAS, it must run the scam checks in the 2021 transfer rules. These include proof that you have a real link to the SSAS's employer. In June 2026 the government asked for views on a new red flag, to stop a transfer where there is no real job link. By 5 October 2026 it had not published its response.",
         ["si2021", "tprtransfer", "dwpcons"]),
    ]),
    ("When things change", "changes", [
        ("If your company is sold or closes", "A SSAS does not end just because the company is sold or closes, unless its rules say so. But the trustees may need a new sponsoring employer, or to run it as a closed scheme, transfer it or wind it up. Any loan to the company must keep to HMRC's loan rules until it is paid back. HMRC can take a SSAS off its register if a sponsoring employer is a dormant company.",
         ["ptm022000", "tprwindup", "ptm123200", "ptm033200"]),
    ]),
]

QA = [
    ("Is a SSAS worth it for a small pension?",
     "No law sets a minimum size for a SSAS. But the fees are flat, so they weigh more on a small pension. A flat fee of £1,500 a year costs less than a 1% yearly charge once the pension is above £150,000, and more below it. Some providers set their own minimum.",
     ["fees", "analysis"]),
    ("Can I lose money in a SSAS?",
     "Yes. The investments a SSAS holds can fall in value, so you could get back less than was paid in. The scheme itself is not protected by the FSCS.",
     ["moneyhelper", "fscspen"]),
    ("Can I move out of a SSAS later?",
     "Usually, yes. Members can normally move their share to another registered pension scheme, such as a SIPP. Assets such as business property can move across as they are, if the new scheme accepts them, or be sold first. A loan from the SSAS to your company cannot move into a SIPP. This site does not advise on transfers.",
     ["ptm100010", "ptm123200", "fa161"]),
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
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    groups = [SHORT_SRC] + [k for _, _, items in SECTIONS for (_, _, k) in items] + [q[2] for q in QA]
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
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "What are the disadvantages of a SSAS?",
         "description": "The disadvantages of a SSAS: cost, trustee duties and liability, tax charges, paperwork, ties to your business, no FSCS cover for the scheme, provider failure, scams and HMRC refusals.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "SSAS disadvantages", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>SSAS disadvantages: the honest list | My SSAS</title>")
    w('<meta name="description" content="What are the disadvantages of a SSAS? Cost, trustee duties, tax charges, paperwork, ties to your business, no FSCS cover for the scheme and scams, with the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="What are the disadvantages of a SSAS?">')
    w('<meta property="og:description" content="The honest list of SSAS disadvantages, in plain English, with the law linked. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; SSAS disadvantages</p>')
    w("  <h1>What are the disadvantages of a SSAS?</h1>")
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
    w('  <h2 id="questions">Common questions</h2>')
    for q, a, keys in QA:
        w(f"  <h3>{html.escape(q, quote=False)}</h3>")
        w(f"  <p>{html.escape(a, quote=False)}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <div class="choice">')
    w("    <h2>A question about the downsides?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read <a href="/who-runs-a-ssas/">who runs a SSAS</a>, <a href="/ssas-vs-sipp/">SSAS or SIPP</a>, or compare <a href="' + FEES + '">SSAS provider fees</a>.</p>')
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
