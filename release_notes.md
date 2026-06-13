## v1.0.5

### New Models

Added two image-generation models via `/v1/images/generations`:

- `wan2.7-image-pro`
- `doubao-seedream-5.0-lite`

### Current routing

| Model | Route |
|---|---|
| `qwen-image-2.0` | `/v1/images/generations` |
| `gpt-image-2` | `/v1/images/generations` |
| `wan2.7-image-pro` | `/v1/images/generations` |
| `doubao-seedream-5.0-lite` | `/v1/images/generations` |
| `gemini-3-pro-image` | `/v1/chat/completions` multimodal route |

### Notes

- `wan2.7-image-pro` and `doubao-seedream-5.0-lite` are treated as standard image endpoint models.
- Gemini remains on the chat multimodal route because Aihubmix does not accept Gemini through `/images/generations`.

### Install

```
Help me install this skill: https://github.com/pipixia-run/aihubmix-image-gen-oss
```

Or download `shengtu.skill` below.
