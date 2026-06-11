# aihubmix-image-gen-oss

An open-source WorkBuddy skill for generating images through the Aihubmix image generation API.

## Why This Exists

AI coding assistants like WorkBuddy can already generate text, code, and analysis—but most cannot generate images. This skill bridges that gap: it gives any WorkBuddy agent the ability to generate production-quality images directly in the conversation flow, without leaving the tool or opening external services.

## What Problem It Solves

**Before:** When users needed images during a WorkBuddy session, they had to:
1. Craft a prompt manually
2. Open a separate image generation service
3. Download the result
4. Drag it back into the conversation

**Now:** A single sentence triggers the entire pipeline. The agent generates the image, downloads it locally, and delivers it inline—all within the same chat.

## Use Cases

| Scenario | Example Prompt |
|---|---|
| E-commerce product images | "White-background smartwatch, blue lighting, premium" |
| Posters and banners | "Tech conference poster, neon blue, minimal text" |
| Icons and mascots | "A cyberpunk shrimp mascot, clean vector style" |
| Illustrations and concept art | "Futuristic city skyline, purple-orange sunset" |
| Rapid prototyping | "Three variations of a dark-mode SaaS landing page hero" |
| AI workflow automation | Agent needs a header image for a generated report |

## Models

| Model | Best For |
|---|---|
| `qwen-image-2.0` | Chinese prompts, posters, e-commerce, illustrations |
| `gpt-image-2-free` | General testing and free-model usage |
| `gemini-3-pro-image` | High-quality images, complex scenes, semantic detail |

Default: `qwen-image-2.0`

## Directory Structure

```
aihubmix-image-gen-oss/
├── SKILL.md
├── README.md
├── LICENSE
└── scripts/
    └── generate.py
```

## Installation

Copy this folder into your WorkBuddy skills directory.

Common user-level path:

```
~/.workbuddy/skills/aihubmix-image-gen-oss/
```

On Windows:

```
C:\Users\<your-user-name>\.workbuddy\skills\aihubmix-image-gen-oss\
```

Restart WorkBuddy after installation if the skill does not appear immediately.

## Configure API Key

This skill requires an Aihubmix API key. **Never put your key directly into source files.** Use the environment variable instead.

### Windows PowerShell

Temporary:

```powershell
$env:AIHUBMIX_API_KEY = "your-api-key-here"
```

Permanent:

```powershell
[Environment]::SetEnvironmentVariable("AIHUBMIX_API_KEY", "your-api-key-here", "User")
```

Restart your terminal or WorkBuddy after a permanent change.

Verify:

```powershell
echo $env:AIHUBMIX_API_KEY
```

### macOS / Linux

Temporary:

```bash
export AIHUBMIX_API_KEY="your-api-key-here"
```

Permanent: add the line above to `~/.bashrc` or `~/.zshrc`.

Verify:

```bash
echo "$AIHUBMIX_API_KEY"
```

## Usage

### CLI

```bash
python scripts/generate.py \
  --prompt "A futuristic blue technology poster" \
  --output-dir "./outputs/images" \
  --model "qwen-image-2.0" \
  --size "1024x1024" \
  --n 1
```

### Windows PowerShell One-Line

```powershell
python .\scripts\generate.py --prompt "A futuristic poster" --output-dir ".\outputs\images" --model "qwen-image-2.0" --size "1024x1024" --n 1
```

## Parameters

| Parameter | Required | Default | Description |
|---|---:|---|---|
| `--prompt` | Yes | — | Text prompt for image generation |
| `--output-dir` | Yes | — | Directory to save images |
| `--model` | No | `qwen-image-2.0` | Model to use |
| `--size` | No | `1024x1024` | Output image size |
| `--n` | No | `1` | Number of images |

## Example Prompts

```
A futuristic blue technology poster, clean background, premium product style
```

```
Chinese e-commerce hero image for a smartwatch, white background, blue gradient
```

```
A cute robot shrimp mascot, cyberpunk neon blue, minimal icon style
```

## Security Notes

Do not put your API key into:

- `SKILL.md`
- `README.md`
- `scripts/generate.py`
- Git commits
- Screenshots

Use the `AIHUBMIX_API_KEY` environment variable instead.

## Troubleshooting

### Missing API Key

```
Error: Missing AIHUBMIX_API_KEY environment variable
```

**Fix:** Set the environment variable and restart your terminal.

### 401 / 403

The API key may be invalid, expired, or missing permission.

### Unsupported Model

```
Error: Unsupported model: xxx. Supported: gemini-3-pro-image, gpt-image-2-free, qwen-image-2.0
```

**Fix:** Use one of `qwen-image-2.0`, `gpt-image-2-free`, or `gemini-3-pro-image`.

### PowerShell Line Break Error

PowerShell uses backtick (`` ` ``), not `^`, for line continuation:

```powershell
python .\scripts\generate.py `
  --prompt "A futuristic poster" `
  --output-dir ".\outputs\images" `
  --model "qwen-image-2.0"
```

The one-line command is the safest approach if you are unsure.

## License

MIT — see [LICENSE](LICENSE).
