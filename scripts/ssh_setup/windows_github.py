"""Windows + GitHub SSH 設定"""

import os
import subprocess
from pathlib import Path
from .base import SSHSetupBase


class WindowsGitHubSetup(SSHSetupBase):
    """Windows 平台 + GitHub 設定
    
    針對 Windows 作業系統和 GitHub 的 SSH 設定
    """
    
    GITHUB_HOST = "github.com"
    GITHUB_SSH_HOST = "github.com"
    GITHUB_SETTINGS_URL = "https://github.com/settings/keys"
    
    def get_home_path(self) -> str:
        """取得 Windows HOME 路徑"""
        return f"C:\\Users\\{self.username}"
    
    def _set_home_env(self) -> None:
        """設定 Windows HOME 環境變數"""
        try:
            # 使用 setx 設定使用者環境變數
            subprocess.run(
                ["setx", "HOME", str(self.home_dir)],
                check=True,
                capture_output=True
            )
            print(f"✅ 已使用 setx 設定 HOME 環境變數")
            print("⚠️  注意: 需要重新開啟終端機才會生效")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  設定環境變數失敗: {e}")
            print(f"請手動設定 HOME 環境變數為: {self.home_dir}")
    
    def create_ssh_config_content(self) -> str:
        """建立 GitHub SSH config 內容"""
        return f"""Host {self.GITHUB_HOST}
  HostName {self.GITHUB_SSH_HOST}
  User git
  IdentityFile ~/.ssh/id_rsa
"""
    
    def get_target_name(self) -> str:
        """取得設定目標名稱"""
        return "GitHub (公開 Git 平台)"
    
    def show_next_steps(self) -> None:
        """顯示下一步指引"""
        print("\n📋 下一步: 將公鑰加到 GitHub")
        print("-" * 50)
        print("請複製上面的公鑰，然後:")
        print(f"  1. 登入 {self.GITHUB_SETTINGS_URL}")
        print("  2. 點擊 'New SSH key' 按鈕")
        print("  3. Title: 輸入一個描述 (例如: 'My Windows PC')")
        print("  4. Key: 貼上公鑰")
        print("  5. 點擊 'Add SSH key' 按鈕")
    
    def get_verification_command(self) -> str:
        """取得驗證命令"""
        return f"ssh -T git@{self.GITHUB_HOST}"
