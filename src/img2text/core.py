# -*- coding: utf-8 -*-
"""img2text.core —— 图片 → 文字翻译的核心逻辑。

给纯文本大模型（如 DeepSeek）提供"视觉"：先用 OCR 读文字 / 本地视觉模型描述画面，
再把翻译结果作为文字喂给底层模型。图片全程在本机处理，零额外 API 费用。
"""
from __future__ import annotations

# 视觉模型：优先大模型（更准），失败回退 base。
BLIP_MODELS = (
    "Salesforce/blip-image-captioning-large",
    "Salesforce/blip-image-captioning-base",
)

_easyocr_reader = None
_blip_cache: dict = {}


def easyocr_ocr(image_path: str, langs=("ch_sim", "en")) -> str:
    """用本地 easyocr 提取图片中的文字。失败返回 ''。"""
    global _easyocr_reader
    try:
        import easyocr
        if _easyocr_reader is None:
            # 首次调用会下载 ~100MB 模型到 ~/.EasyOCR
            _easyocr_reader = easyocr.Reader(langs, gpu=False)
        result = _easyocr_reader.readtext(image_path, detail=0, paragraph=True)
        return "\n".join(str(x) for x in result).strip()
    except Exception:
        return ""


def _load_blip():
    """懒加载 BLIP 模型；large 优先，回退 base。返回 {model_id: (processor, model)}。"""
    global _blip_cache
    if _blip_cache:
        return _blip_cache
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
    except ImportError:
        return None
    for model_id in BLIP_MODELS:
        try:
            # local_files_only: 只用本地缓存，避免因网络被墙（HF 连不上）而加载失败
            proc = BlipProcessor.from_pretrained(model_id, local_files_only=True)
            model = BlipForConditionalGeneration.from_pretrained(model_id, local_files_only=True)
            _blip_cache[model_id] = (proc, model)
            return _blip_cache
        except Exception:
            continue
    return None


def blip_caption(image_path: str, max_new_tokens: int = 60) -> str:
    """用本地视觉模型描述画面内容。模型未就绪或失败返回 ''。"""
    cache = _load_blip()
    if not cache:
        return ""
    try:
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
    except Exception:
        return ""


def run(image_path: str, mode: str = "auto", max_new_tokens: int = 60,
        verbose: bool = True) -> str:
    """把图片翻译成文字。

    参数:
        image_path: 图片路径
        mode: auto(先OCR再视觉) | ocr(只读文字) | vision(只描述画面)
        max_new_tokens: 视觉描述最大 token 数
        verbose: 是否打印过程

    返回:
        拼接的翻译文字；无内容时返回 ''。
    """
    parts = []
    if verbose:
        print(f"=== 图片 -> 文字翻译: {image_path} ===")

    if mode in ("auto", "ocr"):
        ocr_text = easyocr_ocr(image_path)
        if ocr_text:
            if verbose:
                print(f"[OCR] 识别到文字: {ocr_text!r}")
            parts.append(f"[图片中的文字] {ocr_text}")

    if mode in ("auto", "vision"):
        cap = blip_caption(image_path, max_new_tokens=max_new_tokens)
        if cap:
            if verbose:
                print(f"[视觉模型] 描述: {cap!r}")
            parts.append(f"[图片内容描述] {cap}")

    if not parts:
        if verbose:
            print("[!] 没有提取到任何内容（OCR 无文字 + 视觉模型未就绪）")
        return ""

    combined = "\n".join(parts)
    if verbose:
        print("--- 汇总（将喂给底层大脑）---")
        print(combined)
    return combined


def download_models(base: bool = False) -> None:
    """下载本地视觉模型。base=True 下载 ~990MB 的 base，否则 ~3.9GB 的 large。"""
    from transformers import BlipProcessor, BlipForConditionalGeneration
    model_id = "Salesforce/blip-image-captioning-base" if base \
        else "Salesforce/blip-image-captioning-large"
    print(f">>> 下载 {model_id} ...")
    BlipProcessor.from_pretrained(model_id)
    BlipForConditionalGeneration.from_pretrained(model_id)
    print(">>> 完成")
