#!/usr/bin/env bash
# ============================================
#  claude-code-deepseek-vision-solution 一键安装 (macOS / Linux)
#  1) 安装 Python 依赖
#  2) 下载本地视觉模型 (BLIP-large, ~3.9GB)
# ============================================
set -e
cd "$(dirname "$0")"

echo ""
echo " [1/2] 安装 Python 依赖..."
python3 -m pip install -r requirements.txt

echo ""
echo " [2/2] 下载视觉模型 (BLIP-large, 约 3.9GB, 耐心等待)..."
python3 download_models.py

echo ""
echo " 安装完成! 使用方法:"
echo "   python3 img2text.py <图片路径> [auto|ocr|vision]"
echo ""
echo " 装成 Claude Code skill:"
echo "   mkdir -p ~/.claude/skills/image-understanding && cp SKILL.md ~/.claude/skills/image-understanding/"
