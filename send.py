import os
import json
import datetime as dt
import requests
from zoneinfo import ZoneInfo

KAUTH = "https://kauth.kakao.com"
KAPI  = "https://kapi.kakao.com"

def today_kst():
    now = dt.datetime.now(ZoneInfo("Asia/Seoul"))
    return now.strftime("%Y%m%d")

def refresh_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": os.environ["KAKAO_REST_API_KEY"],
        "refresh_token": os.environ["KAKAO_REFRESH_TOKEN"],
        "client_secret": os.environ["KAKAO_CLIENT_SECRET"],
    }
    r = requests.post(f"{KAUTH}/oauth/token", data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def send_image_to_me(access_token: str, image_url: str, link_url: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{KAPI}/v2/api/talk/memo/default/send"

    template = {
        "object_type": "feed",
        "content": {
            "title": "오늘의 묵상",
            "image_url": image_url,
            "link": {"web_url": link_url, "mobile_web_url": link_url},
        },
    }

    data = {"template_object": json.dumps(template, ensure_ascii=False)}
    r = requests.post(url, headers=headers, data=data, timeout=30)
    r.raise_for_status()
    print(r.json())

def main():
    ymd = today_kst()
    image_url = f"https://www.qtland.com/data/meditation/A{ymd}.jpg"
    link_url = "https://www.qtland.com/quiet/quiet.php"

    access_token = refresh_access_token()
    send_image_to_me(access_token, image_url, link_url)

if __name__ == "__main__":
    main()

