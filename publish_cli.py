import sys
import os
from publisher import publish_to_tiktok, publish_to_facebook, publish_to_instagram
# استيراد دالة تليجرام إذا كانت موجودة، أو يمكنك دمجها هنا

def main():
    print("=== نظام النشر السريع (Waelaistudio CLI) ===")
    
    if len(sys.argv) < 2:
        print("الاستخدام: python publish_cli.py \"نص المنشور\" [رابط الميديا]")
        return

    text = sys.argv[1]
    media_url = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\n📝 النص: {text}")
    if media_url:
        print(f"🔗 الوسائط: {media_url}")
    print("-" * 40)

    print("جاري توزيع النشر على المنصات المفعلة...")
    
    # استدعاء منصات Meta و TikTok
    publish_to_facebook(text, media_url)
    publish_to_instagram(text, media_url)
    publish_to_tiktok(text, media_url)
    
    print("\n✨ تمت عملية محاولة النشر على المنصات المتاحة!")

if __name__ == "__main__":
    main()
