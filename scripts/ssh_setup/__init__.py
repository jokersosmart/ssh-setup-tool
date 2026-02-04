"""SSH Setup Tool - 跨平台 SSH/Git 環境自動設定工具

此模組提供跨平台的 SSH 和 Git 環境自動設定功能，
支援 Windows、Linux 和 macOS，以及 Gerrit 和 GitHub。
"""

__version__ = "1.0.0"
__author__ = "SSH Setup Tool Contributors"

from .base import SSHSetupBase
from .windows_gerrit import WindowsGerritSetup
from .windows_github import WindowsGitHubSetup
from .linux_gerrit import LinuxGerritSetup
from .linux_github import LinuxGitHubSetup

__all__ = [
    "SSHSetupBase",
    "WindowsGerritSetup",
    "WindowsGitHubSetup",
    "LinuxGerritSetup",
    "LinuxGitHubSetup",
]
