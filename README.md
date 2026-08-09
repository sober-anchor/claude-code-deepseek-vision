<div align="center">

# 👁️ claudecode 接 DeepSeek API 无法识图？一键解决方案

**给 Claude Code × DeepSeek 装上眼睛 —— 本地 OCR + 视觉模型翻译管道，零额外 API 费用**
**Give your text-only DeepSeek backend real vision inside Claude Code — locally, privately, free.**

[![GitHub stars](https://img.shields.io/github/stars/sober-anchor/claude-code-deepseek-vision-solution?style=social)](https://github.com/sober-anchor/claude-code-deepseek-vision-solution)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](img2text.py)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](install.sh)
[![Offline](https://img.shields.io/badge/runtime-offline-orange.svg)](#-特性-features)

📖 [幕后故事](STORY.md) · 🔧 [疑难排解](docs/TROUBLESHOOTING.md) · 🤝 [参与贡献](docs/CONTRIBUTING.md) · 📝 [更新日志](CHANGELOG.md)

</div>

---

## 🎯 为什么需要这个项目？

DeepSeek 的公开 API 是**纯文本模型**。当你把它接进 **Claude Code** 后会发现：

- ❌ 官方 Anthropic 兼容端点会把图片替换成一行字 `[Unsupported Image]`
- ❌ 原生 API 直接拒绝图片（`unknown variant 'image_url', expected 'text'`）
- ❌ 网页版「识图模式」是**网页端专属功能**，**不向 API 开放**
- ❌ 把模型名改成 `claude-opus-5` 也没用 —— 病根在 DeepSeek 的接口层

**本项目**在中间加一层本地「翻译官」：**图片 → OCR / 视觉模型 → 文字 → 喂给 DeepSeek**，你的 DeepSeek 大脑就能「看懂」图片了。

## 🧠 原理 / How it works

```
┌─────────┐    ┌────────────────────────────┐    ┌────────────┐    ┌──────────┐
│  图片     │───▶│  img2text.py 本地翻译官       │───▶│  文字描述     │───▶│ DeepSeek │
│ cat.jpg  │    │  · easyocr    读文字         │    │ "a kitten  │    │  大脑     │
│          │    │  · BLIP-large 描述画面       │    │  sitting…" │    │  "看懂"  │
└─────────┘    └────────────────────────────┘    └────────────┘    └──────────┘
                完全离线 · 图片不离开本机 · 零额外 API 费用
```

## ✨ 特性 / Features

- 🖼️ **看图**：本地视觉模型（BLIP-large）描述画面内容
- 📄 **读字**：本地 OCR（easyocr）提取中英文文字
- 🔒 **纯离线**：图片不出本机，零额外 API 费用
- 🧩 **一键装成 skill**：让 Claude Code 自动知道怎么用
- ⚡ **全盘找图**（可选）：配合 Voidtools Everything 秒级定位任何图片
- 🚀 **一键安装**：Windows 双击 `install.bat`，macOS/Linux 运行 `./install.sh`

## 🚀 快速开始 / Quick start

```bash
# 1. 克隆仓库
git clone https://github.com/sober-anchor/claude-code-deepseek-vision-solution.git
cd claude-code-deepseek-vision-solution

# 2. 安装（Windows: 双击 install.bat；macOS/Linux: ./install.sh）
python -m pip install -r requirements.txt
python download_models.py        # 下载 BLIP-large (~3.9GB)

# 3. 试用：让 AI "看"一张图
python img2text.py your_photo.jpg
# → [视觉模型] 描述: 'there is a small kitten sitting on the floor looking at the camera'
```

## 🧩 装成 Claude Code skill

```bash
mkdir -p ~/.claude/skills/image-understanding
cp SKILL.md ~/.claude/skills/image-understanding/
```

重启 Claude Code 后技能自动可用。之后你只需说 **"看看这张图"**，Claude 就会自动调用翻译管道。

## 🎬 效果对比 / Demo（BLIP-base vs BLIP-large）

同一张猫照片：

| 模型 | 描述 |
|---|---|
| BLIP-base（旧） | `a kitten is standing on the floor looking up` |
| **BLIP-large**（本仓库默认） | `there is a small kitten sitting on the floor looking at the camera` |

OCR 效果（一张写着中文+英文的测试图）：

```
[图片中的文字] 猫品种图鉴 / OCR 测试 Hello World 12345 / Windows 内置识别
```

## 🔧 命令参考 / CLI

```
python img2text.py <图片路径> [auto|ocr|vision]
  auto   - 先 OCR 再视觉描述（默认）
  ocr    - 只提取文字
  vision - 只描述画面
```

## 📚 文档 / Docs

| 文档 | 说明 |
|---|---|
| [STORY.md](STORY.md) | 📖 《一个小白如何不动手发布一个高星 GitHub 项目》—— 本项目的诞生故事 |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | 🔧 常见问题：`[Unsupported Image]`、网络被墙、WinRT OCR、模型下载失败等 |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | 🤝 贡献指南：环境、代码规范、提 PR 流程 |
| [docs/SECURITY.md](docs/SECURITY.md) | 🔒 安全政策：如何报告漏洞、隐私提醒 |
| [CHANGELOG.md](CHANGELOG.md) | 📝 版本更新日志 |

## ❓ FAQ

**为什么不能直接改模型名让它支持图片？**
因为 DeepSeek 的 API 层根本不接受/不转发图片块（实测：发送图片后，模型收到的是文字 `[Unsupported Image]`）。这是接口层的限制，换名字解决不了。本仓库从外部补上视觉，绕开这个限制。详见 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)。

**一定要下载 3.9GB 的模型吗？**
`download_models.py` 默认下 BLIP-large（更准）。嫌大就 `python download_models.py --base`（~990MB），`img2text.py` 会自动回退。

**EasyOCR 会不会很慢？**
首次运行下载 ~100MB 模型；之后 OCR 很快，BLIP 每张图 CPU 约 9–16 秒。

**隐私？**
所有处理都在本机，图片不会上传到任何服务。你只决定是否把翻译后的文字发给你自己的模型。

## 📦 目录结构

```
├── img2text.py          # 核心工具：图片 → 文字
├── SKILL.md             # Claude Code skill 定义
├── STORY.md             # 项目幕后故事
├── download_models.py   # 下载视觉模型
├── install.sh           # macOS/Linux 一键安装
├── install.bat          # Windows 一键安装
├── winrt_ocr.ps1        # [实验性] Windows 内置 OCR
├── docs/                # 文档：排解 / 贡献 / 安全
├── requirements.txt
└── LICENSE
```

## 📄 License

[MIT](LICENSE)

## 🙏 致谢 / Credits

- [Voidtools Everything](https://www.voidtools.com/) —— 全盘秒级文件搜索
- [Salesforce BLIP](https://github.com/salesforce/BLIP) —— 本地图像描述模型
- [JaidedAI EasyOCR](https://github.com/JaidedAI/EasyOCR) —— 本地 OCR
- 以及一路帮忙点「Authorize」的那个小白 🙌
