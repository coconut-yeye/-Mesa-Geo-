@echo off
chcp 65001 >nul
echo ========================================
echo 运行商业人流模拟
echo ========================================
echo.

python run.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ❌ 运行出错
    echo ========================================
    echo.
    echo 请先运行测试脚本检查环境：
    echo   python test_installation.py
    echo.
    echo 或查看 QUICKSTART.md 获取帮助
)

pause

