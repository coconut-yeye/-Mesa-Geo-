@echo off
chcp 65001 >nul
echo ========================================
echo 安装项目依赖包
echo ========================================
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 安装成功！
    echo ========================================
    echo.
    echo 现在可以运行测试脚本验证安装：
    echo   python test_installation.py
    echo.
    echo 或直接运行主程序：
    echo   python run.py
) else (
    echo.
    echo ========================================
    echo ❌ 安装失败
    echo ========================================
    echo.
    echo 如果安装 geopandas 失败，请尝试：
    echo   conda install geopandas
    echo.
    echo 或使用国内镜像：
    echo   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

pause

