---
name: aihubmix-image-gen-oss
description: >
  Generate images through the Aihubmix image generation API and save them locally.
  Supports qwen-image-2.0, gpt-image-2, and gemini-3-pro-image.
  Use this skill when the user asks for image generation, text-to-image,
  posters, illustrations, e-commerce product images, icons, or visual concept art.
---

# Aihubmix Image Generation OSS Skill

Generate images with Aihubmix-compatible image models and save the results as local files.

## Supported Models

| Model | Recommended Use |
|---|---|
| `qwen-image-2.0` | Chinese prompts, posters, e-commerce images, illustrations |
| `gpt-image-2` | General testing and free-model usage |
| `gemini-3-pro-image` | High-quality images, complex scenes, strong semantic understanding |

Default model: `qwen-image-2.0`

## Requirements

- Python 3.8+
- A valid Aihubmix API key
- Environment variable:

```bash
AIHUBMIX_API_KEY
```

Never hardcode the API key in any file.

## Basic Usage

Run:

```bash
python scripts/generate.py \
  --prompt "A futuristic blue tech poster, clean composition, high detail" \
  --output-dir "./outputs/images" \
  --model "qwen-image-2.0" \
  --size "1024x1024" \
  --n 1
```

Windows PowerShell:

```powershell
python .\scripts\generate.py --prompt "A futuristic blue tech poster, clean composition, high detail" --output-dir ".\outputs\images" --model "qwen-image-2.0" --size "1024x1024" --n 1
```

## Environment Variable Setup

### macOS / Linux

```bash
export AIHUBMIX_API_KEY="your-api-key-here"
```

To make it permanent, add the line above to your shell profile, such as `~/.bashrc` or `~/.zshrc`.

### Windows PowerShell

Temporary:

```powershell
$env:AIHUBMIX_API_KEY = "your-api-key-here"
```

Permanent user-level setting:

```powershell
[Environment]::SetEnvironmentVariable("AIHUBMIX_API_KEY", "your-api-key-here", "User")
```

After setting it permanently, restart the terminal or the host application.

## Workflow for Agents

When using this skill:

1. Extract the user's image prompt.
2. Use `qwen-image-2.0` by default unless the user specifies a model.
3. Validate the model is one of:
   - `qwen-image-2.0`
   - `gpt-image-2`
   - `gemini-3-pro-image`
4. Check that `AIHUBMIX_API_KEY` exists.
5. Run `scripts/generate.py`.
6. Save output to `{workspace}/outputs/images/` unless the user specifies another safe location.
7. Return generated file paths to the user.
8. If possible, present the generated image file directly.

## Security Rules

- Never hardcode API keys.
- Never print the full API key.
- Never commit `.env` files containing secrets.
- Never write generated files outside the active workspace unless the user explicitly approves.
- Do not delete, move, or overwrite user files.
- If a filename already exists, generate a unique timestamped name.

## Failure Handling

| Error | Action |
|---|---|
| Missing `AIHUBMIX_API_KEY` | Ask the user to configure the environment variable |
| 401 / 403 | Ask the user to verify API key and account permissions |
| Unknown model | Show supported models and ask the user to choose again |
| Empty response | Show a sanitized response summary |
| Timeout | Retry once; stop and report if it fails again |
