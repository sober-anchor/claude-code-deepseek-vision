@echo off
REM ============================================
REM  claude-code-deepseek-vision 一键安装 (Windows)
REM  1) 安装 Python 依赖
REM  2) 下载本地视觉模型 (BLIP-large, ~3.9GB)
REM ============================================
chcp 65001 >nul
echo.
echo  [1/2] 安装 Python 依赖...
python -m pip install -r requirements.txt || goto :err

echo.
echo  [2/2] 下载视觉模型 (BLIP-large, 约 3.9GB, 耐心等待)...
python download_models.py || goto :err

echo.
echo  安装完成! 使用方法:
echo    python img2text.py <图片路径> [auto^|ocr^|vision]
echo.
echo  装成 Claude Code skill:
echo    xcopy /s /y SKILL.md "%USERPROFILE%\.claude\skills\image-understanding\SKILL.md"
echo.
pause
exit /b 0

:err
echo.
echo  安装失败, 请检查 Python 和网络后重试。
pause
exit /b 1
