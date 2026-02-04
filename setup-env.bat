@echo off
REM SSH/Git 環境自動設定工具 - Windows 快速啟動器
REM 此腳本會自動偵測 Python 並執行設定程式

echo ====================================================
echo     SSH/Git 環境自動設定工具
echo ====================================================
echo.

REM 檢查 Python 是否存在
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python
    echo.
    echo 請先安裝 Python 3.6 或更高版本:
    echo   下載: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 執行主程式
python setup-env.py

REM 暫停以便查看結果
pause
