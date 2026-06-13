---
name: 生图图
displayName: 生图图
description: >
  Generate images via Aihubmix API (qwen-image-2.0, gpt-image-2, gemini-3-pro-image, wan2.7-image-pro, doubao-seedream-5.0-lite)
  and save output files to the workspace. qwen/gpt/wan/doubao use /images/generations;
  gemini uses /chat/completions multimodal route. Use when the user asks to create or generate images,
  especially with keywords like Aihubmix, 生图, 文生图, qwen-image, gpt-image, gemini-image,
  图片生成, 生成图片, 电商图, 海报, 插画, or any image-generation task.
---

# Aihubmix Image Generation

Generate images through Aihubmix and save files locally. qwen/gpt models use `/v1/images/generations`; Gemini image model uses `/v1/chat/completions` with multimodal output.

## Supported Models

| Model | Best For |
|---|---|
| `qwen-image-2.0` | 中文提示词、电商图、海报、插画 |
| `gpt-image-2` | Highest quality, precise editing, best face preservation. Slow (5min+), timeout >=10min. Rate limit (403) possible |
| `gemini-3-pro-image` | Gemini multimodal image route. Supports aspect ratio via `--aspect-ratio`; uses `/chat/completions`, not `/images/generations` |
| `wan2.7-image-pro` | Wan image generation model via `/images/generations`; use when user requests Wan/万相/通义系生图 |
| `doubao-seedream-5.0-lite` | Doubao Seedream lightweight image model via `/images/generations`; use for fast/cost-effective image generation |

Default: `qwen-image-2.0`

## Security

- **Never hardcode API keys.** Read only from env var `AIHUBMIX_API_KEY`.
- Never print or log the full API key.
- Default output: `{workspace}/outputs/images/`
- Never write files outside the workspace without explicit user approval.
- Do NOT delete, move, or overwrite any existing user files.
- If a target filename already exists, append a timestamp suffix.

## Workflow

When the user requests image generation:

1. Confirm or infer the image prompt.
2. Use `qwen-image-2.0` by default. Let the user override.
3. Validate the model is in `{qwen-image-2.0, gpt-image-2, gemini-3-pro-image, wan2.7-image-pro, doubao-seedream-5.0-lite}`.
4. Check `AIHUBMIX_API_KEY` env var. If missing, ask the user to set it.
5. Run the generation script (`scripts/generate.py`).
6. Save images to `{workspace}/outputs/images/`.
7. Return the generated file paths. Attach viewable files when possible.

## CLI Usage

```bash
python scripts/generate.py \
  --prompt "<prompt>" \
  --output-dir "<workspace>/outputs/images" \
  --model "qwen-image-2.0" \
  --size "1024x1024" \
  --n 1
```

Parameters:
- `--prompt` (required): Image description
- `--output-dir` (required): Where to save generated files
- `--model`: One of `qwen-image-2.0`, `gpt-image-2`, `gemini-3-pro-image`, `wan2.7-image-pro`, `doubao-seedream-5.0-lite`
- `--size`: Image size for qwen/gpt image endpoint models, default `1024x1024`
- `--n`: Number of images for qwen/gpt image endpoint models, default `1`
- `--aspect-ratio`: Gemini aspect ratio, default `1:1`; supports `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Failure Handling

| Error | Action |
|---|---|
| Missing `AIHUBMIX_API_KEY` | Ask user to configure environment variable |
| 401 / 403 | Ask user to verify API key or account permissions |
| Unknown model | List supported models; ask user to confirm |
| Empty response data | Show sanitized API response summary |
| Timeout | Retry once; stop on second failure |
