#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""下载本地视觉模型（BLIP-large，约 3.9GB；失败则回退下载 base，约 990MB）。

用法:
    python download_models.py            # 下载 large
    python download_models.py --base     # 强制下载 base
"""
import sys

def log(msg):
    print(msg, flush=True)

def download(model_id: str):
    from transformers import BlipProcessor, BlipForConditionalGeneration
    log(f">>> 下载 {model_id} ...")
    BlipProcessor.from_pretrained(model_id)
    BlipForConditionalGeneration.from_pretrained(model_id)
    log(">>> 完成")

if __name__ == "__main__":
    if "--base" in sys.argv:
        download("Salesforce/blip-image-captioning-base")
    else:
        try:
            download("Salesforce/blip-image-captioning-large")
        except Exception as e:
            log("large 下载失败: " + repr(e))
            log("回退下载 base ...")
            download("Salesforce/blip-image-captioning-base")
