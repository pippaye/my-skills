#!/usr/bin/env python3
"""Inspect an image for faithful draw.io reconstruction.

The script reports image dimensions and extracts a simple palette. It also
supports exact point and region color sampling.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

from PIL import Image


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def load_rgb(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.alpha_composite(image)
    return background.convert("RGB")


def point_color(image: Image.Image, x: int, y: int) -> str:
    width, height = image.size
    x = max(0, min(width - 1, x))
    y = max(0, min(height - 1, y))
    return to_hex(image.getpixel((x, y)))


def region_color(image: Image.Image, x0: int, y0: int, x1: int, y1: int) -> str:
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    width, height = image.size
    x0 = max(0, min(width - 1, x0))
    x1 = max(0, min(width - 1, x1))
    y0 = max(0, min(height - 1, y0))
    y1 = max(0, min(height - 1, y1))

    pixels = list(image.crop((x0, y0, x1 + 1, y1 + 1)).getdata())
    if not pixels:
        return "#000000"
    count = len(pixels)
    rgb = tuple(round(sum(pixel[i] for pixel in pixels) / count) for i in range(3))
    return to_hex(rgb)  # type: ignore[arg-type]


def palette(image: Image.Image, color_count: int) -> list[tuple[str, float]]:
    sample = image.copy()
    sample.thumbnail((240, 240))

    # Pillow quantization avoids a sklearn dependency while giving stable,
    # good-enough structural colors for diagrams.
    quantized = sample.quantize(colors=max(1, color_count), method=Image.Quantize.MEDIANCUT)
    palette_values = quantized.getpalette() or []
    data = quantized.get_flattened_data() if hasattr(quantized, "get_flattened_data") else quantized.getdata()
    counts = Counter(data)
    total = sum(counts.values()) or 1

    result: list[tuple[str, float]] = []
    for index, count in counts.most_common(color_count):
        offset = index * 3
        rgb = tuple(palette_values[offset : offset + 3])
        if len(rgb) == 3:
            result.append((to_hex(rgb), count / total * 100.0))  # type: ignore[arg-type]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect an image for draw.io reconstruction.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--point", nargs=2, type=int, metavar=("X", "Y"))
    parser.add_argument("--region", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    parser.add_argument("--colors", type=int, default=8)
    args = parser.parse_args()

    if not args.image.exists():
        print(f"Image not found: {args.image}", file=sys.stderr)
        return 1

    image = load_rgb(args.image)
    width, height = image.size

    if args.point:
        print(point_color(image, args.point[0], args.point[1]))
        return 0

    if args.region:
        print(region_color(image, *args.region))
        return 0

    print(f"size_px: {width} x {height}")
    print(f"aspect_ratio: {width / height:.4f}")
    print(f'drawio_page_reference: "0 0 {width} {height}"')
    print("palette:")
    for hex_color, percent in palette(image, args.colors):
        print(f"  {hex_color}  {percent:5.1f}%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
