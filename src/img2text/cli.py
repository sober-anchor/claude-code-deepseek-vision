# -*- coding: utf-8 -*-
"""img2text.cli —— 命令行入口。"""
import argparse
import sys

from .core import download_models, run


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog="img2text",
        description="把图片翻译成文字，喂给纯文本大模型（给 DeepSeek/文本模型装上眼睛）",
        epilog="示例: img2text photo.jpg auto | img2text photo.jpg vision | img2text photo.jpg ocr",
    )
    parser.add_argument("image", help="图片路径")
    parser.add_argument(
        "mode", nargs="?", default="auto", choices=["auto", "ocr", "vision"],
        help="auto=先OCR再视觉(默认); ocr=只读文字; vision=只描述画面",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=60,
        help="视觉描述的最大 token 数（默认 60）",
    )
    args = parser.parse_args(argv)
    try:
        run(args.image, args.mode, max_new_tokens=args.max_tokens)
    except KeyboardInterrupt:
        sys.exit(130)


def download_main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog="img2text-download",
        description="下载本地视觉模型（BLIP-large ~3.9GB，或 --base ~990MB）",
    )
    parser.add_argument(
        "--base", action="store_true",
        help="下载 base 版（~990MB）而非 large（~3.9GB）",
    )
    args = parser.parse_args(argv)
    download_models(base=args.base)


if __name__ == "__main__":
    main()
