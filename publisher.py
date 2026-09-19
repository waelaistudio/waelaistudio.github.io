import os
import json
import requests

# 1. Telegram Settings
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "8754723524:AAFM43M7iTZEAgiqVutMdr9XHCHcXvz6Bfw"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or "-1003988112289"
TELEGRAM_TOPIC_ID = os.environ.get("TELEGRAM_TOPIC_ID") or 5

# 2. Meta API Settings
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
IG_USER_ID = os.environ.get("IG_USER_ID")

# 3. TikTok Settings
TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN")

# Default Message & Media URL
MESSAGE = "تحديث جديد من Wael AiStudio 🚀"
MEDIA_URL = None

# Extract payload from GitHub Actions event file
event_path = os.environ.get("GITHUB_EVENT_PATH")
if event_path and os.path.exists(event_path):
    try:
        with open(event_path, "r", encoding="utf-8") as f:
            event_data = json.load(f)
            client_payload = event_data.get("client_payload", {})
            MESSAGE = client_payload.get("message") or MESSAGE
            MEDIA_URL = client_payload.get("media_url") or MEDIA_URL
    except Exception as e:
        print(f"[-] Error reading event payload: {e}")

print("=== Wael AiStudio: Omnichannel Publisher Engine Started ===")

def publish_to_telegram(text, media_url=None):
    print("[+] Publishing to Telegram...")
    
    # إذا وجد رابط وسائط (صورة/فيديو)
    if media_url:
        is_video = any(media_url.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi']) or 'reel' in media_url.lower()
        method = "sendVideo" if is_video else "sendPhoto"
        param_name = "video" if is_video else "photo"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            param_name: media_url,
            "caption": text,
            "message_thread_id": TELEGRAM_TOPIC_ID
        }
        res = requests.post(url, json=payload)
        
        # إذا فشل إرسال الوسائط كملف مباشر (مثلاً رابط ويب عادي)، يتم إرساله كـ HTML مع النص
        if res.status_code != 200:
            print("[-] Direct media link failed, sending as embedded link...")
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            formatted_text = f"{text}\n\n🔗 <b>Media:</b> {media_url}"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": formatted_text,
                "parse_mode": "HTML",
                "message_thread_id": TELEGRAM_TOPIC_ID
            }
            res = requests.post(url, json=payload)
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "message_thread_id": TELEGRAM_TOPIC_ID
        }
        res = requests.post(url, json=payload)

    print(f"Telegram Response: {res.status_code}")

def publish_to_facebook(text, media_url=None):
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID:
        print("[-] Meta FB Tokens missing, skipping Facebook...")
        return
    print("[+] Publishing to Facebook Page...")
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/feed"
    payload = {"message": text, "access_token": FB_PAGE_ACCESS_TOKEN}
    res = requests.post(url, data=payload)
    print(f"Facebook Response: {res.status_code}")

def publish_to_instagram(media_url, caption):
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
