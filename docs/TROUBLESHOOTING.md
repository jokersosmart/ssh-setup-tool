# SSH/Git 環境設定工具 - 故障排除指南

本文檔提供常見問題的解決方案和手動設定步驟。

## 📋 目錄

- [常見錯誤](#常見錯誤)
- [平台特定問題](#平台特定問題)
- [連線問題](#連線問題)
- [權限問題](#權限問題)
- [手動設定步驟](#手動設定步驟)

## 🔧 常見錯誤

### 1. `ssh-keygen: command not found`

**問題描述**: 系統找不到 ssh-keygen 命令

**解決方案**:

#### Windows
**方法 1: 安裝 Git for Windows** (推薦)
1. 下載: https://git-scm.com/download/win
2. 執行安裝程式
3. 重新啟動終端機

**方法 2: 安裝 OpenSSH**
1. 開啟「設定」-> 「應用程式」
2. 點擊「選用功能」
3. 點擊「新增功能」
4. 搜尋「OpenSSH 用戶端」
5. 點擊「安裝」
6. 重新啟動終端機

**驗證安裝**:
```cmd
ssh-keygen -V
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install openssh-client
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install openssh-clients
```

#### macOS
OpenSSH 應該已預裝。如果沒有：
```bash
brew install openssh
```

### 2. `git: command not found`

**問題描述**: 系統找不到 git 命令

**解決方案**:

#### Windows
1. 下載 Git for Windows: https://git-scm.com/download/win
2. 執行安裝程式
3. 確保勾選「Add Git to PATH」
4. 重新啟動終端機

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install git
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install git
```

#### macOS
```bash
# 方法 1: Xcode Command Line Tools
xcode-select --install

# 方法 2: Homebrew
brew install git
```

### 3. `Permission denied (publickey)`

**問題描述**: SSH 連線被拒絕

**可能原因**:
- 公鑰未上傳到伺服器
- 金鑰權限不正確
- 使用了錯誤的金鑰

**解決方案**:

#### 步驟 1: 確認公鑰已上傳
- **Gerrit**: https://rd2gerrit01.siliconmotion.com.tw -> Settings -> SSH Public Keys
- **GitHub**: https://github.com/settings/keys

#### 步驟 2: 檢查金鑰權限 (Linux/macOS)
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/config
```

#### 步驟 3: 測試連線（詳細模式）
```bash
# Gerrit
ssh -v -p 29418 username@rd2gerrit01.siliconmotion.com.tw

# GitHub
ssh -vT git@github.com
```

查看輸出中的錯誤訊息，通常會指出具體問題。

### 4. Python 版本錯誤

**問題描述**: `Python version too old` 或類似錯誤

**解決方案**:

#### 檢查 Python 版本
```bash
python --version  # 或 python3 --version
```

需要 Python 3.6 或更高版本。

#### 升級 Python

**Windows**:
1. 下載最新版: https://www.python.org/downloads/
2. 執行安裝程式

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install python3.8
```

**Linux (CentOS/RHEL)**:
```bash
sudo yum install python38
```

**macOS**:
```bash
brew install python3
```

### 5. `setx` 命令失敗 (Windows)

**問題描述**: Windows 上設定環境變數失敗

**解決方案**:

#### 手動設定 HOME 環境變數
1. 右鍵點擊「本機」或「我的電腦」
2. 選擇「內容」
3. 點擊「進階系統設定」
4. 點擊「環境變數」
5. 在「使用者變數」區塊點擊「新增」
6. 變數名稱: `HOME`
7. 變數值: `C:\Users\YourUsername`
8. 點擊「確定」
9. 重新啟動終端機

## 🖥️ 平台特定問題

### Windows

#### 問題: 路徑中的反斜線問題

**解決方案**: 在 Git Bash 中使用，或在路徑中使用正斜線：
```bash
# 不好
cd C:\Users\username\.ssh

# 好
cd /c/Users/username/.ssh
# 或
cd C:/Users/username/.ssh
```

#### 問題: Git Bash 無法執行 Python

**解決方案**: 確保 Python 在 PATH 中：
```bash
# 檢查
which python

# 如果找不到，手動指定完整路徑
/c/Python39/python.exe setup-env.py
```

#### 問題: Windows 防火牆阻擋連線

**解決方案**:
1. 開啟「Windows Defender 防火牆」
2. 點擊「允許應用程式或功能通過 Windows Defender 防火牆」
3. 找到「Git」或「SSH」並勾選
4. 點擊「確定」

### Linux

#### 問題: SELinux 阻擋 SSH

**解決方案**:
```bash
# 臨時停用 SELinux
sudo setenforce 0

# 或設定 SELinux 上下文
restorecon -R -v ~/.ssh
```

#### 問題: 權限錯誤

**解決方案**:
```bash
# 修正 .ssh 目錄權限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
chmod 644 ~/.ssh/*.pub
```

### macOS

#### 問題: Keychain 問題

**解決方案**:
```bash
# 加入金鑰到 keychain
ssh-add --apple-use-keychain ~/.ssh/id_rsa

# 或編輯 ~/.ssh/config
Host *
  UseKeychain yes
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_rsa
```

## 🌐 連線問題

### Gerrit 連線失敗

#### 問題: `Connection timed out`

**檢查清單**:
1. 確認網路連線
2. 確認 Gerrit 伺服器運作中
3. 檢查公司防火牆設定
4. 確認 Port 29418 開放

**測試連線**:
```bash
# 測試網路連線
ping rd2gerrit01.siliconmotion.com.tw

# 測試 SSH port
telnet rd2gerrit01.siliconmotion.com.tw 29418
# 或
nc -zv rd2gerrit01.siliconmotion.com.tw 29418
```

#### 問題: `no mutual signature algorithm`

**解決方案**: 確認 SSH config 包含以下設定：
```
Host rd2gerrit01.siliconmotion.com.tw
  HostKeyAlgorithms +ssh-rsa
  PubkeyAcceptedAlgorithms +ssh-rsa
  User username
  Port 29418
```

### GitHub 連線失敗

#### 問題: `Connection reset by peer`

**可能原因**:
- 網路問題
- GitHub 服務中斷
- 防火牆阻擋

**解決方案**:

1. **檢查 GitHub 狀態**: https://www.githubstatus.com/

2. **使用 HTTPS 代替 SSH** (臨時方案):
   ```bash
   git clone https://github.com/username/repository.git
   ```

3. **測試 SSH 連線**:
   ```bash
   ssh -T git@github.com
   ```

4. **使用 GitHub CLI** (選項):
   ```bash
   # Windows
   winget install GitHub.cli
   
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   ```

## 🔐 權限問題

### Linux/macOS SSH 權限要求

SSH 對檔案權限有嚴格要求：

```bash
# .ssh 目錄: 只有擁有者可以讀寫執行
chmod 700 ~/.ssh

# 私鑰: 只有擁有者可以讀寫
chmod 600 ~/.ssh/id_rsa

# 公鑰: 擁有者可讀寫，其他人可讀
chmod 644 ~/.ssh/id_rsa.pub

# config 檔案: 只有擁有者可以讀寫
chmod 600 ~/.ssh/config

# authorized_keys (如果有): 只有擁有者可以讀寫
chmod 600 ~/.ssh/authorized_keys
```

**快速修正所有權限**:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa ~/.ssh/config
chmod 644 ~/.ssh/id_rsa.pub
```

### Windows 權限問題

Windows 通常不需要特別設定權限，但如果遇到問題：

1. 右鍵點擊 `.ssh` 資料夾
2. 選擇「內容」-> 「安全性」
3. 確保只有您的使用者帳號有存取權限

## 🛠️ 手動設定步驟

如果自動化工具無法運作，您可以手動設定：

### 1. 手動設定 HOME 環境變數

#### Windows (CMD)
```cmd
setx HOME "C:\Users\YourUsername"
```

#### Windows (PowerShell)
```powershell
[Environment]::SetEnvironmentVariable("HOME", "C:\Users\YourUsername", "User")
```

#### Linux/macOS (Bash)
```bash
echo 'export HOME="/home/yourusername"' >> ~/.bashrc
source ~/.bashrc
```

#### Linux/macOS (Zsh)
```bash
echo 'export HOME="/Users/yourusername"' >> ~/.zshrc
source ~/.zshrc
```

### 2. 手動建立 .ssh 資料夾

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh  # Linux/macOS only
```

### 3. 手動生成 SSH 金鑰

```bash
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

按提示操作：
- 檔案位置: 按 Enter (使用預設)
- 密碼: 按 Enter (不設密碼) 或輸入密碼

### 4. 手動建立 SSH config

#### Gerrit
建立或編輯 `~/.ssh/config`:
```bash
Host rd2gerrit01.siliconmotion.com.tw
  HostKeyAlgorithms +ssh-rsa
  PubkeyAcceptedAlgorithms +ssh-rsa
  User yourusername
  Port 29418
```

#### GitHub
```bash
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
```

設定權限 (Linux/macOS):
```bash
chmod 600 ~/.ssh/config
```

### 5. 手動設定 Git 配置

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 6. 手動複製公鑰

```bash
# Linux/macOS
cat ~/.ssh/id_rsa.pub

# Windows (CMD)
type %USERPROFILE%\.ssh\id_rsa.pub

# Windows (PowerShell)
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub

# Windows (Git Bash)
cat ~/.ssh/id_rsa.pub
```

複製輸出的內容並上傳到 Gerrit 或 GitHub。

## 🔍 診斷工具

### SSH 詳細模式

使用 `-v`、`-vv` 或 `-vvv` 選項查看詳細輸出：

```bash
# 一般詳細
ssh -v git@github.com

# 更詳細
ssh -vv git@github.com

# 最詳細
ssh -vvv git@github.com
```

### 檢查 SSH Agent

```bash
# 檢查 agent 是否執行
echo $SSH_AUTH_SOCK

# 列出已加入的金鑰
ssh-add -l

# 加入金鑰
ssh-add ~/.ssh/id_rsa
```

### Git 診斷

```bash
# 檢查 Git 配置
git config --list --show-origin

# 測試 Git 連線
git ls-remote git@github.com:username/repository.git
```

## 📞 取得協助

如果以上方法都無法解決問題：

1. **檢查完整錯誤訊息**: 記錄完整的錯誤輸出
2. **收集系統資訊**: 作業系統版本、Python 版本、Git 版本
3. **搜尋類似問題**: Google、Stack Overflow
4. **開啟 Issue**: https://github.com/jokersosmart/ssh-setup-tool/issues
5. **聯絡系統管理員**: 如果是公司內部 Gerrit 問題

## 📚 額外資源

- [SSH 官方文檔](https://www.openssh.com/manual.html)
- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub SSH 故障排除](https://docs.github.com/en/authentication/troubleshooting-ssh)
- [Stack Overflow - SSH Tag](https://stackoverflow.com/questions/tagged/ssh)

---

回到 [README](../README.md) | 查看 [使用指南](GUIDE.md)
