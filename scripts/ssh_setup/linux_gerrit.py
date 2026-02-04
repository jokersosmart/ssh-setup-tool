"""Linux/macOS + Gerrit SSH 設定"""

import os
import subprocess
from pathlib import Path
from .base import SSHSetupBase


class LinuxGerritSetup(SSHSetupBase):
    """Linux/macOS 平台 + Gerrit 設定
    
    針對 Linux 和 macOS 作業系統和 Gerrit Code Review 的 SSH 設定
    """
    
    GERRIT_HOST = "rd2gerrit01.siliconmotion.com.tw"
    GERRIT_PORT = "29418"
    GERRIT_URL = f"https://{GERRIT_HOST}"
    
    def get_home_path(self) -> str:
        """取得 Linux/macOS HOME 路徑"""
        # 使用環境變數或預設路徑
        return os.environ.get("HOME", f"/home/{self.username}")
    
    def _set_home_env(self) -> None:
        """設定 Linux/macOS HOME 環境變數"""
        # 在 Linux/macOS 上，HOME 通常已經正確設定
        # 但我們可以寫入 shell 設定檔以確保
        home = str(self.home_dir)
        
        # 偵測使用的 shell
        shell = os.environ.get("SHELL", "/bin/bash")
        
        if "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            rc_file = Path.home() / ".bashrc"
        
        # 檢查是否已經設定
        if rc_file.exists():
            with open(rc_file, "r", encoding="utf-8") as f:
                content = f.read()
                if f'export HOME="{home}"' in content or f"export HOME='{home}'" in content:
                    print(f"✅ HOME 環境變數已在 {rc_file} 中設定")
                    return
        
        # 加入 HOME 設定
        try:
            with open(rc_file, "a", encoding="utf-8") as f:
                f.write(f'\n# SSH Setup Tool - HOME environment variable\n')
                f.write(f'export HOME="{home}"\n')
            print(f"✅ 已將 HOME 環境變數加入 {rc_file}")
            print(f"⚠️  請執行: source {rc_file}")
        except Exception as e:
            print(f"⚠️  寫入 {rc_file} 失敗: {e}")
            print(f"HOME 目前已設定為: {home}")
    
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
