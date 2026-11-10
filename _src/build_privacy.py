#!/usr/bin/env python3
"""Build /privacy-policy/index.html for my-ssas.co.uk (template parts copied from the home page).

Retention: 2 years after the last contact (Steve's decision, 5 October 2026).
CHECK at Formspree sign-up: that Formspree's data processing terms cover UK data (UK Addendum or IDTA).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "privacy-policy" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/privacy-policy/"
UPDATED = "10 November 2026"
UPDATED_ISO = "2026-11-10"
GDPR = "https://www.legislation.gov.uk/eur/2016/679/article/"
# Formspree's Security page, read by Steve on 10 November 2026: "We rely on Standard Contractual Clauses (SCCs) as a data processor."
# Formspree's pages do not say whether its clauses carry the UK Addendum. When Formspree confirms, change this line to
# the exact UK mechanism (for example "the EU standard contractual clauses with the UK Addendum").
FORMSPREE_SAFEGUARD = "Formspree says it relies on standard contractual clauses"

PURPOSES = [
    ("To answer your question or your SSAS Test answers, and to contact you about them",
     "Legitimate interests: Steve's interest in answering the questions people send him, and yours in getting an answer"),
    ("To pass your details to another firm, if you want help that this site does not give",
     "Your consent. You can withdraw it at any time"),
    ("To keep a record in case of a later question, complaint or legal claim",
     "Legitimate interests"),
    ("To help Steve read, sort and draft replies, using AI tools",
     "Legitimate interests, using only the information reasonably needed"),
    ("To count visits to the site, so it can be improved",
     "Legitimate interests, with a simple way to opt out (see the cookie policy)"),
]

PROVIDERS = [
    ("Formspree, Inc.", "runs the form, and keeps a copy of each form sent", "USA (Amazon Web Services)", FORMSPREE_SAFEGUARD),
    ("Google", "Gmail, one of the email accounts that receives enquiries", "USA and other countries", "the UK Extension to the EU-US Data Privacy Framework"),
    ("Microsoft", "Microsoft 365, for the other email accounts that receive enquiries", "USA and other countries", "the UK Extension to the EU-US Data Privacy Framework"),
    ("Cloudflare, Inc.", "counts visits to the site, without cookies", "USA and other countries", "the EU standard contractual clauses with the UK Addendum"),
    ("Anthropic Ireland, Limited", "Claude, the AI assistant Steve may use to help him read, sort and draft replies", "USA and other countries", "Anthropic says it relies on adequacy decisions or standard contractual clauses"),
]

SOURCES = [
    ("Law", [
        ("UK GDPR, Article 6: lawful bases", GDPR + "6"),
        ("UK GDPR, Article 13: what people must be told", GDPR + "13"),
        ("UK GDPR, Articles 15 to 22: your rights", GDPR + "15"),
        ("UK GDPR, Article 77: complaints to the ICO", GDPR + "77"),
        ("Data Protection Act 2018, s.164A: complaints to the controller", "https://www.legislation.gov.uk/ukpga/2018/12/section/164A"),
        ("The Data Protection (Adequacy) (United States of America) Regulations 2023", "https://www.legislation.gov.uk/uksi/2023/1028/contents/made"),
    ]),
    ("Provider evidence", [
        ("Formspree: security", "https://formspree.io/security/"),
        ("Google: privacy frameworks", "https://policies.google.com/privacy/frameworks?hl=en-GB"),
        ("Microsoft: privacy statement", "https://www.microsoft.com/en-gb/privacy/privacystatement"),
        ("Cloudflare: privacy policy", "https://www.cloudflare.com/privacypolicy/"),
        ("Anthropic: privacy policy", "https://www.anthropic.com/legal/privacy"),
    ]),
]


def ext(url, text):
    return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(text, quote=False)}</a>'


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  ul.plain { padding-left: 20px; }
  ul.plain li { margin-bottom: 8px; }
  table.pp { min-width: 0; }
  table.pp td, table.pp th { vertical-align: top; }
  @media (max-width: 600px) { table.pp { font-size: 15px; } }
  .srclist h3 { font-size: 18px; }
  .srclist ul { font-size: 14px; word-break: break-word; padding-left: 20px; }
  .srclist li { margin-bottom: 4px; }
</style>""")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)

    graph = [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
         "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/"},
        {"@type": "WebPage", "@id": PAGE_URL + "#webpage", "url": PAGE_URL, "name": "Privacy policy",
         "dateModified": UPDATED_ISO, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"},
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Privacy policy", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>Privacy policy | My SSAS</title>")
    w('<meta name="description" content="How My SSAS uses your details when you ask Steve a question or take the SSAS Test: who sees them, where they go, how long they are kept, and your rights.">')
    w(f'<link rel="canonical" href="{PAGE_URL}">')
    w('<script type="application/ld+json">')
    w(ld)
    w("</script>")
    w(style)
    w("</head>")
    w("<body>")
    w(header)
    w("")
    w("<main>")
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; Privacy policy</p>')
    w("  <h1>Privacy policy</h1>")
    w(f'  <p class="byline">Last updated {UPDATED}</p>')
    w('  <div class="answer">')
    w("    <p>This policy explains what happens to your details when you visit this site or ask Steve a question. Your details go to Steve and Lisa Newmark, so Steve can answer you. Two of the email accounts that receive them are provided by Eadon &amp; Co Ltd, trading as Raven Wealth. We do not sell your details. We will not pass them to another firm for advice or other services unless you agree.</p>")
    w("  </div>")
    w("")
    w('  <h2 id="who">Who is responsible</h2>')
    w("  <p>Steve Hunt ACII TEP runs my-ssas.co.uk and decides how your details are used. In data protection law, that makes him the controller. In this policy, &ldquo;we&rdquo; means Steve.</p>")
    w('  <p>Contact Steve at Stable Cottage, Water Lane, South Witham, Grantham, Lincolnshire NG33 5PH, by email at <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a>, or on <a href="tel:+441733602071">01733 602 071</a>.</p>')
    w("")
    w('  <h2 id="what">What we collect</h2>')
    w('  <ul class="plain">')
    w("    <li><strong>When you use the form or the SSAS Test:</strong> your name and email address, and anything else you choose to give us. That can be your phone number, the best time to call, your business name, your question and your SSAS Test answers.</li>")
    w("    <li><strong>When you email or phone Steve:</strong> what you tell him.</li>")
    w('    <li><strong>When you visit the site:</strong> visit counts, from Cloudflare Web Analytics, which uses no cookies. See the <a href="/cookie-policy/">cookie policy</a>.</li>')
    w("  </ul>")
    w("  <p>Please do not send health information, or other sensitive personal information, through this site.</p>")
    w("")
    w('  <h2 id="why">Why we use your details</h2>')
    w('  <div class="tablewrap">')
    w('    <table class="pp">')
    w("      <thead><tr><th>Why</th><th>The legal reason</th></tr></thead>")
    w("      <tbody>")
    for why, basis in PURPOSES:
        w(f"        <tr><td>{html.escape(why)}</td><td>{html.escape(basis)}</td></tr>")
    w("      </tbody>")
    w("    </table>")
    w("  </div>")
    w("")
    w('  <h2 id="recipients">Who sees your details</h2>')
    w('  <ul class="plain">')
    w("    <li>Steve Hunt, and Lisa Newmark, his administrator.</li>")
    w("    <li>Eadon &amp; Co Ltd, trading as Raven Wealth. Two of the email accounts that receive enquiries, Steve&rsquo;s and Lisa&rsquo;s work accounts, are held on its email system.</li>")
    w("    <li>Anthropic Ireland, Limited, if Steve uses its AI assistant, Claude, to help with your enquiry. Anthropic then acts as a separate controller, under its own privacy policy.</li>")
    w("    <li>Another firm, but only if you agree. For example, a regulated financial adviser, a SSAS provider or a life cover firm. Steve will tell you which firm before he passes anything on.</li>")
    w("    <li>The service providers that run the form, the email accounts and the visit counts, listed below.</li>")
    w("    <li>Anyone the law requires us to share them with.</li>")
    w("  </ul>")
    w("")
    w('  <h2 id="providers">Where your details go, and the safeguards</h2>')
    w("  <p>These organisations keep or handle data outside the UK. Each one relies on a legal safeguard for that.</p>")
    w('  <ul class="plain">')
    for name, does, where, safeguard in PROVIDERS:
        w(f"    <li><strong>{html.escape(name)}:</strong> {html.escape(does)}. Where: {html.escape(where)}. Safeguard: {html.escape(safeguard)}.</li>")
    w("  </ul>")
    w("  <p>UK law treats transfers to US companies that have joined the UK Extension to the EU-US Data Privacy Framework as adequately protected. For UK data, contract safeguards can use the UK International Data Transfer Agreement, or the EU standard contractual clauses with the UK Addendum. You can ask Steve for a copy of the safeguards used for any transfer.</p>")
    w("")
    w('  <h2 id="how-long">How long we keep your details</h2>')
    w("  <p>We delete the enquiry records from this site 2 years after our last contact with you. That includes the Formspree copy and the email copies. The only exception is where the law requires us to keep something longer, or we need it for a legal claim.</p>")
    w("  <p>If you become a client of another firm, that firm keeps its own records under its own privacy rules. If you ask us to delete your details sooner, we will, where the law gives you that right.</p>")
    w("")
    w('  <h2 id="rights">Your rights</h2>')
    w("  <p>You can ask to see your details, to correct them or to delete them. You can also ask us to limit how we use them, or object to how we use them. Where the right applies, you can ask for a copy to take elsewhere. If you gave your consent, you can withdraw it at any time.</p>")
    w('  <p>To use any of these rights, email <a href="mailto:steve@my-ssas.co.uk">steve@my-ssas.co.uk</a>. We will normally reply within one month. If the law allows us longer, we will tell you. No decision about you is made by a computer alone.</p>')
    w("")
    w('  <h2 id="must-i">Do you have to give us your details?</h2>')
    w("  <p>No. But Steve needs a way to contact you, to answer your question.</p>")
    w("")
    w('  <h2 id="complaints">Complaints</h2>')
    w('  <p>You have the right to complain to Steve about how your personal data is handled. You can do this by email, by post or using the <a href="/contact/">contact form</a>. He will acknowledge your complaint within 30 days. He will then look into it, and tell you the outcome without undue delay.</p>')
    w(f'  <p>You can also complain to the Information Commissioner&rsquo;s Office (ICO): {ext("https://ico.org.uk/make-a-complaint/", "ico.org.uk/make-a-complaint")}, or call 0303 123 1113.</p>')
    w("")
    w('  <h2 id="changes">Changes to this policy</h2>')
    w("  <p>We will update this page if anything changes. The date at the top shows the latest version.</p>")
    w("")
    w('  <h2 id="sources">Sources</h2>')
    w('  <div class="srclist">')
    for label, items in SOURCES:
        w(f"  <h3>{html.escape(label)}</h3>")
        w("  <ul>")
        for title, url in items:
            w(f"    <li>{ext(url, title)}</li>")
        w("  </ul>")
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
    if FORMSPREE_SAFEGUARD.startswith("["):
        print("WARNING: Formspree safeguard is still a placeholder. Confirm it at sign-up before go-live.")


if __name__ == "__main__":
    main()
