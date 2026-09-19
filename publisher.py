import os
import requests

# 1. إعدادات Telegram Channel & Bot
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "8754723524:AAFM43M7iTZEAgiqVutMdr9XHCHcXvz6Bfw"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or "-1003988112289"
TELEGRAM_TOPIC_ID = os.environ.get("TELEGRAM_TOPIC_ID") or 5

# 2. إعدادات Meta API (Facebook Page & Instagram wael.ai.studio)
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
IG_USER_ID = os.environ.get("IG_USER_ID")

# 3. إعدادات TikTok Developer API (@waelmohamden)
TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN")

# استلام نص المحتوى ورابط الوسائط
MESSAGE = os.environ.get("PAYLOAD") or os.environ.get("MESSAGE") or "تحديث جديد من Wael AiStudio 🚀"
MEDIA_URL = os.environ.get("MEDIA_URL")

print("=== Wael AiStudio: Omnichannel Publisher Engine Started ===")

def publish_to_telegram(text, media_url=None):
    """النشر على قناة تليجرام"""
    print("[+] Publishing to Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "message_thread_id": TELEGRAM_TOPIC_ID
    }
    res = requests.post(url, json=payload)
    print(f"Telegram Response: {res.status_code}")

def publish_to_facebook(text, media_url=None):
    """النشر على صفحة فيسبوك Wael AiStudio"""
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID:
        print("[-] Meta FB Tokens missing, skipping Facebook...")
        return
    print("[+] Publishing to Facebook Page...")
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/feed"
    payload = {"message": text, "access_token": FB_PAGE_ACCESS_TOKEN}
    res = requests.post(url, data=payload)
    print(f"Facebook Response: {res.status_code}")

def publish_to_instagram(media_url, caption):
    """النشر على حساب إنستجرام wael.ai.studio"""
    if not FB_PAGE_ACCESS_TOKEN or not IG_USER_ID or not media_url:
        print("[-] Meta IG Credentials or Media URL missing, skipping Instagram...")
        return
    print("[+] Publishing to Instagram Reels/Posts...")
    container_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "image_url" if media_url.endswith(('.jpg', '.png')) else "video_url": media_url,
        "caption": caption,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }
    res = requests.post(container_url, data=payload)
    if res.status_code == 200:
        creation_id = res.json().get("id")
        pub_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        res_pub = requests.post(pub_url, data={"creation_id": creation_id, "access_token": FB_PAGE_ACCESS_TOKEN})
        print(f"Instagram Publish Status: {res_pub.status_code}")

def publish_to_tiktok(video_url, title):
    """النشر على تيك توك @waelmohamden"""
    if not TIKTOK_ACCESS_TOKEN or not video_url:
        print("[-] TikTok Credentials or Video URL missing, skipping TikTok...")
        return
    print("[+] Publishing to TikTok...")
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "post_info": {"title": title, "privacy_level": "PUBLIC_TO_EVERYONE"},
        "source_info": {"source": "FILE_URL", "video_url": video_url}
    }
    res = requests.post(url, headers=headers, json=body)
    print(f"TikTok Response: {res.status_code}")

if __name__ == "__main__":
    publish_to_telegram(MESSAGE, MEDIA_URL)
    publish_to_facebook(MESSAGE, MEDIA_URL)
    publish_to_instagram(MEDIA_URL, MESSAGE)
    publish_to_tiktok(MEDIA_URL, MESSAGE)
    print("=== All Direct Publishing Jobs Completed ===")
