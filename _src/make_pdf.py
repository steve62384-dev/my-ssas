#!/usr/bin/env python3
"""Make the fees PDF from the fee page.

The PDF sits at the address of the old November 2022 table, so old links still work.
Run this after any change to the fee page: python3 _src/make_pdf.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "ssas-pension-table-showing-best-ssas-providers" / "index.html").as_uri()
OUT = ROOT / "wp-content/uploads/2022/11/SSAS-pension-administrator-fees-based-on-My-SSAS-co-uk-research-at-November-2022-.pdf"

CSS = """
@page { size: A4; margin: 14mm 12mm; }
header nav, form, .hp { display: none !important; }
body { font-size: 13px; }
main { max-width: none !important; }
a { color: #0a5c63; }
.tablewrap { overflow: visible !important; }
table { min-width: 0 !important; font-size: 11.5px; }
.pdfnote { border: 2px solid #0e7c86; border-radius: 6px; padding: 8px 12px; margin: 10px 0 14px; background: #e6f4f5; font-size: 13px; }
h2 { break-after: avoid; }
tr { break-inside: avoid; }
.vat { font-size: 10px !important; }
.note { font-size: 12px !important; }
"""

NOTE = ("This PDF replaces the November 2022 table that used to be at this address. It is a copy of the page "
        "<a href='https://my-ssas.co.uk/ssas-pension-table-showing-best-ssas-providers/'>my-ssas.co.uk/ssas-pension-table-showing-best-ssas-providers</a>, "
        "with every fee checked on 5 and 6 October 2026. Fees change, so always ask the provider for its latest fees. "
        "General information only, not advice.")

FOOTER = ('<div style="font-size:8px;width:100%;text-align:center;color:#55656c;">My SSAS: SSAS provider fees compared, 2026. '
          'Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>')

OUT.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(SRC)
    pg.add_style_tag(content=CSS)
    pg.evaluate("""(note) => { const h = document.querySelector('main h1'); const d = document.createElement('div');
                   d.className = 'pdfnote'; d.innerHTML = note; h.insertAdjacentElement('afterend', d); }""", NOTE)
    pg.emulate_media(media="print")
    pg.pdf(path=str(OUT), format="A4", print_background=True, display_header_footer=True,
           header_template="<div></div>", footer_template=FOOTER,
           margin={"top": "14mm", "bottom": "16mm", "left": "12mm", "right": "12mm"})
    b.close()
print(OUT.name, OUT.stat().st_size, "bytes")
