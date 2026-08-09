@echo off
REM ============================================
REM  claude-code-deepseek-vision-solution 一键安装 (Windows)
REM  1) 安装为正式 Python 包（自动拉取依赖）
REM  2) 下载本地视觉模型 (BLIP-large, ~3.9GB)
REM ============================================
chcp 65001 >nul
echo.
echo  [1/2] 安装为 Python 包 (img2text)...
python -m pip install -e . || goto :err

echo.
echo  [2/2] 下载视觉模型 (BLIP-large, 约 3.9GB, 耐心等待)...
img2text-download || goto :err

echo.
echo  安装完成! 使用方法:
echo    img2text <图片路径> [auto^|ocr^|vision]
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
