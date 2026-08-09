---
name: image-understanding
description: 给纯文本底层大模型（如 DeepSeek）"看"图的能力。当需要查看/理解/描述图片内容、读取图片中的文字(OCR)、根据图片回答问题、或验证下载图片的真实内容时使用。触发词：看图、描述图片、识别图片内容、图片里写了什么、OCR、验证图片、把图片变成文字；英文亦触发：describe image / OCR / what's in this image / view image / check image content。
---

# Image Understanding（看图）

给纯文本底层模型提供"视觉"的翻译管道：**图片 → 文字（OCR / 视觉描述）→ 喂给大脑**。

## 安装要求

```bash
pip install -r requirements.txt
python download_models.py    # 下载 BLIP-large（~3.9GB），可选回退 base
```

## 核心工具

```
python <repo>/img2text.py <图片路径> [auto|ocr|vision]
```

- `auto`：先 OCR 再视觉描述（默认）
- `ocr`：只提取图片中的文字（easyocr，支持中英文）
- `vision`：只描述画面内容（BLIP-large 优先，失败回退 base）

工具输出就是"图片翻译成的文字"，把它作为事实依据用于推理、回答或写文档。

## 工作流程

1. **定位图片**（见下方"找图片"）
2. **运行工具**，拿到翻译文本
3. **基于翻译文本**回答用户或继续完成任务；必要时把文本喂给底层模型进一步分析

## 找图片

- 用户给了**完整路径** → 直接用。
- 只给了**文件名**（没路径）→ 按顺序：
  1. 若 `es.exe` 可用（Voidtools Everything 命令行客户端），用它秒级全盘查找：
     `es.exe -n 30 <文件名>`（Windows）
  2. 否则递归 Glob 常见目录：`Desktop`、`Pictures`、`Documents`、用户主目录
  3. 再找不到 → 直接问用户要路径或所在文件夹
- Everything HTTP 模式（若已开启）：`curl "http://127.0.0.1:8080/?search=<文件名>&json=1"`

## 注意事项

- BLIP 描述是**英文且偏简短**，细节可能不准，用于"大致内容"判断可靠，别当精确事实。
- OCR 只认文字，不认复杂版式/图表结构。
- 性能：BLIP-large 首次加载较慢（~3.9GB），CPU 每张约 9–16 秒；easyocr 首次运行会下载 ~100MB 模型。
- 纯离线运行：图片不离开本机，无需额外 API 费用。
