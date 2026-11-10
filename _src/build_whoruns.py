#!/usr/bin/env python3
"""Build /who-runs-a-ssas/index.html for my-ssas.co.uk (template parts copied from the home page)."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "who-runs-a-ssas" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/who-runs-a-ssas/"
CHECKED = "5 October 2026"
CHECKED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"

S = {
    "s150": ("Law", "Finance Act 2004, s.150(5)", "https://www.legislation.gov.uk/ukpga/2004/12/section/150"),
    "pa34": ("Law", "Pensions Act 1995, s.34(1)", "https://www.legislation.gov.uk/ukpga/1995/26/section/34"),
    "pa33": ("Law", "Pensions Act 1995, s.33", "https://www.legislation.gov.uk/ukpga/1995/26/section/33"),
    "pa36": ("Law", "Pensions Act 1995, s.36(3)", "https://www.legislation.gov.uk/ukpga/1995/26/section/36"),
    "pa7": ("Law", "Pensions Act 1995, s.7", "https://www.legislation.gov.uk/ukpga/1995/26/section/7"),
    "si1991": ("Law", "SI 1991/1614, reg 9 (pensioneer trustee, before 6 April 2006)", "https://www.legislation.gov.uk/uksi/1991/1614/made"),
    "pa49": ("Law", "Pensions Act 1995, s.49(1)", "https://www.legislation.gov.uk/ukpga/1995/26/section/49"),
    "pa2004s256": ("Law", "Pensions Act 2004, s.256", "https://www.legislation.gov.uk/ukpga/2004/35/section/256"),
    "reg3": ("Law", "SI 1996/1715, reg 3(1)(h)", "https://www.legislation.gov.uk/uksi/1996/1715/regulation/3"),
    "inv": ("Law", "SI 2005/3378, regs 6 and 7", "https://www.legislation.gov.uk/uksi/2005/3378/contents"),
    "s270": ("Law", "Finance Act 2004, s.270", "https://www.legislation.gov.uk/ukpga/2004/12/section/270"),
    "ptm151000": ("HMRC", "PTM151000: the scheme administrator", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm151000"),
    "ptm153000": ("HMRC", "PTM153000: fit and proper person", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm153000"),
    "ptm135300": ("HMRC", "PTM135300: who pays the scheme sanction charge", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm135300"),
    "ptm032200": ("HMRC", "PTM032200: HMRC's decision to register", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm032200"),
    "ptm033200": ("HMRC", "PTM033200: de-registration", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm033200"),
    "ptm123200": ("HMRC", "PTM123200: loans to sponsoring employers", "https://www.gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm123200"),
    "regadmin": ("HMRC", "Register as a pension scheme administrator", "https://www.gov.uk/guidance/pension-administrators-register-as-an-administrator"),
    "reports": ("HMRC", "Send pension scheme reports", "https://www.gov.uk/guidance/pension-administrators-reporting-to-hmrc"),
    "tprabout": ("TPR", "About us", "https://www.thepensionsregulator.gov.uk/en/about-us"),
    "tprtrustee": ("TPR", "Trustee guidance", "https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/governing-body-detailed-guidance/trustee-guidance"),
    "tprtoolkit": ("TPR", "Trustee toolkit, tutorial 5: trustee liabilities and protections", "https://trusteetoolkit.thepensionsregulator.gov.uk/pluginfile.php/133/mod_data/content/2375/The%20trustees%20role%20-%20Tutorial%205%20Trustee%20liabilities%20and%20protections.pdf"),
    "tprreg": ("TPR", "Register a pension scheme", "https://www.thepensionsregulator.gov.uk/en/trustees/submit-reports-payments-and-requests-to-us/register-a-pension-scheme"),
    "tprreturn": ("TPR", "DC scheme return", "https://www.thepensionsregulator.gov.uk/en/trustees/submit-reports-payments-and-requests-to-us/scheme-return/dc-scheme-return"),
    "tprpen": ("TPR", "Monetary penalties policy", "https://www.thepensionsregulator.gov.uk/en/document-library/regulatory-and-enforcement-policies/monetary-penalties-policy"),
    "fca1866": ("FCA", "Glossary: establishing, operating or winding up a personal pension scheme", "https://handbook.fca.org.uk/glossary/G1866"),
    "fca974": ("FCA", "Glossary: regulated activity", "https://handbook.fca.org.uk/glossary/G974"),
    "perg12": ("FCA", "PERG 12.2: personal pension schemes", "https://handbook.fca.org.uk/handbook/perg12/perg12s2"),
    "fcadd": ("FCA", "Dear CEO letter: due diligence for SIPP investments, 30 October 2018", "https://www.fca.org.uk/publication/dear-ceo-letters/dear-ceo-letter-due-diligence-requirements-for-self-invested-pension-plan-sipp-investments.pdf"),
    "tpo": ("Ombudsman", "The Pensions Ombudsman: what we can and cannot do", "https://www.pensions-ombudsman.org.uk/what-we-can-and-cannot-do"),
    "mhssas": ("MoneyHelper", "SSAS pensions explained", "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/defined-contribution-small-self-administered-pension-schemes"),
    "mhsipp": ("MoneyHelper", "SIPPs explained", "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/self-invested-personal-pensions"),
    "bpch": ("Published source", "BP Pension Trustees Limited, Companies House", "https://find-and-update.company-information.service.gov.uk/company/00230748"),
    "bpsize": ("Published source", "Top1000funds: BP Pension UK", "https://www.top1000funds.com/asset_owner/bp-pension-uk/"),
    "fees": ("Provider evidence", "SSAS provider fees compared, 2026", FEES),
    "steve": ("Steve's view", "Steve Hunt, 5 October 2026", "#steves-view"),
}
LABEL_ORDER = ["Law", "HMRC", "TPR", "FCA", "Ombudsman", "MoneyHelper", "Published source", "Provider evidence", "Steve's view"]

SHORT = ("usually, you do. In a SSAS the members are normally the trustees, so the trustees, usually including the "
         "business owner, decide how the money is invested, within the law, and are responsible for it. A scheme administrator deals with HMRC, and "
         "some SSASs also have a professional trustee. The Pensions Regulator regulates the scheme, and HMRC runs its "
         "tax rules. Running a SSAS is not an FCA-regulated activity, but FCA rules apply to advice about investments "
         "and pension transfers.")
SHORT_SRC = ["mhssas", "pa34", "ptm151000", "tprabout", "fca1866"]

STEVE = [
    "So many people confuse a SIPP with a SSAS. In this respect the two could not be more different.",
    "With a SIPP, even though you think you have control because it is self-invested, it is still a personal pension. The true control sits with the SIPP firm and, where there is one, its trustee. They let you invest within certain parameters: you choose from the investments the SIPP firm will accept. So it is self-invested with a small s and a small i. That is the big, big difference.",
    "With a SSAS, you are usually a trustee. The business owner is a trustee, the business owner shares the responsibility, and the business owner decides, with any fellow trustees, how the money is invested.",
    "A SSAS is a small company pension scheme, but it is still a company pension scheme. The SSAS itself is regulated by The Pensions Regulator, not by the FCA in the way a SIPP is, and that in itself is a big thing.",
    "The way I explain it is this. The Mr Miggins Ltd pension scheme is the same kind of scheme as the BP pension scheme: both are trust-based company pension schemes, just on completely different scales. The BP pension scheme's billions are invested under the control of its trustees, even though they can hand day-to-day investment decisions to experts. In the same way, you, as a trustee of the Mr Miggins Ltd pension scheme, decide with your fellow trustees how your company pension scheme's money is invested. You have control, as a trustee. It is Self-Invested with a capital S and a capital I.",
]

TRUSTEE_POINTS = [
    ("Who they are",
     "In a SSAS the members are usually the trustees. A professional trustee can sit alongside the member trustees. Or a company can be the sole trustee, with the members acting as its directors.",
     ["mhssas", "reg3"]),
    ("What power they have",
     "The law gives trustees very wide investment powers. Subject to the investment rules in pension law and the scheme's own rules, they have the same power to invest as if they owned the assets outright. That does not mean the money is theirs: they hold it on trust for the scheme. Big company pension schemes work the same way.",
     ["pa34", "bpch", "bpsize"]),
    ("What they must do",
     "Trustees must act in line with the trust deed and rules. Before most investments, they must get and consider proper advice, given or confirmed in writing. They must keep scheme money in a separate bank account, apart from the employer's money.",
     ["tprtrustee", "pa36", "pa49"]),
    ("What they are responsible for",
     "A trustee can have to pay personally for a loss caused by their own breach of trust. The trust deed cannot remove liability for failing to take proper care with investments. Some fines and penalties on a trustee cannot be paid from the scheme's money.",
     ["tprtoolkit", "pa33", "pa2004s256"]),
    ("What small schemes are let off",
     "Small schemes are let off some rules that big schemes must follow. A scheme with fewer than 12 members needs no auditor, if all the members are trustees (or all are directors of a company that is the only trustee) and the decision-making conditions are met. A scheme with fewer than 100 members needs no written statement of investment principles, although the trustees must still think about spreading the risk.",
     ["reg3", "inv"]),
]

OTHERS = [
    ("The scheme administrator", "scheme-administrator",
     "The scheme administrator is the person or firm responsible for the pension tax rules and for dealing with HMRC. It can be the member trustees themselves, or a specialist SSAS firm. Since 6 April 2026 a scheme administrator must be UK resident. They must make declarations to HMRC and be fit and proper. The scheme administrator pays some tax charges, such as the scheme sanction charge.",
     ["s270", "ptm151000", "regadmin", "ptm153000", "ptm135300"]),
    ("Professional trustees and SSAS firms", "professional-trustees",
     "There is no general rule that every SSAS must have a professional trustee. The old rule that every SSAS needed an approved pensioneer trustee ended in 2006. The Pensions Regulator can appoint a trustee in special cases. Some SSAS firms will only run a scheme if they are a trustee too, so check before you choose. A professional trustee can sit alongside you as a trustee. Or a company can be the sole trustee, with the members as its directors.",
     ["si1991", "pa7", "fees"]),
]

REGULATORS = [
    ("The Pensions Regulator", "Regulates workplace pension schemes, including SSASs. A SSAS with more than one member must register with it, and files a scheme return. It can fine trustees, and appoint a trustee in special cases.",
     ["tprabout", "tprreg", "tprreturn", "tprpen", "pa7"]),
    ("HMRC", "Registers the scheme for tax, and runs the pension tax rules. It receives event reports and tax returns, charges tax on unauthorised payments, and can take a scheme off its register.",
     ["ptm032200", "reports", "ptm033200"]),
    ("The FCA", "Does not regulate running a SSAS, in the way it regulates running a personal pension such as a SIPP. But FCA rules apply to separate services, such as investment advice, managing investments and pension transfer advice.",
     ["fca1866", "fca974"]),
    ("The Pensions Ombudsman", "Deals with most complaints about how an occupational pension scheme is run or administered.",
     ["tpo"]),
    ("The Financial Ombudsman Service", "Deals with complaints about FCA-regulated firms, including investment or pension transfer advice, and some SSAS investment complaints.",
     ["tpo"]),
]

COMPARE = [  # (row, SSAS, SIPP)
    ("What kind of pension", "A company (occupational) pension scheme", "A personal pension"),
    ("Who sets it up", "Your company", "A pension firm, which you join"),
    ("Who runs it", "The trustees, usually you", "The SIPP firm"),
    ("Who decides the investments", "The trustees, within the law and the scheme's rules", "You choose, from what the SIPP firm will accept"),
    ("Who regulates it", "The Pensions Regulator, and HMRC for tax", "The FCA regulates the SIPP firm, and HMRC for tax"),
    ("Can it lend to your company?", "Yes, under HMRC's strict rules", "No"),
]
COMPARE_SRC = ["s150", "pa34", "mhssas", "mhsipp", "fca1866", "perg12", "fcadd", "tprabout", "ptm123200"]

QA = [
    ("Am I in control of my SSAS?",
     "Usually, yes. In a SSAS the members are normally the trustees, and the trustees decide how the money is invested, within the law and the scheme's rules. If the SSAS has a professional trustee, trustee control is shared. In a corporate trustee structure, the members may instead act as directors of the trustee company.",
     ["mhssas", "pa34"]),
    ("Is a SSAS regulated by the FCA?",
     "Running a SSAS is not an FCA-regulated activity. The Pensions Regulator regulates the scheme, and HMRC runs its tax rules. But FCA rules apply to separate services, such as investment advice and pension transfer advice.",
     ["fca1866", "tprabout"]),
    ("Who makes sure a SSAS follows the rules?",
     "The trustees and the scheme administrator are responsible for that. The Pensions Regulator oversees the scheme under pensions law, and HMRC checks the tax rules.",
     ["tprtrustee", "ptm151000", "tprabout"]),
    ("What happens if the trustees get it wrong?",
     "A trustee can have to pay personally for a loss caused by their own breach of trust. The Pensions Regulator can fine trustees. Certain fines and civil penalties imposed personally on a trustee cannot be paid from the scheme. Breaking the tax rules brings tax charges, some of which the scheme administrator pays.",
     ["tprtoolkit", "tprpen", "pa2004s256", "ptm135300"]),
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
  table.cmp th:first-child { width: 28%; }
  @media (max-width: 600px) { table.cmp { font-size: 14px; } table.cmp th, table.cmp td { padding: 8px 6px; } }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    used = []
    groups = [SHORT_SRC, ["steve"]] + [t[2] for t in TRUSTEE_POINTS] + [o[3] for o in OTHERS] + [r[2] for r in REGULATORS] + [COMPARE_SRC] + [q[2] for q in QA]
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
        {"@type": "Article", "@id": PAGE_URL + "#article", "headline": "Who runs a SSAS, and who regulates it?",
         "description": "Who controls a SSAS (the trustees, usually the business owner), the scheme administrator, professional trustees, and who regulates it: The Pensions Regulator, HMRC and, for advice, the FCA. With a SSAS and SIPP comparison.",
         "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
         "datePublished": CHECKED_ISO, "dateModified": CHECKED_ISO, "inLanguage": "en-GB",
         "mainEntityOfPage": PAGE_URL, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "FAQPage", "@id": PAGE_URL + "#questions",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in QA]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Who runs a SSAS", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>Who runs a SSAS, and who regulates it? | My SSAS</title>")
    w('<meta name="description" content="Who controls a SSAS: the trustees (usually the business owner), the scheme administrator and any professional trustee. Who regulates it: The Pensions Regulator, HMRC and, for advice, the FCA. Plain English, law linked.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<meta property="og:type" content="article">')
    w('<meta property="og:site_name" content="My SSAS">')
    w('<meta property="og:title" content="Who runs a SSAS, and who regulates it?">')
    w('<meta property="og:description" content="In a SSAS, the business owner is usually the trustee, and in control. Who does what, and who regulates it, in plain English. By Steve Hunt ACII TEP.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; Who runs a SSAS</p>')
    w("  <h1>Who runs a SSAS, and who regulates it?</h1>")
    w(f'  <p class="byline">By Steve Hunt ACII TEP &middot; Last checked {CHECKED}</p>')
    w('  <div class="answer">')
    w(f"    <p><strong>The short answer:</strong> {SHORT}</p>")
    w("    " + src_line(SHORT_SRC))
    w("  </div>")
    w("")
    w('  <h2 id="steves-view">Self-Invested with a capital S and a capital I</h2>')
    w('  <div class="quote">')
    for p in STEVE:
        w(f"    <p>{html.escape(p, quote=False)}</p>")
    w('    <p class="who">Steve Hunt ACII TEP, in his own words</p>')
    w("  </div>")
    w("  <p>The law backs this up. It gives trustees very wide investment powers. Subject to the investment rules in pension law and the scheme's own rules, they have the same power to invest as if they owned the assets outright. That does not mean the money is theirs: they hold it on trust for the scheme. This is the same in any trust-based company pension scheme, big or small.</p>")
    w("  " + src_line(["steve", "pa34", "bpch", "bpsize"]))
    w("")
    w('  <h2 id="trustees">The trustees: in control, and responsible</h2>')
    for title, text, keys in TRUSTEE_POINTS:
        w(f"  <h3>{html.escape(title)}</h3>")
        w(f"  <p>{html.escape(text, quote=False)}</p>")
        w("  " + src_line(keys))
    for title, sid, text, keys in OTHERS:
        w("")
        w(f'  <h2 id="{sid}">{html.escape(title)}</h2>')
        w(f"  <p>{html.escape(text, quote=False)}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <h2 id="regulators">Who regulates a SSAS?</h2>')
    w('  <div class="tablewrap">')
    w('    <table class="cmp">')
    w("      <thead><tr><th>Who</th><th>What it does for a SSAS</th></tr></thead>")
    w("      <tbody>")
    for who, what, _ in REGULATORS:
        w(f"        <tr><td>{html.escape(who)}</td><td>{html.escape(what, quote=False)}</td></tr>")
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    regkeys = []
    for _, _, keys in REGULATORS:
        for k in keys:
            if k not in regkeys:
                regkeys.append(k)
    w("  " + src_line(regkeys))
    w("")
    w('  <h2 id="ssas-or-sipp">SSAS or SIPP: who is really in control?</h2>')
    w('  <div class="tablewrap">')
    w('    <table class="cmp">')
    w("      <thead><tr><th></th><th>SSAS</th><th>SIPP</th></tr></thead>")
    w("      <tbody>")
    for row, a, b in COMPARE:
        w(f"        <tr><td>{html.escape(row)}</td><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>")
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    w('  <p>More on this: <a href="/ssas-vs-sipp/">SSAS or SIPP?</a></p>')
    w("  " + src_line(COMPARE_SRC))
    w("")
    w('  <h2 id="questions">Common questions</h2>')
    for q, a, keys in QA:
        w(f"  <h3>{html.escape(q, quote=False)}</h3>")
        w(f"  <p>{html.escape(a, quote=False)}</p>")
        w("  " + src_line(keys))
    w("")
    w('  <div class="choice">')
    w("    <h2>A question about running a SSAS?</h2>")
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
