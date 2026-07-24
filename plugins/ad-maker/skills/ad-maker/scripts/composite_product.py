#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Composite a real product PNG over a generated background.")
    parser.add_argument("--background", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--x", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def composite(background_path: str, product_path: str, x: int, y: int, width: int, out_path: str) -> None:
    if width <= 0:
        raise ValueError("--width must be greater than zero")
    background = Image.open(background_path).convert("RGBA")
    product = Image.open(product_path).convert("RGBA")
    ratio = width / product.width
    height = round(product.height * ratio)
    product = product.resize((width, height), Image.LANCZOS)
    background.alpha_composite(product, dest=(x, y))
    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    background.save(output, format="PNG")


def main() -> int:
    args = parse_args()
    try:
        composite(args.background, args.product, args.x, args.y, args.width, args.out)
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
