#!/usr/bin/env python3
"""Optional pixel-level comparison for source and exported preview images.

This is not part of the default img2drawio workflow. Use it only when the user
asks for pixel-level diff output or when a stricter visual debugging pass is
worth the extra artifacts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a source image and rendered preview.")
    parser.add_argument("source", type=Path)
    parser.add_argument("rendered", type=Path)
    parser.add_argument("out_prefix", type=Path)
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGB")
    rendered = Image.open(args.rendered).convert("RGB")
    if rendered.size != source.size:
        rendered = rendered.resize(source.size)

    width, height = source.size
    side = Image.new("RGB", (width * 2 + 20, height), (245, 245, 245))
    side.paste(source, (0, 0))
    side.paste(rendered, (width + 20, 0))
    side.save(str(args.out_prefix) + "_side.png")

    Image.blend(source, rendered, 0.5).save(str(args.out_prefix) + "_overlay.png")

    difference = ImageChops.difference(source, rendered)
    diff_array = np.asarray(difference).astype(float)
    magnitude = diff_array.max(axis=2)
    if magnitude.max() > 0:
        magnitude = magnitude / magnitude.max() * 255.0
    Image.fromarray(magnitude.astype("uint8")).save(str(args.out_prefix) + "_diff.png")

    mean_error = float(np.asarray(difference).mean())
    print(f"side: {args.out_prefix}_side.png")
    print(f"overlay: {args.out_prefix}_overlay.png")
    print(f"diff: {args.out_prefix}_diff.png")
    print(f"mean_pixel_error: {mean_error:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
