#!/usr/bin/env python3
"""Build /how-to-set-up-a-ssas/index.html for my-ssas.co.uk.

Template parts (style, header, footer) are copied from the home page.
"""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "how-to-set-up-a-ssas" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/how-to-set-up-a-ssas/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

S = {  # sources used on this page: key -> (label, title, url)
    "s150": ("Law", "Finance Act 2004, s.150(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/150"),
    "s153": ("Law", "Finance Act 2004, s.153(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/153"),
    "s196": ("Law", "Finance Act 2004, s.196", "https://www.legislation.gov.uk/ukpga/2004/12/section/196"),
    "s228": ("Law", "Finance Act 2004, s.228", "https://www.legislation.gov.uk/ukpga/2004/12/section/228"),
    "pa36": ("Law", "Pensions Act 1995, s.36(3)", "https://www.legislation.gov.uk/ukpga/1995/26/section/36"),
    "pa49": ("Law", "Pensions Act 1995, s.49(1)", "https://www.legislation.gov.uk/ukpga/1995/26/section/49"),
    "reg11": ("Law", "SI 1996/1715, reg 11", "https://www.legislation.gov.uk/uksi/1996/1715/regulation/11"),
    "s197": ("Law", "Finance Act 2004, s.197", "https://www.legislation.gov.uk/ukpga/2004/12/section/197"),
    "cta54": ("Law", "Corporation Tax Act 2009, s.54", "https://www.legislation.gov.uk/ukpga/2009/4/section/54"),
    "reg3": ("Law", "SI 1996/1715, reg 3(1)(h)", "https://www.legislation.gov.uk/uksi/1996/1715/regulation/3"),
    "inv12": ("Law", "SI 2005/3378, regs 1(2) and 12", "https://www.legislation.gov.uk/uksi/2005/3378/regulation/12"),
    "si1237": ("Law", "SI 2021/1237", "https://www.legislation.gov.uk/uksi/2021/1237/contents"),
    "ptm032100": ("HMRC", "PTM032100: applying to register", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm032100"),
    "ptm032200": ("HMRC", "PTM032200: HMRC's decision", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm032200"),
    "ptm032300": ("HMRC", "PTM032300: date of registration", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm032300"),
    "ptm043200": ("HMRC", "PTM043200: relief for employers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm043200"),
    "ptm100010": ("HMRC", "PTM100010: transfers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm100010"),
    "ptm121000": ("HMRC", "PTM121000: investments, essential principles", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm121000"),
    "ptm125100": ("HMRC", "PTM125100: tangible moveable property", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm125100"),
    "ptm151000": ("HMRC", "PTM151000: the scheme administrator", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm151000"),
    "ptm153000": ("HMRC", "PTM153000: fit and proper person", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm153000"),
    "regadmin": ("HMRC", "Register as a pension scheme administrator", "https://www.gov.uk/guidance/pension-administrators-register-as-an-administrator"),
    "regscheme": ("HMRC", "Apply to register a pension scheme", "https://www.gov.uk/guidance/pension-administrators-register-a-scheme"),
    "nl180": ("HMRC", "Pension schemes newsletter 180, April 2026", "https://www.gov.uk/government/publications/pension-schemes-newsletter-180-april-2026/newsletter-180-april-2026"),
    "tprtrustee": ("TPR", "Trustee guidance", "https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/governing-body-detailed-guidance/trustee-guidance"),
    "tprreg": ("TPR", "Register a pension scheme", "https://www.thepensionsregulator.gov.uk/en/trustees/submit-reports-payments-and-requests-to-us/register-a-pension-scheme"),
    "tprtransfer": ("TPR", "Dealing with transfer requests", "https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/administration-detailed-guidance/dealing-with-transfer-requests"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
}
LABEL_ORDER = ["Law", "HMRC", "TPR", "Provider evidence"]

SHORT = ("your company sets up the SSAS under a trust deed, and appoints the trustees and a scheme administrator. "
         "The scheme administrator then applies online to HMRC to register it. The tax reliefs start from the date "
         "HMRC registers it. There is no fixed time, because HMRC has no time limit to decide. We checked the current fees "
         "of ten providers. For a SSAS with two members, the yearly fee is £800 to £2,420 plus VAT. "
         "Of the initial costs we can price, the highest in our simple example is £2,100 plus VAT.")
SHORT_SRC = ["s153", "ptm032100", "ptm032300", "tprtrustee", "fees"]

STEPS = [
    ("Check your company can be the employer",
     ["A SSAS must be set up by an employer. That is usually a limited company you own and run. HMRC can refuse to register a scheme if a sponsoring employer has been dormant. That means dormant for a whole month in a row, during the year before HMRC decides."],
     ["s150", "s153", "ptm032200"]),
    ("Decide who will run it",
     ["You can pay a specialist SSAS firm to be the scheme administrator, and often a trustee too. Or the member trustees can do the job themselves. Either way, a scheme administrator must be UK resident, make declarations to HMRC and be fit and proper. You can compare the firms on our <a href=\"" + FEES + "\">fee page</a>."],
     ["regadmin", "ptm151000", "ptm153000", "fees"]),
    ("Set up the trust",
     ["Your company sets up the scheme with a trust deed and rules. The trust deed is the legal document that sets up and governs the scheme. The rules give the detailed conditions. The trustees must act in line with both. The members usually help run the scheme, as trustees or as directors of a company that is the trustee.",
      "Think about the small-scheme rules now. A scheme with fewer than 12 members can be let off some rules, such as having an auditor. For that, all the members must be trustees, or all must be directors of a company that is the only trustee. Decisions must also be unanimous, unless the scheme has the required independent trustee or director. The same conditions matter if the SSAS will ever lend to your company."],
     ["tprtrustee", "reg3", "inv12"]),
    ("Register with HMRC",
     ["The scheme administrator registers with HMRC first, using the Managing pension schemes service. Then they apply online to register the scheme. Only the scheme administrator can apply, and it cannot be done on paper.",
      "HMRC asks for details such as the names, addresses and National Insurance numbers of the directors and trustees. It also asks for the company's registration number and its tax references. An application can be saved, but must be finished within 28 days."],
     ["regadmin", "regscheme", "ptm032100"]),
    ("Wait for HMRC's decision",
     ["HMRC may ask questions, and it has no time limit to decide. If there is no decision within six months, the scheme administrator can appeal to a tribunal. Registration cannot be backdated. Tax relief only starts from the date HMRC registers the scheme."],
     ["ptm032200", "ptm032300", "regscheme"]),
    ("Open a bank account for the scheme",
     ["The trustees must normally keep the money they receive for the scheme in a separate account with a bank, building society or other authorised deposit-taker. Scheme money must not be mixed with the employer's money."],
     ["tprtrustee", "pa49", "reg11"]),
    ("Register with The Pensions Regulator, if there is more than one member",
     ["A SSAS with more than one member must be registered with The Pensions Regulator within three months of first meeting the rules for registration. A one-member SSAS does not need to register with it."],
     ["tprreg"]),
    ("Pay money in",
     ["Your company can pay in. Its contributions can normally be deducted for corporation tax, if they are paid wholly and exclusively for the trade. Relief is normally given for the accounting period in which they are paid, although very large increases can be spread. For 2026/27 the standard annual allowance is £60,000 across all of a member's pensions, although it can be lower for some people.",
      "Money can also come in from other pension schemes. Before a transfer under the legal transfer rules, the old scheme must carry out the required scam checks. Moving a pension can mean losing valuable benefits, and this site does not advise on it."],
     ["s196", "s197", "cta54", "ptm043200", "s228", "ptm100010", "si1237", "tprtransfer"]),
    ("Invest, after proper advice",
     ["Before most investments, the trustees must get and consider proper advice, given or confirmed in writing. Homes, and things like art, antiques or classic cars, bring heavy tax charges."],
     ["pa36", "ptm121000", "ptm125100"]),
]

SECTIONS = [
    ("How long does it take?", "how-long-does-it-take",
     ["There is no fixed time. HMRC has no time limit to decide, although the scheme administrator can appeal if there is no decision within six months. If the SSAS has more than one member, it must be registered with The Pensions Regulator within three months. Before you choose a SSAS firm, ask how long its own steps usually take."],
     ["regscheme", "ptm032200", "tprreg"]),
    ("What does it cost?", "what-does-it-cost",
     ["We checked the current fees of ten providers. For a SSAS with two members, the yearly fee is £800 to £2,420 plus VAT. Most also charge initial costs, such as a set-up fee and a fee to open the investment account. Of those we can price, the highest in our simple example is £2,100 plus VAT. Some charge the yearly fee in advance and some in arrears, so ask when the first one is due. The fees are flat, not a percentage of the pension. Buying a property, or lending to your company, usually costs extra. <a href=\"" + FEES + "\">See every provider's fees, compared</a>."],
     ["fees"]),
    ("Why does HMRC refuse some schemes?", "why-does-hmrc-refuse-some-schemes",
     ["The law says HMRC must register a new pension scheme unless certain problems apply. These include wrong or false information, and a scheme not set up mainly to provide authorised pensions or lump sums. They also include a scheme administrator who is not fit and proper, and a sponsoring company that has been dormant.",
      "In 2025/26 HMRC received 2,421 applications to register new pension schemes of all kinds, not just SSASs. It registered 54%, refused 33%, and had not yet decided the rest."],
     ["s153", "ptm032200", "nl180"]),
]

CHECKLIST = [
    "An employer to set up the scheme. HMRC can refuse to register a scheme if a sponsoring employer has been dormant (see step 1).",
    "Who the trustees will be, and who will be the scheme administrator.",
    "For each director and trustee: name, address (and previous address, where HMRC asks for it), National Insurance number, phone number and email address.",
    "The company's registration number, and its HMRC references: PAYE, Unique Taxpayer Reference (UTR) and VAT number.",
    "A Government Gateway user ID for the scheme administrator, if you will run the scheme yourselves.",
]
CHECKLIST_SRC = ["regscheme", "regadmin"]

ASK = [
    "Is a professional trustee included in the fee?",
    "How many members does the fee cover?",
    "What does buying a property, or lending to my company, cost?",
    "Must cash be left in the bank account, and how much?",
    "Do the fees rise every year?",
    "Will you deal with me direct, or only through a financial adviser?",
    "How long do your own set-up steps usually take?",
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
  ol.steps { padding-left: 0; list-style: none; counter-reset: step; }
  ol.steps > li { counter-increment: step; position: relative; padding: 0 0 6px 52px; margin: 0 0 18px; }
  ol.steps > li::before { content: counter(step); position: absolute; left: 0; top: 0; width: 36px; height: 36px; border-radius: 50%; background: var(--teal); color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; }
  ol.steps h3 { font-size: 19px; margin: 4px 0 6px; }
  ol.steps p { margin: 0 0 8px; }
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
    for keys in [SHORT_SRC, CHECKLIST_SRC] + [s[2] for s in STEPS] + [s[3] for s in SECTIONS]:
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
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "How do I set up a SSAS?",
         "description": "The steps to set up a SSAS pension, how long it takes, what it costs and why HMRC refuses some schemes.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "How to set up a SSAS", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>How to set up a SSAS pension: the steps, the time and the cost | My SSAS</title>")
    w('<meta name="description" content="How to set up a SSAS pension: the steps in order, what HMRC asks for, how long it takes, what it costs and why HMRC refuses some schemes, in plain English with the law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="How do I set up a SSAS?">')
    w('<meta property="og:description" content="The steps to set up a SSAS pension, how long it takes and what it costs, in plain English with the law linked. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; How to set up a SSAS</p>')
    w("  <h1>How do I set up a SSAS?</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {SHORT}</p>")
    w("    " + src_line(SHORT_SRC))
    w("  </div>")
    w("")
    w('  <h2 id="the-steps">The steps, in order</h2>')
    w('  <ol class="steps">')
    for title, paras, keys in STEPS:
        w("    <li>")
        w(f"      <h3>{html.escape(title)}</h3>")
        for p in paras:
            w(f"      <p>{p}</p>")
        w("      " + src_line(keys))
        w("    </li>")
    w("  </ol>")
    w("")
    w('  <h2 id="what-you-need">What you need before you start</h2>')
    w('  <ul class="plain">')
    for item in CHECKLIST:
        w(f"    <li>{html.escape(item, quote=False)}</li>")
    w("  </ul>")
    w("  " + src_line(CHECKLIST_SRC))
    for title, sid, paras, keys in SECTIONS:
        w("")
        w(f'  <h2 id="{sid}">{html.escape(title)}</h2>')
        for p in paras:
            w(f"  <p>{p}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <h2 id="questions-to-ask">Questions to ask a SSAS firm</h2>')
    w('  <ul class="plain">')
    for item in ASK:
        w(f"    <li>{html.escape(item, quote=False)}</li>")
    w("  </ul>")
    w("  " + src_line(["fees"]))
    w("")
    w('  <div class="choice">')
    w("    <h2>Thinking about a SSAS?</h2>")
    w('    <p>Take the <a href="/take-the-ssas-test/">SSAS Test</a>, or ask Steve a question. Your question goes to Steve, who will get back to you.</p>')
    w('    <a class="ask" href="/contact/">Ask Steve a question about SSAS pensions</a>')
    w("  </div>")
    w("")
    w("  <h2>More on SSAS pensions</h2>")
    w('  <ul class="plain">')
    w('    <li><a href="/faq/">SSAS pension FAQ: every question answered</a></li>')
    w(f'    <li><a href="{FEES}">SSAS provider fees compared, 2026</a></li>')
    w('    <li><a href="/who-runs-a-ssas/">Who runs a SSAS, and who regulates it</a></li>')
    w('    <li><a href="/ssas-loanback/">SSAS loanback rules</a></li>')
    w("  </ul>")
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
