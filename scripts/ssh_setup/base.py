"""SSH Setup Base Class - 共用基礎類別和工具函數"""

import os
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class SSHSetupBase(ABC):
    """SSH 設定基礎類別
    
    提供 SSH 和 Git 環境設定的共用功能，
    子類別需實作平台和目標特定的方法。
    """
    
    # 命令超時設定（秒）
    COMMAND_TIMEOUT = 5
    
    def __init__(self, username: str, email: str):
        """初始化 SSH 設定
        
        Args:
            username: 使用者名稱
            email: 電子郵件地址
        """
        self.username = username
        self.email = email
        # 這些路徑會在 setup() 執行時被初始化
        self.home_dir: Optional[Path] = None
        self.ssh_dir: Optional[Path] = None
        self.ssh_key_path: Optional[Path] = None
        self.ssh_pub_key_path: Optional[Path] = None
        
    def setup(self) -> None:
        """主要設定流程"""
        try:
            self.print_header()
            self.confirm_settings()
            
            print("\n開始設定流程...")
            print("=" * 50)
            
            # 執行 5 個步驟
            self.set_home()
            self.create_ssh_dir()
            self.generate_ssh_key()
            self.create_ssh_config()
            self.set_git_config()
            
            # 顯示結果
            self.show_results()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  設定已取消")
            sys.exit(0)
        except Exception as e:
            print(f"\n\n❌ 錯誤: {e}")
            sys.exit(1)
    
    def print_header(self) -> None:
        """顯示標題"""
        print("=" * 50)
        print("    SSH/Git 環境自動設定工具")
        print("=" * 50)
        print()
    
    def confirm_settings(self) -> None:
        """確認設定資訊"""
        import platform
        print(f"🖥️  作業系統: {platform.system()}")
        print(f"👤 使用者名稱: {self.username}")
        print(f"📧 電子郵件: {self.email}")
        print(f"🎯 設定目標: {self.get_target_name()}")
        print()
        
        response = input("確認以上資訊無誤? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("設定已取消")
            sys.exit(0)
    
    def set_home(self) -> None:
        """[1/5] 設定 HOME 環境變數"""
        print("\n[1/5] 設定 HOME 環境變數")
        print("-" * 50)
        
        self.home_dir = Path(self.get_home_path())
        print(f"HOME 路徑: {self.home_dir}")
        
        # 平台特定的設定
        self._set_home_env()
        
        print("✅ HOME 環境變數設定完成")
    
    def create_ssh_dir(self) -> None:
        """[2/5] 建立 .ssh 資料夾"""
        print("\n[2/5] 建立 .ssh 資料夾")
        print("-" * 50)
        
        self.ssh_dir = self.home_dir / ".ssh"
        
        if self.ssh_dir.exists():
            print(f"📁 資料夾已存在: {self.ssh_dir}")
        else:
            self.ssh_dir.mkdir(mode=0o700, parents=True)
            print(f"✅ 已建立資料夾: {self.ssh_dir}")
        
        # 設定權限 (Unix 系統)
        if os.name != 'nt':
            os.chmod(self.ssh_dir, 0o700)
            print("✅ 已設定權限: 700")
    
    def generate_ssh_key(self) -> None:
        """[3/5] 生成 SSH 金鑰"""
        print("\n[3/5] 生成 SSH 金鑰")
        print("-" * 50)
        
        self.ssh_key_path = self.ssh_dir / "id_rsa"
        self.ssh_pub_key_path = self.ssh_dir / "id_rsa.pub"
        
        # 檢查是否已存在
        if self.ssh_key_path.exists():
            print(f"⚠️  SSH 金鑰已存在: {self.ssh_key_path}")
            response = input("是否覆蓋現有金鑰? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("⏭️  跳過金鑰生成")
                return
            print("⚠️  將覆蓋現有金鑰...")
        
        # 檢查 ssh-keygen 命令
        if not self._check_command("ssh-keygen"):
            self._show_ssh_keygen_install_guide()
            sys.exit(1)
        
        # 生成金鑰
        try:
            cmd = [
                "ssh-keygen",
                "-t", "rsa",
                "-b", "4096",
                "-C", self.email,
                "-f", str(self.ssh_key_path),
                "-N", ""  # 空密碼
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ SSH 金鑰已生成: {self.ssh_key_path}")
            
            # 設定權限 (Unix 系統)
            if os.name != 'nt':
                os.chmod(self.ssh_key_path, 0o600)
                os.chmod(self.ssh_pub_key_path, 0o644)
                print("✅ 已設定金鑰權限")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 生成金鑰失敗: {e}")
            sys.exit(1)
    
    def create_ssh_config(self) -> None:
        """[4/5] 建立 SSH config 檔案"""
        print("\n[4/5] 建立 SSH config 檔案")
        print("-" * 50)
        
        config_path = self.ssh_dir / "config"
        config_content = self.create_ssh_config_content()
        
        # 如果檔案已存在，詢問是否覆蓋或附加
        if config_path.exists():
            print(f"⚠️  Config 檔案已存在: {config_path}")
            print("1. 覆蓋現有 config")
            print("2. 附加到現有 config")
            print("3. 跳過")
            choice = input("請選擇 (1/2/3): ").strip()
            
            if choice == "1":
                mode = "w"
            elif choice == "2":
                mode = "a"
                config_content = "\n\n" + config_content
            else:
                print("⏭️  跳過 config 設定")
                return
        else:
            mode = "w"
        
        # 寫入 config
        with open(config_path, mode, encoding="utf-8") as f:
            f.write(config_content)
        
        # 設定權限 (Unix 系統)
        if os.name != 'nt':
            os.chmod(config_path, 0o600)
        
        print(f"✅ SSH config 已建立: {config_path}")
        print("\nConfig 內容:")
        print("-" * 30)
        print(config_content.strip())
        print("-" * 30)
    
    def set_git_config(self) -> None:
        """[5/5] 設定 Git 全域配置"""
        print("\n[5/5] 設定 Git 全域配置")
        print("-" * 50)
        
        # 檢查 git 命令
        if not self._check_command("git"):
            self._show_git_install_guide()
            sys.exit(1)
        
        try:
            # 設定 user.name
            subprocess.run(
                ["git", "config", "--global", "user.name", self.username],
                check=True,
                capture_output=True
            )
            print(f"✅ Git user.name: {self.username}")
            
            # 設定 user.email
            subprocess.run(
                ["git", "config", "--global", "user.email", self.email],
                check=True,
                capture_output=True
            )
            print(f"✅ Git user.email: {self.email}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 設定 Git config 失敗: {e}")
            sys.exit(1)
    
    def show_results(self) -> None:
        """顯示設定結果和下一步指引"""
        print("\n" + "=" * 50)
        print("✅ 設定完成！")
        print("=" * 50)
        
        self.show_public_key()
        self.show_next_steps()
        self.show_verification_steps()
    
    def show_public_key(self) -> None:
        """顯示公鑰"""
        if not self.ssh_pub_key_path or not self.ssh_pub_key_path.exists():
            return
        
        print("\n你的 SSH 公鑰:")
        print("=" * 50)
        with open(self.ssh_pub_key_path, "r", encoding="utf-8") as f:
            public_key = f.read().strip()
            print(public_key)
        print("=" * 50)
    
    # 抽象方法 - 由子類實作
    @abstractmethod
    def get_home_path(self) -> str:
        """取得 HOME 路徑"""
        pass
    
    @abstractmethod
    def _set_home_env(self) -> None:
        """設定 HOME 環境變數（平台特定）"""
        pass
    
    @abstractmethod
    def create_ssh_config_content(self) -> str:
        """建立 SSH config 內容"""
        pass
    
    @abstractmethod
    def get_target_name(self) -> str:
        """取得設定目標名稱"""
        pass
    
    @abstractmethod
    def show_next_steps(self) -> None:
        """顯示下一步指引"""
        pass
    
    @abstractmethod
    def get_verification_command(self) -> str:
        """取得驗證命令"""
        pass
    
    def show_verification_steps(self) -> None:
        """顯示驗證步驟"""
        print("\n🔍 驗證連線:")
        print("-" * 50)
        print(f"執行命令: {self.get_verification_command()}")
        print()
    
    # 工具方法
    @classmethod
    def _check_command(cls, command: str) -> bool:
        """檢查命令是否存在"""
        try:
            subprocess.run(
                [command, "--version"],
                check=True,
                capture_output=True,
                timeout=cls.COMMAND_TIMEOUT
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    @staticmethod
    def _show_ssh_keygen_install_guide() -> None:
        """顯示 ssh-keygen 安裝指南"""
        import platform
        
        print("\n❌ 錯誤: 找不到 ssh-keygen 命令")
        print("\n解決方法:")
        
        os_type = platform.system()
        if os_type == "Windows":
            print("  1. 安裝 Git for Windows")
            print("     下載: https://git-scm.com/")
            print("  2. 或安裝 OpenSSH")
            print("     設定 -> 應用程式 -> 選用功能 -> 新增功能 -> OpenSSH 用戶端")
        elif os_type == "Linux":
            print("  Ubuntu/Debian:")
            print("    sudo apt-get install openssh-client")
            print("  CentOS/RHEL:")
            print("    sudo yum install openssh-clients")
        else:  # macOS
            print("  macOS 應該已預裝 OpenSSH")
            print("  如果沒有，請使用 Homebrew:")
            print("    brew install openssh")
    
    @staticmethod
    def _show_git_install_guide() -> None:
        """顯示 git 安裝指南"""
        import platform
        
        print("\n❌ 錯誤: 找不到 git 命令")
        print("\n解決方法:")
        
        os_type = platform.system()
        if os_type == "Windows":
            print("  下載並安裝 Git for Windows:")
            print("  https://git-scm.com/")
        elif os_type == "Linux":
            print("  Ubuntu/Debian:")
            print("    sudo apt-get install git")
            print("  CentOS/RHEL:")
            print("    sudo yum install git")
        else:  # macOS
            print("  使用 Homebrew:")
            print("    brew install git")
            print("  或下載安裝程式:")
            print("    https://git-scm.com/")
