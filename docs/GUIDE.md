# SSH/Git 環境自動設定工具 - 完整使用指南

本指南提供詳細的安裝、設定和使用說明。

## 📋 目錄

- [安裝前準備](#安裝前準備)
- [詳細使用步驟](#詳細使用步驟)
- [Gerrit 設定說明](#gerrit-設定說明)
- [GitHub 設定說明](#github-設定說明)
- [進階設定](#進階設定)
- [命令列選項](#命令列選項)

## 🔧 安裝前準備

### 1. 安裝 Python

本工具需要 Python 3.6 或更高版本。

#### Windows
1. 下載 Python: https://www.python.org/downloads/
2. 執行安裝程式
3. **重要**: 勾選 "Add Python to PATH"
4. 驗證安裝：
   ```cmd
   python --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install python3
python3 --version
```

#### macOS
```bash
# 使用 Homebrew
brew install python3
python3 --version
```

### 2. 安裝 Git

#### Windows
1. 下載 Git for Windows: https://git-scm.com/
2. 執行安裝程式
3. 建議選項：
   - 使用 Git from the command line and also from 3rd-party software
   - Use the OpenSSL library
   - Checkout Windows-style, commit Unix-style line endings
4. 驗證安裝：
   ```cmd
   git --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install git
git --version
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install git
git --version
```

#### macOS
```bash
# 方法 1: 使用 Xcode Command Line Tools
xcode-select --install

# 方法 2: 使用 Homebrew
brew install git

git --version
```

### 3. 安裝 OpenSSH (Windows 可選)

#### Windows
如果您已安裝 Git for Windows，則已包含 SSH 工具。

如需單獨安裝 OpenSSH：
1. 開啟設定 -> 應用程式
2. 點擊「選用功能」
3. 點擊「新增功能」
4. 搜尋並安裝「OpenSSH 用戶端」

#### Linux/macOS
通常已預裝。如未安裝：

```bash
# Ubuntu/Debian
sudo apt-get install openssh-client

# CentOS/RHEL
sudo yum install openssh-clients

# macOS (如需要)
brew install openssh
```

## 📖 詳細使用步驟

### 步驟 1: 下載工具

```bash
git clone https://github.com/jokersosmart/ssh-setup-tool.git
cd ssh-setup-tool
```

### 步驟 2: 執行設定程式

#### Windows
```cmd
setup-env.bat
```

#### Linux/macOS
```bash
chmod +x setup-env.sh
./setup-env.sh
```

### 步驟 3: 互動式設定

#### 3.1 確認使用者名稱
```
👤 偵測到使用者名稱: john.doe
確認使用者名稱 (直接按 Enter 確認，或輸入新名稱):
```

- 按 `Enter` 使用偵測到的名稱
- 或輸入您想要的使用者名稱

#### 3.2 選擇設定目標
```
請選擇設定目標:
  1. Gerrit (公司內部 Code Review)
  2. GitHub (公開 Git 平台)

請輸入 1 或 2:
```

輸入 `1` 或 `2` 並按 `Enter`

#### 3.3 輸入 Email
```
📧 Gerrit 建議使用公司 email
預設: john.doe@siliconmotion.com
請輸入 email (直接按 Enter 使用預設):
```

- 按 `Enter` 使用預設 email
- 或輸入您的 email 地址

#### 3.4 確認設定資訊
```
==================================================
🖥️  作業系統: Windows
👤 使用者名稱: john.doe
📧 電子郵件: john.doe@siliconmotion.com
🎯 設定目標: Gerrit (公司內部 Code Review)

確認以上資訊無誤? (y/N):
```

輸入 `y` 並按 `Enter` 開始設定

### 步驟 4: 自動設定過程

程式會自動執行 5 個步驟：

#### [1/5] 設定 HOME 環境變數
- Windows: 使用 `setx` 設定
- Linux/macOS: 寫入 `~/.bashrc` 或 `~/.zshrc`

#### [2/5] 建立 .ssh 資料夾
- 建立 `~/.ssh` 目錄
- 設定權限為 700 (Linux/macOS)

#### [3/5] 生成 SSH 金鑰
- 使用 RSA 4096-bit 加密
- 檔案：`id_rsa` 和 `id_rsa.pub`
- 如果金鑰已存在，會詢問是否覆蓋

#### [4/5] 建立 SSH config 檔案
- 建立 `~/.ssh/config`
- 如果 config 已存在，可選擇覆蓋、附加或跳過

#### [5/5] 設定 Git 全域配置
- 設定 `user.name`
- 設定 `user.email`

### 步驟 5: 複製並上傳公鑰

設定完成後，程式會顯示您的 SSH 公鑰：

```
你的 SSH 公鑰:
==================================================
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ... john.doe@siliconmotion.com
==================================================
```

複製整個公鑰（從 `ssh-rsa` 開始到 email 結束）

## 🔐 Gerrit 設定說明

### 上傳公鑰到 Gerrit

1. **登入 Gerrit**
   - 開啟 https://rd2gerrit01.siliconmotion.com.tw
   - 使用您的公司帳號登入

2. **進入設定頁面**
   - 點擊右上角的使用者圖示
   - 選擇「Settings」

3. **加入 SSH 公鑰**
   - 左側選單點擊「SSH Public Keys」
   - 點擊「Add Key」按鈕
   - 在文字框中貼上您的公鑰
   - 點擊「Add」按鈕

4. **驗證設定**
   ```bash
   ssh -p 29418 username@rd2gerrit01.siliconmotion.com.tw
   ```
   
   成功的話會看到：
   ```
   ****    Welcome to Gerrit Code Review    ****
   
   Hi [Your Name], you have successfully connected over SSH.
   ```

### Gerrit 常用命令

#### Clone 專案
```bash
git clone ssh://username@rd2gerrit01.siliconmotion.com.tw:29418/project-name
```

#### 設定 commit-msg hook
```bash
cd project-name
curl -Lo .git/hooks/commit-msg \
  https://rd2gerrit01.siliconmotion.com.tw/tools/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

#### Push for review
```bash
git push origin HEAD:refs/for/master
```

## 🐙 GitHub 設定說明

### 上傳公鑰到 GitHub

1. **登入 GitHub**
   - 開啟 https://github.com
   - 使用您的帳號登入

2. **進入 SSH 設定頁面**
   - 方法 1: 直接開啟 https://github.com/settings/keys
   - 方法 2: 
     - 點擊右上角頭像
     - 選擇「Settings」
     - 左側選單點擊「SSH and GPG keys」

3. **加入新的 SSH 金鑰**
   - 點擊「New SSH key」按鈕
   - **Title**: 輸入描述（例如：「My Work PC」）
   - **Key**: 貼上您的公鑰
   - 點擊「Add SSH key」按鈕
   - 可能需要輸入密碼確認

4. **驗證設定**
   ```bash
   ssh -T git@github.com
   ```
   
   成功的話會看到：
   ```
   Hi username! You've successfully authenticated, but GitHub does not provide shell access.
   ```

### GitHub 常用命令

#### Clone 專案
```bash
git clone git@github.com:username/repository.git
```

#### 設定 remote
```bash
git remote add origin git@github.com:username/repository.git
```

#### Push 到 GitHub
```bash
git push -u origin main
```

## ⚙️ 進階設定

### 多個 SSH 金鑰

如果您需要為不同的服務使用不同的 SSH 金鑰：

1. **生成額外的金鑰**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "email@example.com" -f ~/.ssh/id_rsa_github
   ```

2. **修改 SSH config**
   編輯 `~/.ssh/config`：
   ```
   # Gerrit
   Host rd2gerrit01.siliconmotion.com.tw
     HostKeyAlgorithms +ssh-rsa
     PubkeyAcceptedAlgorithms +ssh-rsa
     User username
     Port 29418
     IdentityFile ~/.ssh/id_rsa
   
   # GitHub
   Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_rsa_github
   ```

### SSH Agent

#### Windows (Git Bash)
```bash
# 啟動 ssh-agent
eval $(ssh-agent -s)

# 加入金鑰
ssh-add ~/.ssh/id_rsa
```

#### Linux/macOS
```bash
# 啟動 ssh-agent
eval "$(ssh-agent -s)"

# 加入金鑰
ssh-add ~/.ssh/id_rsa

# 自動啟動 (加入 ~/.bashrc 或 ~/.zshrc)
if [ -z "$SSH_AUTH_SOCK" ] ; then
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa
fi
```

### Git 進階配置

#### 設定編輯器
```bash
git config --global core.editor "vim"  # 或 nano, emacs, code
```

#### 設定別名
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

#### 設定換行符
```bash
# Windows
git config --global core.autocrlf true

# Linux/macOS
git config --global core.autocrlf input
```

## 🔍 檢查設定

### 檢查 Git 配置
```bash
git config --global --list
```

### 檢查 SSH 金鑰
```bash
# 列出金鑰
ls -la ~/.ssh

# 查看公鑰
cat ~/.ssh/id_rsa.pub
```

### 檢查 SSH config
```bash
cat ~/.ssh/config
```

### 測試 SSH 連線
```bash
# Gerrit
ssh -v -p 29418 username@rd2gerrit01.siliconmotion.com.tw

# GitHub
ssh -vT git@github.com
```

## 📚 參考資源

- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub SSH 文檔](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Gerrit 文檔](https://gerrit-review.googlesource.com/Documentation/)
- [SSH 配置指南](https://www.ssh.com/academy/ssh/config)

## 💡 小技巧

1. **Windows 使用者**: 建議使用 Git Bash 而非 CMD，以獲得更好的體驗
2. **多專案開發**: 使用不同的 SSH config Host 別名管理多個帳號
3. **安全性**: 定期更換 SSH 金鑰（建議每年一次）
4. **備份**: 將 `~/.ssh` 目錄備份到安全的地方
5. **權限**: Linux/macOS 務必確保正確的檔案權限，否則 SSH 會拒絕使用金鑰

---

回到 [README](../README.md) | 查看 [故障排除](TROUBLESHOOTING.md)
