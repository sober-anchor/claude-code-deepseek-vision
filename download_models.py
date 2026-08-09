#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""下载本地视觉模型（无需安装包即可使用）。

用法:
    python download_models.py            # 下载 large (~3.9GB)
    python download_models.py --base     # 下载 base  (~990MB)

安装为包后也可用命令 `img2text-download [--base]`。
"""
import sys


def download(model_id: str) -> None:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    print(f">>> 下载 {model_id} ...")
    BlipProcessor.from_pretrained(model_id)
    BlipForConditionalGeneration.from_pretrained(model_id)
    print(">>> 完成")


if __name__ == "__main__":
    if "--base" in sys.argv:
        download("Salesforce/blip-image-captioning-base")
    else:
        try:
            download("Salesforce/blip-image-captioning-large")
        except Exception as e:
            print("large 下载失败: " + repr(e))
            print("回退下载 base ...")
            download("Salesforce/blip-image-captioning-base")
