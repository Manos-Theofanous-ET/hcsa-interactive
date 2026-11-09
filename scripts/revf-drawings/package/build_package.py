"""Assemble the Rev F release package PDF for Marco Cross (run from anywhere; paths are relative to this file).

Text parts (markdown) become A4 pages through Chrome; the A3 sheet PDFs are interleaved behind
their part; page numbers go on the A4 pages; bookmarks on every part and sheet.

    python build_package.py            -> out/HCSA_RevF_release_package_<date>.pdf
"""
import datetime as dt, html, io, os, re, subprocess, sys
import markdown
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # the repo root
DL = os.path.join(SITE, "public", "downloads")
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
DRAFT = len(sys.argv) > 1 and sys.argv[1] == "draft"
DATE = "draft of 9 November 2026" if DRAFT else "12 November 2026"
STAMP = "draft_9Nov2026" if DRAFT else "12Nov2026"

SHEETS_RF14 = os.path.join(DL, "HCSA-Rev-F-sheets-RF-01-to-RF-04-5-Nov-2026.pdf")
SHEETS_RF59 = os.path.join(DL, "HCSA-Rev-F-sheets-RF-05-to-RF-09-9-Nov-2026.pdf")
SHEETS_TP = os.path.join(DL, "HCSA-Rev-F-test-pieces-TP-00-to-TP-04-9-Nov-2026.pdf")

# (bookmark title, markdown file or None, list of (sheet pdf, [sheet names]) to append after the text)
PARTS = [
    ("0. Read this first", os.path.join(HERE, "00_read_first.md"), []),
    ("1. The facility", os.path.join(HERE, "01_facility.md"), []),
    ("2. The flight parts, drawn and in 3D", os.path.join(HERE, "02_flight_parts.md"),
     [(SHEETS_RF14, ["RF-01 Ribs", "RF-02 Seam and gland", "RF-03 T1 articles (superseded by TP)", "RF-04 Transfer lock"]),
      (SHEETS_RF59, ["RF-05 Seam section and z' table", "RF-06 Hexagon GA", "RF-07 Hardpoint fitting", "RF-08 Corner node", "RF-09 Pentagon GA"])]),
    ("3. The test pieces", os.path.join(HERE, "03_test_pieces.md"),
     [(SHEETS_TP, ["TP-00 Cover, tolerances, parts list", "TP-01 Frame B", "TP-02 Frame A and assembled", "TP-03 550 article", "TP-04 Pull blocks and fixture"])]),
    ("4. What the computer tests say", os.path.join(HERE, "04_computer_tests.md"), []),
    ("5. What is still open, by subsystem", os.path.join(HERE, "05_open_items.md"), []),
    ("6. For the call with Marco", os.path.join(HERE, "06_questions.md"), []),
    ("7. Where everything lives", os.path.join(HERE, "07_where.md"), []),
    ("Appendix. Marco's points worked with numbers", os.path.join(HERE, "A1_marcos_points.md"), []),
]

CSS = """
@page { size: A4; margin: 18mm 18mm 20mm 18mm; }
html { font-size: 10.6pt; }
body { font-family: Georgia, 'DejaVu Serif', serif; color: #1a1a1a; line-height: 1.42; margin: 0; }
h1 { font-size: 20pt; font-weight: 600; margin: 0 0 10pt; letter-spacing: -0.01em; }
h2 { font-size: 13.5pt; font-weight: 600; margin: 16pt 0 6pt; page-break-after: avoid; }
h3 { font-size: 11.5pt; font-weight: 600; margin: 12pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 7pt; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 7pt 1.2em; padding: 0; }
li { margin: 0 0 3pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9.2pt; line-height: 1.3; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { text-align: left; font-weight: 600; border-bottom: 1.2pt solid #1a1a1a; padding: 3pt 6pt 3pt 0; vertical-align: bottom; }
td { border-bottom: 0.5pt solid #bbb; padding: 3pt 6pt 3pt 0; vertical-align: top; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; }
em.still { display: block; border: 0.8pt dashed #999; padding: 18pt 10pt; margin: 8pt 0; color: #666; font-style: normal; text-align: center; }
.part { page-break-before: always; }
.part:first-child { page-break-before: auto; }
.eyebrow { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; letter-spacing: 0.08em; text-transform: uppercase; color: #666; margin: 0 0 6pt; }
.cover { height: 240mm; display: flex; flex-direction: column; justify-content: space-between; }
.cover h1 { font-size: 30pt; line-height: 1.1; margin-top: 60mm; }
.cover .sub { font-size: 13pt; color: #444; }
.cover table { width: auto; font-size: 10pt; }
.cover td { border: 0; padding: 2pt 18pt 2pt 0; }
.toc td { border-bottom: 0.5pt solid #ddd; }
.footer-note { font-size: 9pt; color: #666; }
figure { margin: 8pt 0 10pt; page-break-inside: avoid; }
figure img { width: 100%; display: block; border-radius: 3pt; }
figure.half { width: 48.5%; display: inline-block; vertical-align: top; margin-right: 2%; }
figure.half + figure.half { margin-right: 0; }
figcaption { font-size: 8.8pt; color: #555; margin-top: 4pt; line-height: 1.35; }
"""

MD = markdown.Markdown(extensions=["tables", "sane_lists"])


def md_to_html(path):
    text = open(path, encoding="utf-8").read()
    # [STILL: ...] placeholders become dashed boxes
    text = re.sub(r"^\[STILL: (.*?)\]\s*$", lambda m: f'<em class="still">Still from the model: {html.escape(m.group(1))}</em>', text, flags=re.M)
    MD.reset()
    out = MD.convert(text)
    return out.replace('src="img/', f'src="file://{HERE}/img/')


def cover_html(toc_rows):
    toc = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>" for a, b in toc_rows)
    return f"""
<div class="cover">
<div><p class="eyebrow">Human-Centric Space Habitat, Brown University</p>
<h1>HCSA Rev F release package</h1>
<p class="sub">The facility taken apart, every flight part drawn and in 3D, the test pieces with their shop drawings and STEP files, what the computer tests found, and what is still open.</p></div>
<div><table>
<tr><td>For</td><td>Marco Cross, fabrication and feasibility review, Friday 13 November 2026, 1:00, and Rick Fleeter</td></tr>
<tr><td>From</td><td>Manos Theofanous and the HCSA team</td></tr>
<tr><td>Date</td><td>{DATE}</td></tr>
<tr><td>Replaces</td><td>The Master Document of 27 October 2026 (Rev E)</td></tr>
<tr><td>Status</td><td>Working baseline. Nothing in it is released for manufacture; the test pieces are for quotation</td></tr>
</table></div>
</div>
<div class="part">
<p class="eyebrow">Contents</p>
<table class="toc">{toc}</table>
<p class="footer-note">The sheets are A3 and follow the text of their part. Page numbers are on the text pages; the sheets carry their own title blocks.</p>
</div>"""


def chrome_pdf(html_path, pdf_path):
    cmd = ["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf_path}", f"file://{html_path}"]
    subprocess.run(cmd, check=True, capture_output=True, timeout=180)


def number_pages(reader_pages, start, total_text_pages):
    """Overlay 'page n' at the foot of each A4 page. Returns list of pages."""
    out = []
    for i, page in enumerate(reader_pages):
        n = start + i
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(18 * 72 / 25.4, 11 * 72 / 25.4, "HCSA Rev F release package, " + DATE)
        c.drawRightString(A4[0] - 18 * 72 / 25.4, 11 * 72 / 25.4, f"{n}")
        c.save(); buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
        out.append(page)
    return out


def main():
    # 1. each text part -> its own PDF, so sheets can be interleaved
    text_pdfs = []
    for title, md_path, sheets in PARTS:
        body = md_to_html(md_path)
        page_html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
        hp = os.path.join(OUT, re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_') + ".html")
        pp = hp[:-5] + ".pdf"
        open(hp, "w", encoding="utf-8").write(page_html)
        chrome_pdf(hp, pp)
        text_pdfs.append(pp)
        print(title, "->", len(PdfReader(pp).pages), "pages")

    # 2. assemble, numbering the text pages
    writer = PdfWriter()
    page_no = 1
    toc_rows = []
    # cover + contents are built after we know page numbers, so first pass: compute
    plan = []  # (title, text pdf, sheets)
    for (title, md_path, sheets), pp in zip(PARTS, text_pdfs):
        plan.append((title, pp, sheets))

    # count pages to fill the contents table: cover (2 pages) first
    page_counter = 3
    for title, pp, sheets in plan:
        toc_rows.append((title, f"page {page_counter}"))
        page_counter += len(PdfReader(pp).pages)
        for spdf, names in sheets:
            for nm in names:
                toc_rows.append(("    Sheet " + nm, "A3, after part " + title.split(".")[0]))
            page_counter += len(PdfReader(spdf).pages)

    cover_path_html = os.path.join(OUT, "cover.html")
    open(cover_path_html, "w", encoding="utf-8").write(
        f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cover_html(toc_rows)}</body></html>")
    cover_pdf = os.path.join(OUT, "cover.pdf")
    chrome_pdf(cover_path_html, cover_pdf)
    cover_pages = PdfReader(cover_pdf).pages
    for p in number_pages(list(cover_pages), 1, 0):
        writer.add_page(p)
    page_no = len(cover_pages) + 1
    writer.add_outline_item("Cover and contents", 0)

    for title, pp, sheets in plan:
        start_index = len(writer.pages)
        pages = number_pages(list(PdfReader(pp).pages), page_no, 0)
        for p in pages:
            writer.add_page(p)
        page_no += len(pages)
        parent = writer.add_outline_item(title, start_index)
        for spdf, names in sheets:
            r = PdfReader(spdf)
            for p, nm in zip(r.pages, names):
                idx = len(writer.pages)
                writer.add_page(p)
                writer.add_outline_item("Sheet " + nm, idx, parent=parent)
            page_no += len(r.pages)

    writer.add_metadata({"/Title": "HCSA Rev F release package", "/Author": "Manos Theofanous, HCSA team, Brown University",
                         "/Subject": "Release of drawings for the fabrication review with Marco Cross, 13 Nov 2026"})
    final = os.path.join(OUT, f"HCSA_RevF_release_package_{STAMP}.pdf")
    raw = final[:-4] + "_raw.pdf"
    with open(raw, "wb") as f:
        writer.write(f)
    # qpdf recompresses the streams (pypdf writes them loosely); halves the file
    subprocess.run(["qpdf", "--compress-streams=y", "--object-streams=generate", "--recompress-flate", "--compression-level=9", raw, final], check=True)
    os.remove(raw)
    print("wrote", final, len(writer.pages), "pages,", round(os.path.getsize(final) / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
