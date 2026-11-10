#!/usr/bin/env python3
"""Build /cookie-policy/index.html for my-ssas.co.uk (template parts copied from the home page).

Visit counting: Cloudflare Web Analytics, relying on PECR Schedule A1 para 5 (statistical purposes, from 5 February 2026).
The opt-out button stores one flag (localStorage key below). At go-live, STATS_LOADER is added to every page,
with Steve's Cloudflare token, so the beacon only loads when the flag is not set and no Global Privacy Control signal is sent.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
OUT = ROOT / "cookie-policy" / "index.html"
SITE = "https://my-ssas.co.uk"
PAGE_URL = SITE + "/cookie-policy/"
UPDATED = "5 October 2026"
UPDATED_ISO = "2026-10-05"
FLAG = "mySsasNoStats"
PECR = "https://www.legislation.gov.uk/uksi/2003/2426/"
ICO_EXC = "https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/"

# Added to every page at go-live (replace CF_TOKEN with the token from Steve's Cloudflare account).
STATS_LOADER = """<script>
(function () {
  try {
    if (navigator.globalPrivacyControl) return;
    if (localStorage.getItem('%s') === '1') return;
    var s = document.createElement('script');
    s.defer = true;
    s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    s.setAttribute('data-cf-beacon', '{"token": "CF_TOKEN"}');
    document.head.appendChild(s);
  } catch (e) {}
})();
</script>""" % FLAG

OPT_OUT_JS = """<script>
(function () {
  var key = '%s';
  var status = document.getElementById('stats-status');
  function isOff() {
    try { return localStorage.getItem(key) === '1'; } catch (e) { return null; }
  }
  function show() {
    var off = isOff();
    if (off === null) {
      status.textContent = 'Your browser is blocking site storage, so this page cannot save your choice. Visit counting will not run while storage is blocked.';
    } else if (off) {
      status.textContent = 'Visit counting is switched off in this browser.';
    } else if (navigator.globalPrivacyControl) {
      status.textContent = 'Your browser sends a Global Privacy Control signal, so visit counting is switched off.';
    } else {
      status.textContent = 'Visit counting is switched on in this browser.';
    }
  }
  document.getElementById('stats-off').addEventListener('click', function () {
    try { localStorage.setItem(key, '1'); } catch (e) {}
    show();
  });
  document.getElementById('stats-on').addEventListener('click', function () {
    try { localStorage.removeItem(key); } catch (e) {}
    show();
  });
  show();
})();
</script>""" % FLAG

SOURCES = [
    ("Law", [
        ("PECR, regulation 6: storing or reading information on your device", PECR + "regulation/6"),
        ("PECR, Schedule A1, para 4 (strictly necessary) and para 5 (statistical purposes)", PECR + "schedule/A1"),
    ]),
    ("ICO", [
        ("Guidance on the use of storage and access technologies: what are the exceptions?", ICO_EXC),
    ]),
    ("Provider evidence", [
        ("Cloudflare Web Analytics", "https://cloudflare.com/web-analytics"),
        ("Cloudflare Web Analytics docs", "https://developers.cloudflare.com/web-analytics/about/"),
    ]),
]


def ext(url, text):
    return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(text, quote=False)}</a>'


def main():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  .optout { border: 2px solid var(--teal); border-radius: 8px; padding: 14px 18px; margin: 16px 0; background: var(--soft); }
  .optout p#stats-status { font-weight: 600; }
  .optout button { margin: 6px 10px 6px 0; }
  .optout button.plain { font: inherit; padding: 10px 16px; border-radius: 6px; border: 1px solid var(--teal); background: #fff; color: var(--teal-dark); cursor: pointer; }
  ul.plain { padding-left: 20px; }
  ul.plain li { margin-bottom: 4px; }
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
        {"@type": "WebPage", "@id": PAGE_URL + "#webpage", "url": PAGE_URL, "name": "Cookies and visit counts",
         "dateModified": UPDATED_ISO, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"},
         "publisher": {"@id": SITE + "/#steve-hunt"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Cookies", "item": PAGE_URL}]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    o = []
    w = o.append
    w("<!doctype html>")
    w('<html lang="en-GB">')
    w("<head>")
    w('<meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>Cookies and visit counts | My SSAS</title>")
    w('<meta name="description" content="My SSAS sets no cookies. It counts visits with Cloudflare Web Analytics, which uses no cookies, and you can switch the counting off on this page.">')
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
    w('  <p class="crumbs"><a href="/">Home</a> &rsaquo; Cookies</p>')
    w("  <h1>Cookies and visit counts</h1>")
    w(f'  <p class="byline">Last updated {UPDATED}</p>')
    w('  <div class="answer">')
    w("    <p>This site sets no cookies. It counts visits using Cloudflare Web Analytics, which Cloudflare says uses no cookies and does not track you as a person. You can switch the counting off on this page.</p>")
    w("  </div>")
    w("")
    w('  <h2 id="cookies">Cookies</h2>')
    w("  <p>This site does not set any cookies. It has no advertising, and it does not use Google Analytics.</p>")
    w("")
    w('  <h2 id="visit-counts">Visit counts</h2>')
    w("  <p>To see which pages help people, and to improve the site, we use Cloudflare Web Analytics. When a page loads, its script sends Cloudflare information such as:</p>")
    w('  <ul class="plain">')
    for item in ["the page you looked at", "the site that sent you here", "your browser and operating system, and the type of device", "how quickly the page loaded", "your country"]:
        w(f"    <li>{item}</li>")
    w("  </ul>")
    w("  <p>Cloudflare says it does not use cookies, browser storage or fingerprinting to identify visitors. We see statistics for the whole site, such as how many people read a page, broken down by things like country and browser. We use them only to improve the site, and Cloudflare handles them only to help us do that.</p>")
    w("")
    w('  <h2 id="no-banner">Why there is no cookie banner</h2>')
    w("  <p>Since 5 February 2026, the law has let a website count visits without asking first, if the only purpose is statistics to improve the site. The website must explain this clearly, and give you a simple, free way to say no. The counts must not be used to track or profile individual visitors. This site uses Cloudflare Web Analytics on that basis.</p>")
    w("")
    w('  <h2 id="switch-off">Switch off visit counting</h2>')
    w('  <div class="optout">')
    w('    <p id="stats-status">Visit counting can be switched off here. This needs JavaScript to be on in your browser.</p>')
    w('    <button class="ask" type="button" id="stats-off">Switch off visit counting</button>')
    w('    <button class="plain" type="button" id="stats-on">Switch it back on</button>')
    w("  </div>")
    w("  <p>Switching off saves one small note in your browser, so the counting stays off on this device. That note is used only to remember your choice, not for counting. Nothing else is stored. If you clear your browser data, or use another browser or device, you will need to switch it off again.</p>")
    w("  <p>If your browser sends a Global Privacy Control signal, we treat that as switching the counting off.</p>")
    w("")
    w('  <h2 id="forms">Sending a form</h2>')
    w('  <p>When you send a form, your browser goes to Formspree&rsquo;s website to confirm it was sent. Formspree&rsquo;s own cookie and privacy policies apply there. The <a href="/privacy-policy/">privacy policy</a> explains what happens to your details.</p>')
    w("")
    w('  <h2 id="links">Links to other sites</h2>')
    w("  <p>Links to other websites, such as GOV.UK and HMRC&rsquo;s manuals, take you to sites with their own cookie policies.</p>")
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
    w(OPT_OUT_JS)
    w("</body>")
    w("</html>")
    text = "\n".join(o) + "\n"
    assert "—" not in text and "–" not in text
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    (ROOT / "_src" / "stats_loader.html").write_text(STATS_LOADER + "\n", encoding="utf-8")
    print(f"built {OUT}, {len(text):,} chars; wrote _src/stats_loader.html for go-live")


if __name__ == "__main__":
    main()
