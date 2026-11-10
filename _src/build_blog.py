#!/usr/bin/env python3
"""Build Steve's 2022 blog posts, the withdrawn post notice, /blog/ and the two old category pages.

Old WordPress addresses are kept exactly (GitHub Pages cannot redirect).
Post text lives in blog_posts.py, copied word for word from the live site on 5 October 2026.
"""
import html
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blog_posts import POSTS, WITHDRAWN, NOTE_SOURCES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
SITE = "https://my-ssas.co.uk"
UPDATED_ISO = "2026-10-05"
FEES = "/ssas-pension-table-showing-best-ssas-providers/"
ORDER = ["autumn-statement-2022-salary-sacrifice-salary-exchange-better-than-ever",
         "business-owners-missing-out-on-billions-form-government",
         "ssas-for-business-survive-or-thrive"]
CATEGORIES = {"general-news": "General News", "ssas-for-business": "SSAS for business"}

PERSON = {"@type": "Person", "@id": SITE + "/#steve-hunt", "name": "Steve Hunt",
          "alternateName": ["Steve Hunt ACII TEP", "Stephen Hunt"], "honorificSuffix": "ACII TEP", "url": SITE + "/about/"}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "My SSAS", "publishingPrinciples": SITE + "/sources-and-corrections/", "inLanguage": "en-GB",
           "publisher": {"@id": SITE + "/#steve-hunt"}}

EXTRA_CSS = """
  .crumbs { font-size: 14px; color: var(--muted); margin: 14px 0 0; }
  h3 { font-size: 19px; line-height: 1.35; margin: 24px 0 6px; }
  .post blockquote { margin: 12px 0; padding: 10px 16px; border-left: 4px solid var(--teal); background: var(--soft); }
  .post ol ol { list-style: lower-alpha; }
  .post li { margin-bottom: 8px; }
  .post p, .post li, .post a { overflow-wrap: anywhere; }
  .post table.post { min-width: 0; max-width: 560px; }
  .note2026 { background: #fff8e1; border-left: 4px solid #e0a800; padding: 10px 14px; border-radius: 4px; font-size: 16px; }
  .changed { border: 2px solid var(--teal); border-radius: 8px; padding: 6px 18px 12px; background: var(--soft); }
  .changed ul { padding-left: 20px; }
  .changed li { margin: 10px 0; }
  p.src { font-size: 14px; color: var(--muted); margin: 4px 0 0; word-break: break-word; }
  p.src .lead { font-weight: 700; margin-right: 4px; }
  p.src .lbl { font-weight: 600; }
  ul.posts { padding-left: 20px; }
  ul.posts li { margin-bottom: 14px; }
  .small { font-size: 14px; color: var(--muted); }
"""


def link(title, url):
    t = html.escape(title, quote=False)
    if url.startswith("http"):
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{t}</a>'
    return f'<a href="{html.escape(url)}">{t}</a>'


def src_line(keys):
    groups = OrderedDict()
    for k in keys:
        label, title, url = NOTE_SOURCES[k]
        groups.setdefault(label, []).append(link(title, url))
    parts = [f'<span class="lbl">{html.escape(l)}:</span> ' + "; ".join(v) for l, v in groups.items()]
    return '<p class="src"><span class="lead">Sources</span> ' + " &middot; ".join(parts) + "</p>"


def parts():
    home = HOME.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", home, re.S).group(0).replace("</style>", EXTRA_CSS + "</style>")
    header = re.search(r"<header>.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
    return style, header, footer


def page(path, title, description, graph, body_lines, noindex=False, og_type="article"):
    style, header, footer = parts()
    url = SITE + path
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    o = ["<!doctype html>", '<html lang="en-GB">', "<head>", '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f"<title>{html.escape(title, quote=False)}</title>",
         f'<meta name="description" content="{html.escape(description)}">']
    if noindex:
        o.append('<meta name="robots" content="noindex, follow">')
    o += [f'<link rel="canonical" href="{url}">', f'<meta property="og:type" content="{og_type}">',
          '<meta property="og:site_name" content="My SSAS">',
          f'<meta property="og:title" content="{html.escape(title.split(" | ")[0])}">',
          f'<meta property="og:description" content="{html.escape(description)}">',
          f'<meta property="og:url" content="{url}">',
          '<script type="application/ld+json">', ld, "</script>", style, "</head>", "<body>", header, "", "<main>"]
    o += body_lines
    o += ["</main>", "", footer, "</body>", "</html>"]
    text = "\n".join(o) + "\n"
    assert "—" not in text and "–" not in text, path
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


def build_post(slug, p):
    path = f"/{slug}/"
    graph = [WEBSITE, PERSON,
             {"@type": "BlogPosting", "@id": SITE + path + "#post", "headline": p["title"], "description": p["description"],
              "datePublished": p["date_iso"], "dateModified": UPDATED_ISO, "inLanguage": "en-GB",
              "author": {"@id": SITE + "/#steve-hunt"}, "publisher": {"@id": SITE + "/#steve-hunt"},
              "mainEntityOfPage": SITE + path, "isPartOf": {"@id": SITE + "/#website"}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                 {"@type": "ListItem", "position": 3, "name": p["title"], "item": SITE + path}]}]
    b = []
    w = b.append
    w(f'  <p class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {html.escape(p["title"])}</p>')
    w(f"  <h1>{html.escape(p['title'])}</h1>")
    w(f'  <p class="byline">By Steve Hunt &middot; Written {p["date"]}</p>')
    w('  <div class="answer">')
    w(f'    <p><strong>Archived opinion piece, written in {p["month"]}.</strong> Its figures, examples and calls to action are historical, not current recommendations. Please do not use them to decide whether to set up a SSAS, move money into one, or invest through one.</p>')
    w('    <p>Some rules and figures have changed since. See <a href="#changed">what has changed</a> at the end of this post, and the <a href="/faq/">SSAS pension FAQ</a> for today&rsquo;s rules.</p>')
    w("  </div>")
    w('  <div class="post">')
    w(re.sub(r'<a href="mailto:[^"]*">(.*?)</a>', r'\1', p["body"].strip()))
    w("  </div>")
    w("")
    w(f'  <h2 id="changed">What has changed since {p["month"]}</h2>')
    w('  <div class="changed">')
    w("    <ul>")
    for text, keys in p["notes"]:
        w(f"      <li>{html.escape(text, quote=False)}{src_line(keys)}</li>")
    w("    </ul>")
    w('    <p class="small">Typing errors in the original post were corrected in October 2026.</p>')
    w("  </div>")
    w("")
    w('  <div class="choice">')
    w("    <h2>A question about SSAS pensions?</h2>")
    w('    <p>Ask Steve a question about SSAS pensions. Your question goes to Steve, who will get back to you. You can also read <a href="/blog/">more posts</a> or the <a href="/faq/">SSAS pension FAQ</a>.</p>')
    w('    <a class="ask" href="/contact/">Ask Steve a question about SSAS pensions</a>')
    w("  </div>")
    return page(path, f"{p['title']} | My SSAS", p["description"], graph, b)


def build_withdrawn():
    path = f"/{WITHDRAWN['slug']}/"
    graph = [WEBSITE, PERSON,
             {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": "Post withdrawn",
              "dateModified": UPDATED_ISO, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"}}]
    b = [
        '  <p class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; Post withdrawn</p>',
        "  <h1>This post has been withdrawn</h1>",
        '  <div class="answer">',
        f"    <p>This page used to hold &ldquo;{html.escape(WITHDRAWN['title'])}&rdquo;, an opinion piece Steve wrote in November 2022. It included views about whether some people should transfer out of final salary pensions. This site does not give pension transfer advice, so the post has been withdrawn.</p>",
        "  </div>",
        '  <p>For the current rules, see <a href="/faq/#can-i-move-a-final-salary-pension-into-a-ssas">Can I move a final salary pension into a SSAS?</a> in the FAQ.</p>',
        '  <p>You can also read <a href="/blog/">Steve&rsquo;s other posts</a>, or <a href="/contact/">ask Steve a question about SSAS pensions</a>.</p>',
    ]
    return page(path, "Post withdrawn | My SSAS", "This 2022 blog post has been withdrawn. See the FAQ for the current rules.", graph, b,
                noindex=True, og_type="website")


def post_list(slugs):
    lines = ['  <ul class="posts">']
    for s in slugs:
        p = POSTS[s]
        lines.append(f'    <li><a href="/{s}/">{html.escape(p["title"])}</a><br><span class="small">Written {p["date"]}. {html.escape(p["description"])}</span></li>')
    lines.append(f'    <li><a href="{FEES}">SSAS provider fees compared, 2026</a><br><span class="small">Steve&rsquo;s 2022 provider cost table, &ldquo;SSAS Pension: which one is best for your business&rdquo;, now rebuilt with every provider&rsquo;s 2026 fees.</span></li>')
    lines.append("  </ul>")
    return lines


def build_blog_index():
    path = "/blog/"
    graph = [WEBSITE, PERSON,
             {"@type": "Blog", "@id": SITE + path + "#blog", "url": SITE + path, "name": "My SSAS blog",
              "author": {"@id": SITE + "/#steve-hunt"}, "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"},
              "blogPost": [{"@id": f"{SITE}/{s}/#post"} for s in ORDER]},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + path}]}]
    b = ['  <p class="crumbs"><a href="/">Home</a> &rsaquo; Blog</p>',
         "  <h1>Blog</h1>",
         '  <div class="answer">',
         '    <p>Steve&rsquo;s opinion pieces, written in 2022. Some rules and figures have changed since, so each post ends with a note on what has changed, with sources. For the current rules, see the <a href="/faq/">SSAS pension FAQ</a>.</p>',
         "  </div>"]
    b += post_list(ORDER)
    return page(path, "Blog | My SSAS", "Steve Hunt's 2022 opinion pieces on SSAS pensions and salary sacrifice, each with a note on what has changed since.",
                graph, b, og_type="website")


def build_category(slug, name):
    path = f"/category/{slug}/"
    graph = [WEBSITE, PERSON,
             {"@type": "CollectionPage", "@id": SITE + path + "#page", "url": SITE + path, "name": name,
              "inLanguage": "en-GB", "isPartOf": {"@id": SITE + "/#website"}}]
    slugs = [s for s in ORDER if name in POSTS[s]["categories"]]
    b = [f'  <p class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {html.escape(name)}</p>',
         f"  <h1>{html.escape(name)}</h1>",
         '  <p>Posts in this category. All of Steve&rsquo;s posts are also on the <a href="/blog/">blog page</a>.</p>']
    b += post_list(slugs)
    return page(path, f"{name} | My SSAS", f"Blog posts in the {name} category.", graph, b, noindex=True, og_type="website")


def main():
    built = [build_post(s, POSTS[s]) for s in ORDER]
    built.append(build_withdrawn())
    built.append(build_blog_index())
    built += [build_category(s, n) for s, n in CATEGORIES.items()]
    for b in built:
        print("built", b.relative_to(ROOT))


if __name__ == "__main__":
    main()
