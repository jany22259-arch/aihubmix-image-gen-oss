"""
Aihubmix Image Generation — save generated images locally.

Routes:
- qwen-image-2.0 / gpt-image-2 / wan2.7-image-pro / doubao-seedream-5.0-lite: /v1/images/generations
- gemini-3-pro-image: /v1/chat/completions with multimodal output

Reads AIHUBMIX_API_KEY from environment.
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
from typing import Any


BASE_URL = "https://aihubmix.com/v1"
IMAGE_ENDPOINT = "/images/generations"
CHAT_ENDPOINT = "/chat/completions"

IMAGE_ENDPOINT_MODELS = {
    "qwen-image-2.0",
    "gpt-image-2",
    "wan2.7-image-pro",
    "doubao-seedream-5.0-lite",
}

CHAT_IMAGE_MODELS = {
    "gemini-3-pro-image",
}

SUPPORTED_MODELS = IMAGE_ENDPOINT_MODELS | CHAT_IMAGE_MODELS


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


def post_json(api_key: str, endpoint: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    req = urllib.request.Request(
        BASE_URL + endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Aihubmix API HTTP {exc.code}: {body[:1000]}") from exc


def download_url(url: str, output_path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        output_path.write_bytes(resp.read())


def extract_inline_images(value: Any) -> list[str]:
    images: list[str] = []

    if isinstance(value, dict):
        inline_data = value.get("inline_data")
        if isinstance(inline_data, dict) and isinstance(inline_data.get("data"), str):
            images.append(inline_data["data"])

        if isinstance(value.get("b64_json"), str):
            images.append(value["b64_json"])

        for child in value.values():
            images.extend(extract_inline_images(child))

    elif isinstance(value, list):
        for item in value:
            images.extend(extract_inline_images(item))

    return images


def generate_via_images_endpoint(
    api_key: str,
    prompt: str,
    output_dir: Path,
    model: str,
    size: str,
    n: int,
) -> list[str]:
    payload = {"model": model, "prompt": prompt, "size": size, "n": n}
    result = post_json(api_key, IMAGE_ENDPOINT, payload, timeout=700)

    data = result.get("data", [])
    if not data:
        sanitized = json.dumps(result, ensure_ascii=False)[:1000]
        raise RuntimeError(f"No image data returned: {sanitized}")

    files: list[str] = []
    for index, item in enumerate(data, start=1):
        output_path = output_dir / safe_filename(prompt, "png")
        if n > 1:
            output_path = output_path.with_name(f"{output_path.stem}_{index}{output_path.suffix}")
        output_path = ensure_unique_path(output_path)

        if "url" in item:
            download_url(item["url"], output_path)
        elif "b64_json" in item:
            output_path.write_bytes(base64.b64decode(item["b64_json"]))
        else:
            raise RuntimeError(f"Unsupported image response item: {item!r}")

        files.append(str(output_path))

    return files


def generate_via_chat_endpoint(
    api_key: str,
    prompt: str,
    output_dir: Path,
    model: str,
    aspect_ratio: str,
) -> list[str]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"aspect_ratio={aspect_ratio}"},
            {"role": "user", "content": [{"type": "text", "text": prompt}]},
        ],
        "modalities": ["text", "image"],
    }
    result = post_json(api_key, CHAT_ENDPOINT, payload, timeout=700)

    image_payloads = extract_inline_images(result)
    if not image_payloads:
        sanitized = json.dumps(result, ensure_ascii=False)[:1000]
        raise RuntimeError(f"No inline image data returned from chat endpoint: {sanitized}")

    files: list[str] = []
    for index, image_b64 in enumerate(image_payloads, start=1):
        output_path = output_dir / safe_filename(prompt, "png")
        if len(image_payloads) > 1:
            output_path = output_path.with_name(f"{output_path.stem}_{index}{output_path.suffix}")
        output_path = ensure_unique_path(output_path)
        output_path.write_bytes(base64.b64decode(image_b64))
        files.append(str(output_path))

    return files


def generate_image(
    prompt: str,
    output_dir: str,
    model: str = "qwen-image-2.0",
    size: str = "1024x1024",
    n: int = 1,
    aspect_ratio: str = "1:1",
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

    if model in CHAT_IMAGE_MODELS:
        if n != 1:
            raise ValueError("Gemini chat image route currently supports --n 1 only")
        return generate_via_chat_endpoint(api_key, prompt, out_dir, model, aspect_ratio)

    return generate_via_images_endpoint(api_key, prompt, out_dir, model, size, n)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate images through Aihubmix API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output-dir", required=True, help="Directory to save images")
    parser.add_argument("--model", default="qwen-image-2.0", help="Image model")
    parser.add_argument("--size", default="1024x1024", help="Image size for image endpoint models")
    parser.add_argument("--n", type=int, default=1, help="Number of images for image endpoint models")
    parser.add_argument("--aspect-ratio", default="1:1", help="Gemini aspect ratio, e.g. 1:1, 2:3, 16:9")

    args = parser.parse_args()
    files = generate_image(
        prompt=args.prompt,
        output_dir=args.output_dir,
        model=args.model,
        size=args.size,
        n=args.n,
        aspect_ratio=args.aspect_ratio,
    )
    print(json.dumps({"files": files}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
