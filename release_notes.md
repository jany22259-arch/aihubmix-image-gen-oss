## v1.0.4

### Gemini route restored

Gemini is not compatible with `/v1/images/generations` on Aihubmix. It must use `/v1/chat/completions` with multimodal output:

- `qwen-image-2.0` → `/v1/images/generations`
- `gpt-image-2` → `/v1/images/generations`
- `gemini-3-pro-image` → `/v1/chat/completions` + `modalities=["text", "image"]`

### Changes

- Restored `gemini-3-pro-image` support.
- Added dual routing in `scripts/generate.py`.
- Added `--aspect-ratio` for Gemini route.
- Added parser for Gemini `inline_data` / multimodal response.
- Kept gpt-image-2 premium/slow/rate-limit notes.

### Install

```
Help me install this skill: https://github.com/jany22259-arch/aihubmix-image-gen-oss
```

Or download `shengtu.skill` below.
