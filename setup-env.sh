#!/bin/bash
# SSH/Git 環境自動設定工具 - Linux/macOS 快速啟動器
# 此腳本會自動偵測 Python 並執行設定程式

echo "===================================================="
echo "    SSH/Git 環境自動設定工具"
echo "===================================================="
echo ""

# 檢查 Python 是否存在
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 找不到 Python3"
    echo ""
    echo "請先安裝 Python 3.6 或更高版本:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  CentOS/RHEL:   sudo yum install python3"
    echo "  macOS:         brew install python3"
    echo ""
    exit 1
fi

# 執行主程式
python3 setup-env.py

echo ""
echo "按任意鍵繼續..."
read -n 1 -s
