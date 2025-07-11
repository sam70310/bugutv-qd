# Bugutv 自動簽到腳本

<div align="left">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License: Apache 2.0">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey" alt="Platform">
</div>

## 📖 介紹
本專案為布谷TV（bugutv.vip）自動登入並每日簽到的 Python 腳本，支援多帳號、異步執行與定時排程。

## 📦 Packages

- httpx
- beautifulsoup4
- apscheduler
- python-dotenv

## ⚙️ 安裝

1. 安裝 Python 3.8 以上版本。
2. 在專案根目錄下建立 `.env` 檔案，內容格式如下（請勿換行、勿加註解）：

```
BUGUTV_ACCOUNTS=[{"username": "帳號1", "password": "密碼1"}, {"username": "帳號2", "password": "密碼2"}]
```

範例：
```
BUGUTV_ACCOUNTS=[{"username": "admin", "password": "admin"}, {"username": "admin2", "password": "admin2"}]
```

3. 安裝必要套件：

```bash
pip install -r requirement.txt
```

## 🚀 執行方式

```bash
python3 mybugutv.py
```

腳本會自動根據程式內設定的排程時間（預設每日中午12點）自動執行所有帳號的登入、簽到與登出。

## ⚠️ 免責聲明

- 本腳本僅供學術研究與自動化學習用途，請勿用於任何商業或違反網站規範之行為。
- 使用本腳本造成的任何後果（如帳號被封、資料遺失等）均由使用者自行承擔，作者不承擔任何法律責任。
- 請尊重目標網站的使用條款與隱私政策。
