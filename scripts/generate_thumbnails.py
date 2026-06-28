#!/usr/bin/env python3
"""Generate optimized image and thumbnails for artwork folders.

Finds the first image in the provided directory (or current dir) and
creates: image.jpg (optimized), image-thumb.jpg (smaller), image.webp.
"""
from pathlib import Path
from PIL import Image
import sys


def find_source_image(folder: Path):
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.tiff", "*.webp"):
        for p in folder.glob(ext):
            return p
    return None


def make_image(src: Path, out: Path, max_width: int, quality: int = 85, webp: bool = False):
    img = Image.open(src)
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        img = background
    else:
        img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        new_h = int(max_width * h / w)
        img = img.resize((max_width, new_h), Image.LANCZOS)

    out.parent.mkdir(parents=True, exist_ok=True)
    if webp:
        img.save(out, "WEBP", quality=quality, method=6)
    else:
        img.save(out, "JPEG", quality=quality, optimize=True)


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("everything/example-artwork")
    if not folder.exists():
        print("Folder not found:", folder)
        sys.exit(2)

    src = find_source_image(folder)
    if not src:
        print("No source image found in", folder)
        sys.exit(3)

    print("Using source:", src.name)
    make_image(src, folder / "image.jpg", max_width=1200, quality=85)
    make_image(src, folder / "image-thumb.jpg", max_width=600, quality=80)
    make_image(src, folder / "image.webp", max_width=1200, quality=80, webp=True)
    print("Wrote: image.jpg, image-thumb.jpg, image.webp")


if __name__ == '__main__':
    main()
