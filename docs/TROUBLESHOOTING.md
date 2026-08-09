# 🔧 疑难排解 / Troubleshooting

> 遇到问题先看这里。都是本项目开发过程中真实踩过的坑。

## 目录

1. [模型收到 `[Unsupported Image]`](#1-模型收到-unsupported-image)
2. [把模型名改成 claude-* 还是不能看图](#2-把模型名改成-claude-还是不能看图)
3. [连接 github.com 超时 / 无法推送](#3-连接-githubcom-超时--无法推送)
4. [WinRT OCR（winrt_ocr.ps1）报 COM 转换错误](#4-winrt-ocrwinrt_ocrps1报-com-转换错误)
5. [模型下载失败 / 很慢](#5-模型下载失败--很慢)
6. [EasyOCR 首次运行很慢](#6-easyocr-首次运行很慢)
7. [只给文件名找不到图片](#7-只给文件名找不到图片)
8. [中文乱码 / 控制台编码问题](#8-中文乱码--控制台编码问题)

---

## 1. 模型收到 `[Unsupported Image]`

**现象**：给 DeepSeek 发图片，模型却"看到"文字 `[Unsupported Image]`。

**原因**：DeepSeek 公开 API 是纯文本模型。官方 Anthropic 兼容端点在收到 `image` 内容块时，
直接把图片替换成占位文字 `[Unsupported Image]` 再交给模型，模型永远拿不到真实像素。

**解决**：使用本项目，用本地 OCR / 视觉模型先把图片翻译成文字，再喂给模型。

**验证**：
```bash
python img2text.py your_photo.jpg vision
```

## 2. 把模型名改成 claude-* 还是不能看图

**现象**：在 Claude Code 里把模型名改成 `claude-opus-5` 等支持视觉的模型名，图片仍然不能看。

**原因**：改名字能骗过 Claude Code 外壳的"视觉能力清单"，但**骗不过 DeepSeek 的接口层**。
实测：伪装成 `claude-opus-5` 发送图片，后台还是跑 deepseek-v4-pro，图片仍被替换成 `[Unsupported Image]`。
**病根在 API 层，不在能力清单。**

**结论**：不要再折腾改模型名了，走"翻译官"管道。

## 3. 连接 github.com 超时 / 无法推送

**现象**：`gh auth login`、`git push` 卡住或报 `dial tcp ...: i/o timeout`。

**原因**：国内部分网络环境会墙掉 `github.com` 主域（但 `api.github.com`、`codeload.github.com` 往往能通）。

**排查**：
```bash
curl -m 8 -o /dev/null -w "%{http_code}\n" https://github.com   # 000 = 不通
curl -m 8 -o /dev/null -w "%{http_code}\n" https://api.github.com  # 200 = 通
```

**解决**：使用系统代理（如 Clash 等）：
```bash
export HTTPS_PROXY=http://127.0.0.1:<你的代理端口>
git config http.proxy http://127.0.0.1:<你的代理端口>
```

## 4. WinRT OCR（winrt_ocr.ps1）报 COM 转换错误

**现象**：运行 `winrt_ocr.ps1` 报
`无法将类型"System.__ComObject"的对象转换为类型"Windows.Foundation.IAsyncOperation..."`。

**原因**：Windows PowerShell 5.1 调用 WinRT 异步接口时的经典互操作问题，与脚本本身无关。

**解决**：本项目的默认 OCR 是 **easyocr**（`python img2text.py ... ocr`），不要依赖 WinRT。
`winrt_ocr.ps1` 仅作为实验性参考保留。

## 5. 模型下载失败 / 很慢

**现象**：`download_models.py` 卡住或超时。

**原因**：BLIP 模型（~3.9GB）托管在 HuggingFace Hub，网络波动会失败。

**解决**：
- 重试：`python download_models.py`
- 换小模型：`python download_models.py --base`（~990MB）
- 配代理后重试。

## 6. EasyOCR 首次运行很慢

**现象**：第一次调用 OCR 卡很久。

**原因**：easyocr 首次运行需下载 ~100MB 识别模型到 `~/.EasyOCR`，且 torch CPU 初始化较慢。

**解决**：耐心等首次完成，之后会缓存到本地，速度正常。

## 7. 只给文件名找不到图片

**现象**：用户只给了文件名、没给路径，找不到图。

**解决**：
- 先确认机器上有没有 **Voidtools Everything** 的命令行客户端 `es.exe`（本项目文档建议安装）。
- 有：`es.exe -n 30 <文件名>` 秒级全盘查找。
- 没有：递归查找常见目录（Desktop / Pictures / Documents / 主目录），再不行就问用户要路径。

## 8. 中文乱码 / 控制台编码问题

**现象**：终端输出中文变 `�`。

**解决**：Windows 下先执行 `chcp 65001` 切 UTF-8；或在 Python 里 `sys.stdout.reconfigure(encoding="utf-8")`（本项目已内置）。

---

> 没找到你遇到的问题？欢迎提 [Issue](../../issues) 或参与 [CONTRIBUTING](CONTRIBUTING.md)。
