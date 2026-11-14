"""Convert the Rev F sheet PDFs (A3, one sheet per page) into WebP for /blueprints.

Usage, from the site root:
  python scripts/static-pages/convert_revf_sheets.py <pdf> <prefix> <sheet-id> [<sheet-id> ...]

For example:
  python scripts/static-pages/convert_revf_sheets.py \
      public/downloads/HCSA-Rev-F-sheets-RF-05-to-RF-09-8-Nov-2026.pdf revf rf-05 rf-06 rf-07 rf-08 rf-09

Page N of the PDF becomes public/blueprints/img/<prefix>-<sheet-id>.webp (2481 px wide, the size the
RF-01 to RF-04 sheets were published at) and <prefix>-<sheet-id>-thumb.webp (720 px wide). The thumb
sizes are recorded in image-sizes.json, which gen_pages.py reads. Needs pdftoppm (poppler) and Pillow.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "public", "blueprints", "img")
SIZES_PATH = os.path.join(HERE, "image-sizes.json")
FULL_W, THUMB_W = 2481, 720


def main(pdf, prefix, ids):
    os.makedirs(OUT, exist_ok=True)
    sizes = json.load(open(SIZES_PATH)) if os.path.exists(SIZES_PATH) else {}
    with tempfile.TemporaryDirectory() as tmp:
        # 150 dpi on A3 gives 2481 x 1754, the published size of the Rev F sheets.
        subprocess.run(["pdftoppm", "-r", "150", "-png", pdf, os.path.join(tmp, "p")], check=True)
        pages = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
        if len(pages) != len(ids):
            sys.exit(f"{pdf} has {len(pages)} pages but {len(ids)} sheet ids were given")
        for page, sid in zip(pages, ids):
            im = Image.open(os.path.join(tmp, page)).convert("RGB")
            stem = f"{prefix}-{sid}"
            for suffix, width, q in (("", FULL_W, 80), ("-thumb", THUMB_W, 72)):
                w = min(width, im.width)
                h = round(im.height * w / im.width)
                im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, stem + suffix + ".webp"), "WEBP", quality=q, method=6)
                if suffix == "-thumb":
                    sizes[stem] = [w, h]
            print(stem, im.size)
    json.dump(sizes, open(SIZES_PATH, "w"), indent=0)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
