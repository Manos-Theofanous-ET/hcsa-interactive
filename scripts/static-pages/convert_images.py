"""Convert the dimensioned Rev S drawings (PNG) into WebP for /blueprints.
Source folders are the CAD repo's img/ and img_dim/; run from the site root:
  python scripts/static-pages/convert_images.py <path-to-hcsa/simple>"""
import json, os, sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "../hcsa/simple"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "public", "blueprints", "img")
os.makedirs(OUT, exist_ok=True)
data = json.load(open(os.path.join(HERE, "blueprints-data.json")))

def files_for(kind, name):
    if kind == "2d_sketch":
        return [("2d_sketch", os.path.join(SRC, "img", "2d_sketch", name + ".png"))]
    if kind == "2d_render":
        return [("2d_render", os.path.join(SRC, "img_dim", "2d_render", name + ".png"))]
    return [("3d_sketch", os.path.join(SRC, "img_dim", "3d_sketch", name + ".png")),
            ("3d_render", os.path.join(SRC, "img_dim", "3d_render", name + ".png"))]

sizes = {}
for subj, kind, name, note in data["pages"]:
    for k, path in files_for(kind, name):
        im = Image.open(path).convert("RGB")
        stem = f"{k}-{name}"
        for suffix, width, q in (("", 1800, 80), ("-thumb", 720, 72)):
            w = min(width, im.width)
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, stem + suffix + ".webp"), "WEBP", quality=q, method=6)
            if suffix == "-thumb":
                sizes[stem] = [w, h]
json.dump(sizes, open(os.path.join(HERE, "image-sizes.json"), "w"), indent=0)
print(len(sizes), "images")
