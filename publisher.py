import os
import requests

def publish_to_tiktok(text, media_url):
    """إرسال الفيديو إلى تيك توك باستخدام TikTok Content Posting API"""
    tiktok_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not tiktok_token:
        print("⚠️ TIKTOK_ACCESS_TOKEN غير متوفر، تخطي النشر على تيك توك.")
        return

    if not media_url:
        print("❌ تيك توك يتطلب فيديو للنشر.")
        return

    print("🚀 جاري رفع الفيديو إلى تيك توك...")
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    
    headers = {
        "Authorization": f"Bearer {tiktok_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    
    payload = {
        "post_info": {
            "title": text[:150],
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False
        },
        "source_info": {
            "source": "URL_UPLOAD",
            "video_url": media_url
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        
        if response.status_code == 200 and res_data.get("error", {}).get("code") == "ok":
            print("✅ تم بنجاح إنشاء جلسة النشر على تيك توك!")
        else:
            print(f"❌ فشل النشر على تيك توك: {res_data}")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال بـ تيك توك: {e}")

def publish_to_facebook(text, media_url):
    """نشر المحتوى على صفحة فيسبوك"""
    page_id = os.getenv("FB_PAGE_ID")
    token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    if not page_id or not token:
        print("⚠️ بيانات فيسبوك (FB_PAGE_ID أو FB_PAGE_ACCESS_TOKEN) غير متوفرة، تخطي النشر.")
        return

    print("🚀 جاري النشر على فيسبوك...")
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    
    payload = {
        "message": text,
        "access_token": token
    }
    
    if media_url:
        # إذا كانت صورة أو رابط ميديا
        url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
        payload["url"] = media_url

    try:
        response = requests.post(url, data=payload)
        res_data = response.json()
        if "id" in res_data:
            print("✅ تم النشر على فيسبوك بنجاح!")
        else:
            print(f"❌ فشل النشر على فيسبوك: {res_data}")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال بفيسبوك: {e}")

def publish_to_instagram(text, media_url):
    """نشر المحتوى على إنستجرام"""
    ig_user_id = os.getenv("IG_USER_ID")
    token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    if not ig_user_id or not token:
        print("⚠️ بيانات إنستجرام غير متوفرة، تخطي النشر.")
        return

    if not media_url:
        print("❌ إنستجرام يتطلب صورة أو فيديو أساسي للنشر.")
        return

    print("🚀 جاري النشر على إنستجرام...")
    
    # الخطوة 1: إنشاء حاوية الوسائط (Media Container)
    container_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
    container_payload = {
        "image_url": media_url,
        "caption": text,
        "access_token": token
    }

    try:
        res = requests.post(container_url, data=container_payload).json()
        creation_id = res.get("id")
        
        if not creation_id:
            print(f"❌ فشل إنشاء حاوية إنستجرام: {res}")
            return

        # الخطوة 2: نشر الحاوية
        publish_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": token
        }
        
        pub_res = requests.post(publish_url, data=publish_payload).json()
        if "id" in pub_res:
            print("✅ تم النشر على إنستجرام بنجاح!")
        else:
            print(f"❌ فشل تأكيد النشر على إنستجرام: {pub_res}")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال بإنستجرام: {e}")

if __name__ == "__main__":
    print("Unified Publisher Engine Ready for Meta & TikTok.")
