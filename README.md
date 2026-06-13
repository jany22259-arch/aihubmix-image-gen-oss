# aihubmix-image-gen-oss

> 在 WorkBuddy 里一句话生成图片——不用切工具、不用另开网页、不用拖文件。

Generate images inside WorkBuddy with a single sentence. No tool switching, no external tabs, no drag-and-drop.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: WorkBuddy](https://img.shields.io/badge/Platform-WorkBuddy-6c5ce7)](https://workbuddy.ai)
[![Skills Standard](https://img.shields.io/badge/Skills-Agent%20Skills%20Standard-00b894)](https://agentskills.io)

---

## Quick Start · 快速开始

### 安装 · Install

在 WorkBuddy 里说一句话就能安装：

```
帮我安装这个 skill：https://github.com/jany22259-arch/aihubmix-image-gen-oss
```

或从 [Releases](https://github.com/jany22259-arch/aihubmix-image-gen-oss/releases) 下载 `shengtu.skill`，手动导入 WorkBuddy。

### 配置 · Configure

设置环境变量（只做一次）：

**Windows PowerShell**

```powershell
[Environment]::SetEnvironmentVariable("AIHUBMIX_API_KEY", "你的API密钥", "User")
```

**macOS / Linux**

```bash
echo 'export AIHUBMIX_API_KEY="你的API密钥"' >> ~/.bashrc && source ~/.bashrc
```

重启 WorkBuddy。

### 使用 · Use

在 WorkBuddy 里直接说：

```
用 aihubmix-image-gen-oss 生成一张蓝色科技风海报
```

```
Generate a cyberpunk city poster with neon blue lighting, model gpt-image-2
```

一句话，图片就生成了，保存在当前工程目录的 `outputs/images/` 下。

---

## Why This Exists · 为什么做这个

AI 助手可以写代码、做分析、写文档——但大多数不能生成图片。

每次需要配图，你得：
1. 想好 prompt
2. 打开另一个生图服务
3. 下载图片
4. 拖回 WorkBuddy

这个 skill 把这四步变成**一句话**。

灵感来自日常工作流：写报告要配图、做 PPT 要封面、做电商素材要主图——每次切工具都很烦。跑通了一个月，确实省事，决定开源。

---

## What It Does · 能干什么

| 能力 | 说明 |
|---|---|
| 文生图 | 输入中文/英文 prompt，输出 PNG 图片 |
| 多模型切换 | `qwen-image-2.0`（中文/电商）/ `gpt-image-2`（最高画质）/ `gemini-3-pro-image`（多模态路由） |
| 本地保存 | 图片自动存到 `outputs/images/` |
| 环境变量安全 | API Key 从 `AIHUBMIX_API_KEY` 读取，不写死 |
| 零依赖 | 只用 Python 标准库，不需要 pip install |
| 跨平台 | Windows / macOS / Linux 都能用 |

---

## Models · 模型选择

| 模型 | 适用场景 |
|---|---|
| `qwen-image-2.0`（默认） | 中文 prompt、电商主图、海报、插画 |
| `gpt-image-2` | 最高画质、精细编辑控制、最佳人脸保留。生成较慢（5min+），timeout 建议 >=10min。可能有频率限制（403） |
| `gemini-3-pro-image` | 走 `/v1/chat/completions` 多模态路由，不走 `/v1/images/generations`。支持 `--aspect-ratio` 控制比例 |

> 注意：Gemini 如果误走 `/images/generations` 会报 `Unknown name "prompt"`，这是路由格式问题，不是模型 ID 问题。

指定模型的对话示例：

```
Create a minimal icon of a robot shrimp, use model gpt-image-2
```

```
用 gemini-3-pro-image 生成达芬奇风格蝴蝶解剖草图，比例 2:3
```

---

## Use Cases · 使用场景

### 电商素材

```
生成一张智能手表电商主图，白色背景，蓝色渐变光效，高级感
```

### 海报 & Banner

```
Tech conference poster, dark background, neon blue geometric lines
```

### 图标 & Mascot

```
一只赛博朋克风格的皮皮虾吉祥物，极简线框图标，蓝紫渐变
```

### 插画 & 概念图

```
Future city skyline at sunset, purple-orange gradient, cinematic lighting
```

### 自动化报告配图

Agent 写完周报后，自动生成一张 AI 行业趋势封面图。

---

## Installation · 安装方式

### 方式一：一句安装（推荐）

在 WorkBuddy 中说：

```
帮我安装这个 skill：https://github.com/jany22259-arch/aihubmix-image-gen-oss
```

Agent 会自动 clone 到 `~/.workbuddy/skills/aihubmix-image-gen-oss/`。

### 方式二：下载 .skill 包

从 [GitHub Releases](https://github.com/jany22259-arch/aihubmix-image-gen-oss/releases) 下载最新的 `.skill` 文件，导入 WorkBuddy。

### 方式三：手动安装

```bash
# macOS / Linux
git clone https://github.com/jany22259-arch/aihubmix-image-gen-oss.git ~/.workbuddy/skills/aihubmix-image-gen-oss
```

```powershell
# Windows
git clone https://github.com/jany22259-arch/aihubmix-image-gen-oss.git $env:USERPROFILE\.workbuddy\skills\aihubmix-image-gen-oss
```

---

## Trigger Phrases · 触发方式

在 WorkBuddy 中说下面任意一句都会触发这个 skill：

| 触发语 | 示例 |
|---|---|
| 生成图片 / 生成一张图 | 生成一张蓝色科技风海报 |
| 用 aihubmix 生成 | 用 aihubmix 生成一个猫咪图标 |
| Create an image / Generate an image | Generate a cyberpunk poster |
| 文生图 | 文生图：极简白底智能手表 |
| 电商主图 / 海报 / 图标 / 插画 | 做一张电商主图，白色背景，蓝色光效 |
| 指定模型生成 | 用 gpt-image-2 生成一张城市夜景 |

---

## CLI Usage · 命令行使用

```bash
# 基础用法
python scripts/generate.py \
  --prompt "A futuristic blue technology poster" \
  --output-dir "./outputs/images" \
  --model "qwen-image-2.0" \
  --size "1024x1024" \
  --n 1
```

**Windows PowerShell 一行版本**

```powershell
python .\scripts\generate.py --prompt "赛博朋克城市夜景" --output-dir ".\outputs\images" --model "qwen-image-2.0"
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
|---|---:|---|---|
| `--prompt` | 是 | — | 图片描述 prompt |
| `--output-dir` | 是 | — | 图片保存目录 |
| `--model` | 否 | `qwen-image-2.0` | 生图模型 |
| `--size` | 否 | `1024x1024` | 图片尺寸 |
| `--n` | 否 | `1` | qwen/gpt 路由的生成数量；Gemini 当前仅支持 1 |
| `--aspect-ratio` | 否 | `1:1` | Gemini 专用比例参数，支持 `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |

---

## Security · 安全

- API Key 不放源码，不放 Git 提交，不放 README
- Key 只从 `AIHUBMIX_API_KEY` 环境变量读取
- 图片默认保存到当前工程目录，不写系统目录
- 生成文件会加时间戳，不会覆盖已有文件
- 公开仓库不含任何真实 Key 或个人路径

---

## Troubleshooting · 排障

| 错误 | 原因 | 解决 |
|---|---|---|
| `Missing AIHUBMIX_API_KEY` | 环境变量未设置 | 按上面的「配置」步骤设置，重启终端 |
| `401 / 403` | Key 无效或过期 | 检查 Aihubmix 后台 Key 是否正确 |
| `Unsupported model: xxx` | 模型名写错 | 用 `qwen-image-2.0` / `gpt-image-2` / `gemini-3-pro-image` |
| `Unknown name "prompt"` | Gemini 误走 `/images/generations` | 使用本 skill 新版本：Gemini 会自动走 `/chat/completions` 多模态路由 |
| PowerShell 换行报错 | 用了 `^` 而不是反引号 | 用一行命令，或用反引号 `` ` `` 换行 |

---

## Project Structure · 项目结构

```
aihubmix-image-gen-oss/
├── SKILL.md            # Agent 使用指引
├── README.md           # 用户文档（本文件）
├── LICENSE             # MIT 许可证
├── .gitignore
└── scripts/
    └── generate.py     # 核心生成脚本（零依赖）
```

---

## Compatible Platforms · 兼容

| 平台 | 状态 |
|---|---|
| WorkBuddy | ✅ 原生支持 |
| Claude Code | ✅ 兼容 |
| Codex | ✅ 兼容 |
| OpenCode | ✅ 兼容 |
| 其他支持 Agent Skills 标准的平台 | ✅ 理论兼容 |

---

## License · 许可证

MIT — 随意使用、修改、分发。详见 [LICENSE](LICENSE)。

---

## Star History · 关注项目

如果这个 skill 对你有用，给个 ⭐ Star 就是对开源最大的支持。

有问题或建议，欢迎提 [Issue](https://github.com/jany22259-arch/aihubmix-image-gen-oss/issues)。
