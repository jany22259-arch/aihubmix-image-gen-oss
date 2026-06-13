"""
Aihubmix Image Generation OSS Script.

Reads the API key from AIHUBMIX_API_KEY and calls:
https://aihubmix.com/v1/images/generations

Supported models:
- qwen-image-2.0
- gpt-image-2
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


BASE_URL = "https://aihubmix.com/v1"
ENDPOINT = "/images/generations"

SUPPORTED_MODELS = {
    "qwen-image-2.0",
    "gpt-image-2",
}


def safe_filename(text: str, suffix: str = "png") -> str:
    keep: list[str] = []

    for ch in text[:40]:
        if ch.isalnum() or ch in "-_":
            keep.append(ch)
        elif ch.isspace():
            keep.append("_")

    stem = "".join(keep).strip("_") or "aihubmix_image"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stem}_{timestamp}.{suffix}"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix

    for i in range(1, 1000):
        candidate = path.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"Unable to create unique file name for: {path}")


def download_url(url: str, output_path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "aihubmix-image-gen-oss"})

    with urllib.request.urlopen(req, timeout=120) as resp:
        output_path.write_bytes(resp.read())


def request_generation(
    api_key: str,
    prompt: str,
    model: str,
    size: str,
    n: int,
) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": n,
    }

    req = urllib.request.Request(
        BASE_URL + ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Aihubmix API HTTP {exc.code}: {body[:1000]}"
        ) from exc


def generate_image(
    prompt: str,
    output_dir: str,
    model: str = "qwen-image-2.0",
    size: str = "1024x1024",
    n: int = 1,
) -> list[str]:
    api_key = os.getenv("AIHUBMIX_API_KEY")
    if not api_key:
        raise RuntimeError("Missing AIHUBMIX_API_KEY environment variable")

    if model not in SUPPORTED_MODELS:
        supported = ", ".join(sorted(SUPPORTED_MODELS))
        raise ValueError(f"Unsupported model: {model}. Supported models: {supported}")

    if n < 1:
        raise ValueError("--n must be >= 1")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = request_generation(
        api_key=api_key,
        prompt=prompt,
        model=model,
        size=size,
        n=n,
    )

    data = result.get("data", [])
    if not data:
        sanitized = json.dumps(result, ensure_ascii=False)[:1000]
        raise RuntimeError(f"No image data returned: {sanitized}")

    files: list[str] = []

    for index, item in enumerate(data, start=1):
        output_path = out_dir / safe_filename(prompt, "png")

        if n > 1:
            output_path = output_path.with_name(
                f"{output_path.stem}_{index}{output_path.suffix}"
            )

        output_path = ensure_unique_path(output_path)

        if "url" in item:
            download_url(item["url"], output_path)
        elif "b64_json" in item:
            output_path.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            raise RuntimeError(f"Unsupported image response item: {item!r}")

        files.append(str(output_path))

    return files


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate images through Aihubmix API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output-dir", required=True, help="Directory to save images")
    parser.add_argument("--model", default="qwen-image-2.0", help="Image model")
    parser.add_argument("--size", default="1024x1024", help="Image size")
    parser.add_argument("--n", type=int, default=1, help="Number of images")

    args = parser.parse_args()

    files = generate_image(
        prompt=args.prompt,
        output_dir=args.output_dir,
        model=args.model,
        size=args.size,
        n=args.n,
    )

    print(json.dumps({"files": files}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
