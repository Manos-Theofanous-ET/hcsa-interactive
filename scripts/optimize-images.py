"""Build web-sized WebP copies of the gallery images.

Reads the originals in public/assets/{images,blueprints,prototype} and writes
two sizes into public/assets/web/: `<name>.webp` (max 1800 px, lightbox) and
`<name>-thumb.webp` (max 720 px, grid). Idempotent: skips outputs that are
newer than their source.

    pip install pillow
    python scripts/optimize-images.py
"""
from pathlib import Path

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = Path(__file__).resolve().parent.parent / "public" / "assets"
OUT = ROOT / "web"
SIZES = {"": 1800, "-thumb": 720}

# Left out of the gallery on purpose: broken or placeholder renders.
#   cutaway / exterior_hero / shield_family: shading failed (beige blob)
#   docking_family: untextured grey close-up
#   page-15: still shows a "[URL/QR PLACEHOLDER]" line
SKIP = {
    "images/HCSA_cutaway_hero_orbit.png",
    "images/HCSA_exterior_hero_nominal.png",
    "images/HCSA_shield_family_deployed.png",
    "images/HCSA_docking_family_nominal.png",
    "blueprints/page-15.png",
}


def load(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    # concept-plants.png is truncated: the bottom rows decode as black.
    # Crop to the last row that has real content.
    if src.name == "concept-plants.png":
        bbox = im.point(lambda v: 255 if v > 8 else 0).getbbox()
        if bbox:
            im = im.crop((0, 0, im.width, bbox[3]))
    return im


def slug(p: Path) -> str:
    return p.stem.lower().replace(" ", "-").replace(".", "-")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for folder in ("images", "blueprints", "prototype"):
        for src in sorted((ROOT / folder).iterdir()):
            if src.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue
            if f"{folder}/{src.name}" in SKIP:
                continue
            name = f"{folder}-{slug(src)}"
            for suffix, size in SIZES.items():
                dst = OUT / f"{name}{suffix}.webp"
                if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                    continue
                im = load(src)
                im.thumbnail((size, size), Image.LANCZOS)
                im.save(dst, "WEBP", quality=80, method=6)
                print(f"{dst.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}  {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
