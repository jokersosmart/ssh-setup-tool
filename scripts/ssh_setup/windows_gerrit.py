"""Windows + Gerrit SSH 設定"""

import os
import subprocess
from pathlib import Path
from .base import SSHSetupBase


class WindowsGerritSetup(SSHSetupBase):
    """Windows 平台 + Gerrit 設定
    
    針對 Windows 作業系統和 Gerrit Code Review 的 SSH 設定
    """
    
    GERRIT_HOST = "rd2gerrit01.siliconmotion.com.tw"
    GERRIT_PORT = "29418"
    GERRIT_URL = f"https://{GERRIT_HOST}"
    
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
        """建立 Gerrit SSH config 內容"""
        return f"""Host {self.GERRIT_HOST}
  HostKeyAlgorithms +ssh-rsa
  PubkeyAcceptedAlgorithms +ssh-rsa
  User {self.username}
  Port {self.GERRIT_PORT}
"""
    
    def get_target_name(self) -> str:
        """取得設定目標名稱"""
        return "Gerrit (公司內部 Code Review)"
    
    def show_next_steps(self) -> None:
        """顯示下一步指引"""
        print("\n📋 下一步: 將公鑰加到 Gerrit")
        print("-" * 50)
        print("請複製上面的公鑰，然後:")
        print(f"  1. 登入 {self.GERRIT_URL}")
        print("  2. 點擊右上角使用者圖示 -> Settings")
        print("  3. 左側選單選擇 'SSH Public Keys'")
        print("  4. 點擊 'Add Key' 按鈕")
        print("  5. 貼上公鑰並儲存")
    
    def get_verification_command(self) -> str:
        """取得驗證命令"""
        return f"ssh -p {self.GERRIT_PORT} {self.username}@{self.GERRIT_HOST}"
