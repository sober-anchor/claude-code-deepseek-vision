# -*- coding: utf-8 -*-
"""img2text —— 给纯文本大模型装上眼睛。

本地 OCR + 视觉模型把图片翻译成文字，再喂给底层大模型（如 DeepSeek），
让它也能"看懂"图片。图片全程在本机处理，零额外 API 费用。
"""
from .core import blip_caption, download_models, easyocr_ocr, run

__version__ = "1.1.0"
__all__ = ["easyocr_ocr", "blip_caption", "run", "download_models", "__version__"]
