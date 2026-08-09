# -*- coding: utf-8 -*-
"""img2text 最小测试集（不依赖已下载的模型，离线可跑）。"""
import pytest

import img2text


def test_version():
    assert isinstance(img2text.__version__, str)
    assert img2text.__version__


def test_missing_image_does_not_crash():
    """不存在的图片不应抛异常，应返回空字符串。"""
    assert img2text.run("nonexistent_xyz.jpg", "ocr", verbose=False) == ""
    assert img2text.run("nonexistent_xyz.jpg", "vision", verbose=False) == ""


def test_run_mode_default():
    """默认 mode 为 auto。"""
    assert img2text.run("nonexistent_xyz.jpg", verbose=False) == ""


@pytest.mark.parametrize("mode", ["auto", "ocr", "vision"])
def test_unknown_mode_defaults(mode):
    """已知 mode 都能安全返回。"""
    assert img2text.run("nonexistent_xyz.jpg", mode, verbose=False) == ""
