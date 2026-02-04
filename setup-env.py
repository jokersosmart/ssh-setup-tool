#!/usr/bin/env python3
"""SSH/Git 環境自動設定工具 - 主程式

跨平台的 SSH 和 Git 環境自動設定工具，
支援 Windows、Linux、macOS 以及 Gerrit 和 GitHub。
"""

import platform
import sys
import os
import getpass


def check_python_version():
    """檢查 Python 版本"""
    if sys.version_info < (3, 6):
        print("❌ 錯誤: 需要 Python 3.6 或更高版本")
        print(f"目前版本: Python {sys.version}")
        sys.exit(1)


def get_username() -> str:
    """取得使用者名稱"""
    # 嘗試從環境變數取得
    username = os.environ.get("USER") or os.environ.get("USERNAME")
    
    if not username:
        username = getpass.getuser()
    
    # 讓使用者確認或修改
    print(f"👤 偵測到使用者名稱: {username}")
    response = input("確認使用者名稱 (直接按 Enter 確認，或輸入新名稱): ").strip()
    
    if response:
        username = response
    
    return username


def ask_target() -> str:
    """詢問設定目標"""
    print("\n請選擇設定目標:")
    print("  1. Gerrit (公司內部 Code Review)")
    print("  2. GitHub (公開 Git 平台)")
    print()
    
    while True:
        choice = input("請輸入 1 或 2: ").strip()
        if choice == "1":
            return "gerrit"
        elif choice == "2":
            return "github"
        else:
            print("❌ 無效的選擇，請輸入 1 或 2")


def ask_email(username: str, target: str) -> str:
    """詢問電子郵件地址"""
    # 根據目標提供預設建議
    if target == "gerrit":
        default_email = f"{username}@siliconmotion.com"
        print(f"\n📧 Gerrit 建議使用公司 email")
    else:
        default_email = f"{username}@example.com"
        print(f"\n📧 GitHub 請使用您的 GitHub 帳號 email")
    
    print(f"預設: {default_email}")
    response = input("請輸入 email (直接按 Enter 使用預設): ").strip()
    
    if response:
        return response
    else:
        return default_email


def main():
    """主程式"""
    try:
        # 檢查 Python 版本
        check_python_version()
        
        # 偵測作業系統
        os_type = platform.system()
        
        # 取得使用者資訊
        username = get_username()
        
        # 選擇目標
        target = ask_target()
        
        # 取得 email
        email = ask_email(username, target)
        
        print("\n" + "=" * 50)
        
        # 根據作業系統和目標選擇對應的設定類別
        if os_type == "Windows":
            if target == "gerrit":
                from scripts.ssh_setup.windows_gerrit import WindowsGerritSetup
                setup = WindowsGerritSetup(username, email)
            else:
                from scripts.ssh_setup.windows_github import WindowsGitHubSetup
                setup = WindowsGitHubSetup(username, email)
        else:  # Linux or Darwin (macOS)
            if target == "gerrit":
                from scripts.ssh_setup.linux_gerrit import LinuxGerritSetup
                setup = LinuxGerritSetup(username, email)
            else:
                from scripts.ssh_setup.linux_github import LinuxGitHubSetup
                setup = LinuxGitHubSetup(username, email)
        
        # 執行設定
        setup.setup()
        
        print("\n" + "=" * 50)
        print("🎉 所有設定完成！")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  程式已中斷")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
