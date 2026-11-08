# Rev F drawings and test-piece solids

The scripts that draw the Rev F sheets on the blueprints page and build the
test-piece solids in `/downloads`. Everything is read from one parameter
file, `src/hcsa_params_revF.json`, so a change there moves every sheet.

- `src/hcsa_params_revF.json` — the Rev F parameters with their status
  (LOCKED, DECIDED, PROPOSAL_APPLIED, STUDY) and the date of each decision.
- `src/parts_lib.py` — the CadQuery generator behind the parts library
  (`/parts`): P-01 to P-14 and the assemblies. Writes STEP, STL and SVG views.
- `testpieces/build_testpieces.py` — the T1 slices (75, 150, 225), the 550 mm
  article with the dummy hardpoint at both fitting depths, the pull blocks and
  the F-01 to F-03 fixture, as STEP, STL and assemblies, plus `testpieces.json`
  with the bill of materials.
- `testpieces/sheets_testpieces.py` — sheets TP-00 to TP-04 (A3 PDF and PNG)
  from the solids and `testpieces.json`.
- `flight/sheets_flight_revF.py` — sheets RF-05 to RF-09 (A3 PDF and PNG).

Run, from this folder, with Python 3.11+, `cadquery`, `matplotlib`, `numpy`,
`Pillow` installed (and `rsvg-convert` for the SVG views):

    python testpieces/build_testpieces.py
    python testpieces/sheets_testpieces.py
    python flight/sheets_flight_revF.py

Then convert the PDFs for the website with
`python scripts/static-pages/convert_revf_sheets.py <pdf> revf <sheet ids>`
and regenerate the pages with `python scripts/static-pages/gen_pages.py`.

The sheets are drawn from the parameters, not traced from CAD, and are not
checked for machining. Sheets RF-01 to RF-04 of 5 November were drawn
separately and are kept as the PDF in `/downloads`.

## The release package and the Rev F parts

- `package/` — the text parts of the release package for Marco Cross (markdown, parts 0 to 7), the
  stills from the model's taken-apart view (`img/`) and `build_package.py`, which turns them into the
  package PDF with the A3 sheets from `public/downloads` interleaved: `python package/build_package.py`
  (or `... draft` for a dated draft). Needs google-chrome, qpdf, pypdf, reportlab and markdown.
- `parts_revF/` — the CadQuery builders for the 8 Nov parts (CB-01, CB-02, HP-01, HP-01M, HP-02,
  HP-03, P-11, P-07 at 21 mm, PL-01, A-03, A-04) and the script that put them on the parts page;
  `README.md` lists every clash and departure from the brief. Outputs live in `public/parts`.
