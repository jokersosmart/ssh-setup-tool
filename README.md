# SSH/Git 環境自動設定工具

🚀 跨平台的 SSH/Git 環境自動設定工具，支援 Gerrit 和 GitHub，一鍵完成開發環境配置。

## ✨ 功能特色

- ✅ **跨平台支援** - Windows、Linux、macOS
- ✅ **多目標支援** - Gerrit、GitHub
- ✅ **全自動設定** - 一鍵完成所有配置
- ✅ **互動式介面** - 清楚的步驟指引
- ✅ **智慧偵測** - 自動偵測作業系統和現有設定
- ✅ **完整錯誤處理** - 友善的錯誤訊息和解決方案

## 🎯 支援的設定

| 作業系統 | Gerrit | GitHub |
|---------|--------|--------|
| Windows | ✅ | ✅ |
| Linux | ✅ | ✅ |
| macOS | ✅ | ✅ |

## 📦 系統需求

- **Python** 3.6 或更高版本
- **Git** 命令列工具
- **OpenSSH** 或 Git Bash (Windows)

## 🚀 快速開始

### Windows

```cmd
setup-env.bat
```

或直接執行 Python 程式：

```cmd
python setup-env.py
```

### Linux / macOS

```bash
chmod +x setup-env.sh
./setup-env.sh
```

或直接執行 Python 程式：

```bash
python3 setup-env.py
```

## 📖 使用說明

### 執行流程

1. **啟動程式** - 執行 `setup-env.bat` (Windows) 或 `setup-env.sh` (Linux/macOS)

2. **確認使用者資訊** - 程式會偵測您的使用者名稱，請確認或修改

3. **選擇設定目標** - 選擇要設定 Gerrit 或 GitHub
   ```
   請選擇設定目標:
     1. Gerrit (公司內部 Code Review)
     2. GitHub (公開 Git 平台)
   
   請輸入 1 或 2:
   ```

4. **輸入 Email** - 輸入您的電子郵件地址
   - Gerrit: 建議使用公司 email (例如: `user@siliconmotion.com`)
   - GitHub: 使用您的 GitHub 註冊 email

5. **確認設定** - 檢查所有資訊是否正確

6. **自動設定** - 程式會執行以下步驟：
   - [1/5] 設定 HOME 環境變數
   - [2/5] 建立 .ssh 資料夾
   - [3/5] 生成 SSH 金鑰
   - [4/5] 建立 SSH config 檔案
   - [5/5] 設定 Git 全域配置

7. **複製公鑰** - 程式會顯示您的 SSH 公鑰，請複製並加到 Gerrit 或 GitHub

8. **驗證連線** - 使用提供的命令驗證 SSH 連線是否成功

### 設定內容

#### HOME 環境變數
- **Windows**: `C:\Users\USERNAME`
- **Linux**: `/home/USERNAME`
- **macOS**: `/Users/USERNAME`

#### SSH 金鑰
- **類型**: RSA 4096-bit
- **位置**: `~/.ssh/id_rsa` 和 `~/.ssh/id_rsa.pub`
- **密碼**: 無 (空密碼)

#### SSH Config

**Gerrit**:
```
Host rd2gerrit01.siliconmotion.com.tw
  HostKeyAlgorithms +ssh-rsa
  PubkeyAcceptedAlgorithms +ssh-rsa
  User <username>
  Port 29418
```

**GitHub**:
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
```

#### Git 全域配置
```bash
git config --global user.name "<username>"
git config --global user.email "<email>"
```

## 🔧 詳細指南

完整的使用指南請參閱 [docs/GUIDE.md](docs/GUIDE.md)

## 🆘 故障排除

遇到問題？請參閱 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

### 常見問題

#### 找不到 ssh-keygen 命令

**Windows**:
1. 安裝 Git for Windows: https://git-scm.com/
2. 或在 Windows 設定中安裝 OpenSSH 用戶端

**Linux**:
```bash
sudo apt-get install openssh-client  # Ubuntu/Debian
sudo yum install openssh-clients     # CentOS/RHEL
```

**macOS**:
```bash
brew install openssh  # 如果需要
```

#### 找不到 git 命令

請安裝 Git: https://git-scm.com/

#### 權限錯誤 (Linux/macOS)

確保您有權限建立和修改 `~/.ssh` 目錄：
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/config
```

## 📝 授權

本專案採用 MIT 授權條款 - 詳見 LICENSE 檔案

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📧 聯絡

如有問題或建議，請開啟 Issue 或聯絡專案維護者。

---

Made with ❤️ for developers
