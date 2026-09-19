import os
import requests

# بيانات الاعتماد الصحيحة بالصيغة النهائيه
bot_token = "8754723524:AAFM43M7iTZEAgiqVutMdr9XHCHcXvz6Bfw"
chat_id = "-1003988112289"       # إضافة البادئة -100 الخاصة بالقنوات والمجموعات
message_thread_id = 5            # رقم الموضوع (Topic) إن وجد

# استلام المحتوى إن وجد، أو استخدام الرسالة الافتراضية
payload = os.environ.get("PAYLOAD") or os.environ.get("MESSAGE")

print("=== Multi-Platform Publisher Engine Started ===")

if not payload or payload.strip() == "null" or not payload.strip():
    print("Notice: Manual test run detected (No payload provided). Setting default test message.")
    payload = "🚀 **إشعار تجريبي أوتوماتيكي من GitHub Actions**\nتم تشغيل المحرك بنجاح وتأكيد الاتصال بالقناة!"

# رابط إرسال الرسائل عبر Telegram API
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "message_thread_id": message_thread_id,
    "text": payload,
    "parse_mode": "Markdown"
}

try:
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Status: SUCCESS - Message sent to Telegram successfully!")
    else:
        print(f"Status: FAILED - Telegram API responded with status code {response.status_code}: {response.text}")
except Exception as e:
    print(f"Status: ERROR - Failed to send request: {e}")
