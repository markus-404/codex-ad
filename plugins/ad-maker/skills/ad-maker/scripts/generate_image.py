#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
from pathlib import Path


RATIO_TO_SIZE = {
    "1:1": "1024x1024",
    "4:5": "1024x1280",
    "9:16": "1152x2048",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or edit images from compiled ad-maker prompt JSON.")
    parser.add_argument("--prompt-json", required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--ratio", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--quality", default="medium")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mode", choices=["generate", "edit"], default="generate")
    parser.add_argument("--mask")
    return parser.parse_args()


def load_prompt(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(file_path.read_text())


def effective_prompt(prompt_data: dict) -> str:
    """Fold the negative prompt into the prompt text.

    The OpenAI Images API (gpt-image-2) has no `negative_prompt` body param, so
    the carefully-built negative constraints must be expressed inside the prompt
    to actually reach the model.
    """
    prompt = prompt_data["prompt"]
    negative = (prompt_data.get("negative_prompt") or "").strip()
    if negative:
        prompt = f"{prompt}\n\nAvoid the following:\n{negative}"
    return prompt


def api_request_from_args(args: argparse.Namespace, prompt_data: dict) -> dict:
    """Build exactly the request body sent to the OpenAI Images API.

    Only keys the API actually accepts are included, so a --dry-run reflects the
    real call. Edit requests attach `image` (and optional `mask`) as file
    uploads and do not send `quality`.
    """
    if args.ratio not in RATIO_TO_SIZE:
        raise ValueError(f"Unsupported ratio: {args.ratio}")
    if not 1 <= args.count <= 10:
        raise ValueError("--count must be between 1 and 10 (OpenAI Images API n range).")
    request = {
        "model": args.model,
        "prompt": effective_prompt(prompt_data),
        "size": RATIO_TO_SIZE[args.ratio],
        "n": args.count,
    }
    if args.mode == "generate":
        request["quality"] = args.quality
    else:
        request["image"] = [ref.get("path", "") for ref in prompt_data.get("image_refs", [])]
        if args.mask:
            request["mask"] = args.mask
    return request


def save_b64_images(items: list, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(items, start=1):
        b64_json = getattr(item, "b64_json", None)
        if b64_json is None and isinstance(item, dict):
            b64_json = item.get("b64_json")
        if not b64_json:
            raise ValueError("Image response item did not include b64_json")
        (out_dir / f"image-{index:03d}.png").write_bytes(base64.b64decode(b64_json))


def run_real_request(args: argparse.Namespace, prompt_data: dict, request: dict) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required unless --dry-run is set.")
    from openai import OpenAI

    client = OpenAI()
    out_dir = Path(args.out_dir)
    if args.mode == "generate":
        response = client.images.generate(
            model=request["model"],
            prompt=request["prompt"],
            size=request["size"],
            quality=request["quality"],
            n=request["n"],
        )
        save_b64_images(response.data, out_dir)
        return

    image_refs = prompt_data.get("image_refs", [])
    if not image_refs:
        raise ValueError("Edit mode requires at least one image_ref")
    for ref in image_refs:
        if not Path(ref.get("path", "")).exists():
            raise FileNotFoundError(f"Missing reference image: {ref.get('path', '')}")
    image_files = [open(ref["path"], "rb") for ref in image_refs]
    mask_file = open(args.mask, "rb") if args.mask else None
    try:
        kwargs = {
            "model": request["model"],
            "prompt": request["prompt"],
            "image": image_files,
            "size": request["size"],
            "n": request["n"],
        }
        if mask_file:
            kwargs["mask"] = mask_file
        response = client.images.edit(**kwargs)
        save_b64_images(response.data, out_dir)
    finally:
        for file in image_files:
            file.close()
        if mask_file:
            mask_file.close()


def main() -> int:
    args = parse_args()
    try:
        prompt_data = load_prompt(args.prompt_json)
        request = api_request_from_args(args, prompt_data)
        if args.dry_run:
            dry_run = {
                "mode": args.mode,
                "endpoint": "images.generate" if args.mode == "generate" else "images.edit",
                "api_request": request,
            }
            print(json.dumps(dry_run, indent=2, ensure_ascii=False))
            return 0
        run_real_request(args, prompt_data, request)
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
