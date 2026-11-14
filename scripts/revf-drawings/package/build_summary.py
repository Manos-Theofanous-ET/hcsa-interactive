"""One-page summary of the release package -> out/HCSA_RevF_release_package_one_page_summary_<date>.pdf"""
import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STAMP = sys.argv[1] if len(sys.argv) > 1 else "9Nov2026"   # read before sys.argv is reset for build_package
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_package.py"))
bp = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(bp)
body = bp.md_to_html(os.path.join(HERE, "summary_one_page.md"))
css = (bp.CSS.replace("html { font-size: 10.6pt; }", "html { font-size: 9.4pt; }")
       .replace("@page { size: A4; margin: 18mm 18mm 20mm 18mm; }", "@page { size: A4; margin: 12mm 16mm 12mm 16mm; }")
       .replace("h2 { font-size: 13.5pt; font-weight: 600; margin: 16pt 0 6pt;", "h2 { font-size: 11pt; font-weight: 600; margin: 8pt 0 3pt;")
       .replace("h1 { font-size: 20pt;", "h1 { font-size: 16pt;"))
html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{css} p{{margin:0 0 4.5pt}}</style></head><body>{body}"
        "</body></html>")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
hp = os.path.join(HERE, "out", "summary.html"); open(hp, "w").write(html)
pdf = os.path.join(HERE, "out", f"HCSA_RevF_release_package_one_page_summary_{STAMP}.pdf")
bp.chrome_pdf(hp, pdf)
from pypdf import PdfReader
n = len(PdfReader(pdf).pages); print(pdf, n, "page(s)")
if n != 1: sys.exit("not one page")
