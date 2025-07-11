import asyncio
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
import os
import json
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 從環境變數讀取帳號密碼設定
ACCOUNTS = json.loads(os.getenv("BUGUTV_ACCOUNTS", "[]"))

LOGIN_URL = "https://www.bugutv.vip/wp-admin/admin-ajax.php"
USER_URL = "https://www.bugutv.vip/user"
SIGN_URL = LOGIN_URL

async def login_and_sign(account):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        payload = {
            "action": "user_login",
            "username": account["username"],
            "password": account["password"]
        }
        resp = await client.post(LOGIN_URL, data=payload)
        try:
            data = resp.json()
        except Exception:
            print(f"[{account['username']}] 登入回應非JSON: {resp.text}")
            return
        if resp.status_code == 200 and data.get("status") == "1":
            print(f"[{account['username']}] 登入成功，開始簽到...")
            # 取得 data-nonce
            user_page = await client.get(USER_URL)
            soup = BeautifulSoup(user_page.text, "html.parser")
            btn = soup.find("button", class_="go-user-qiandao")
            if not btn or not btn.has_attr("data-nonce"):
                print(f"[{account['username']}] 找不到 data-nonce，無法簽到")
                return
            data_nonce = btn["data-nonce"]
            # 發送簽到
            sign_payload = {
                "action": "user_qiandao",
                "nonce": data_nonce
            }
            sign_resp = await client.post(SIGN_URL, data=sign_payload)
            try:
                sign_data = sign_resp.json()
            except Exception:
                print(f"[{account['username']}] 簽到回應非JSON: {sign_resp.text}")
                return
            print(f"[{account['username']}] 簽到狀態: {sign_data.get('msg')}")
            # 登出
            LOGOUT_URL = "https://www.bugutv.vip/wp-login.php?action=logout&redirect_to=https%3A%2F%2Fwww.bugutv.vip&_wpnonce=790ab0f28a"
            logout_resp = await client.get(LOGOUT_URL, follow_redirects=False)
        else:
            print(f"[{account['username']}] 登入失敗: {resp.text}")

async def daily_sign():
    tasks = [login_and_sign(acc) for acc in ACCOUNTS]
    await asyncio.gather(*tasks)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_sign, 'cron', hour=12, minute=00)  # 每天中午12點執行簽到
    scheduler.start()
    print("自動簽到排程已啟動，按 Ctrl+C 結束...")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())