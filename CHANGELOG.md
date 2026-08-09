# 📝 更新日志 / Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 与 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-08-09

### ✨ 新增

- 📦 **升级为正式 Python 包**：`pyproject.toml` + `src/` 布局，支持 `pip install -e .`
- 🖥️ **命令行入口**：`img2text <图片> [auto|ocr|vision]` 与 `img2text-download [--base]`
- 🧪 **最小测试集**：`tests/`，离线可跑
- 🔧 核心逻辑拆分为 `src/img2text/{core,cli}.py`，支持 `python -m img2text`

### 📝 变更

- `install.bat` / `install.sh` 改为 `pip install -e .` + `img2text-download`
- README / SKILL.md 安装与用法同步更新

### 🔒 安全

- 全程无敏感信息（无密钥/邮箱/密码）

## [1.0.0] - 2026-08-09

### ✨ 新增

- 🖼️ 核心工具 `img2text.py`：图片 → 文字翻译管道
  - `ocr` 模式：本地 easyocr 提取中英文文字
  - `vision` 模式：本地 BLIP 视觉模型描述画面（优先 BLIP-large，回退 base）
  - `auto` 模式：先 OCR 再视觉描述
- 🧩 Claude Code skill：`SKILL.md`，一键装进 `~/.claude/skills/`
- 🚀 一键安装脚本：`install.bat`（Windows）/ `install.sh`（macOS/Linux）
- 🎛️ 模型下载脚本：`download_models.py`（large / base 可选）
- 📄 完整文档：README、幕后故事 STORY.md、疑难排解、贡献指南、安全政策

### 🐛 已知事项

- `winrt_ocr.ps1`（Windows 内置 OCR）在部分 PowerShell 5.1 环境有 WinRT COM 互操作问题，标记为实验性。
- BLIP-large 首次加载 ~3.9GB、CPU 每张图约 9–16 秒，属预期性能。

### 🔒 安全

- 仓库提交历史使用 GitHub noreply 邮箱，不含个人邮箱。
- 仓库不含任何 API Key / 密码 / token。
