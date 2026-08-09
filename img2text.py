#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""img2text.py — 给纯文本大模型装上"眼睛"。

把一张图片翻译成文字（OCR 提取文字 / 本地视觉模型描述画面），
再把这串文字喂给底层大模型（如 DeepSeek），它就能"看懂"图片。

用法:
    python img2text.py <图片路径> [auto|ocr|vision]
      auto   - 先 OCR 再视觉描述（默认）
      ocr    - 只提取图片中的文字（easyocr，中英）
      vision - 只描述画面内容（BLIP-large，失败回退 base）

依赖:
    pip install -r requirements.txt
    （首次运行 easyocr 会下载 ~100MB 模型；视觉模型需先跑 download_models.py）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))

_easyocr_reader = None

# 视觉模型：优先大模型（更准），回退 base。
BLIP_MODELS = ("Salesforce/blip-image-captioning-large",
               "Salesforce/blip-image-captioning-base")
_blip_cache = {}


def easyocr_ocr(image_path: str, langs=("ch_sim", "en")) -> str:
    """提取图片中的文字。返回 '' 表示未识别到或未安装。"""
    global _easyocr_reader
    try:
        import easyocr
    except ImportError:
        return ""
    if _easyocr_reader is None:
        _easyocr_reader = easyocr.Reader(langs, gpu=False)
    result = _easyocr_reader.readtext(image_path, detail=0, paragraph=True)
    return "\n".join(str(x) for x in result).strip()


def _load_blip():
    global _blip_cache
    if _blip_cache:
        return _blip_cache
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
    except ImportError:
        return None
    for model_id in BLIP_MODELS:
        try:
            proc = BlipProcessor.from_pretrained(model_id)
            model = BlipForConditionalGeneration.from_pretrained(model_id)
            _blip_cache[model_id] = (proc, model)
            return _blip_cache
        except Exception:
            continue
    return None


def blip_caption(image_path: str, max_new_tokens: int = 60) -> str:
    """用本地视觉模型描述画面。返回 '' 表示模型未就绪。"""
    cache = _load_blip()
    if not cache:
        return ""
    from PIL import Image
    raw = Image.open(image_path).convert("RGB")
    best, best_len = "", -1
    for model_id, (proc, model) in cache.items():
        inputs = proc(raw, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=max_new_tokens)
        cap = proc.decode(out[0], skip_special_tokens=True).strip()
        if len(cap) > best_len:  # 取更详细的描述
            best, best_len = cap, len(cap)
    return best


def run(image_path: str, mode: str = "auto") -> str:
    print(f"=== 图片 -> 文字翻译: {image_path} ===")
    parts = []

    if mode in ("auto", "ocr"):
        ocr_text = easyocr_ocr(image_path)
        if ocr_text:
            print(f"[OCR] 识别到文字: {ocr_text!r}")
            parts.append(f"[图片中的文字] {ocr_text}")

    if mode in ("auto", "vision"):
        cap = blip_caption(image_path)
        if cap:
            print(f"[视觉模型] 描述: {cap!r}")
            parts.append(f"[图片内容描述] {cap}")

    if not parts:
        print("[!] 没有提取到任何内容（OCR 无文字 + 视觉模型未就绪）")
        return ""

    combined = "\n".join(parts)
    print("--- 汇总（将喂给底层大脑）---")
    print(combined)
    return combined


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python img2text.py <图片路径> [auto|ocr|vision]")
        sys.exit(1)
    mode = sys.argv[2] if len(sys.argv) > 2 else "auto"
    run(sys.argv[1], mode)
