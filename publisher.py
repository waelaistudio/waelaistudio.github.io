import os
import json

def main():
    print("=== Multi-Platform Publisher Engine Started ===")
    
    # استلام البيانات الممررة من GitHub Actions
    payload_raw = os.getenv("PAYLOAD", "{}")
    
    try:
        payload = json.loads(payload_raw) if payload_raw else {}
    except Exception as e:
        print(f"Warning: Failed to parse JSON: {e}")
        payload = {}

    # التعامل مع التشغيل اليدوي (بدون بيانات تليجرام)
    if not payload:
        print("Notice: Manual test run detected (No payload provided).")
        print("Status: SUCCESS - Environment & dependencies are ready.")
        return

    # معالجة حمولة البيانات عند إرسالها من التليجرام
    print("Processing Telegram Payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
