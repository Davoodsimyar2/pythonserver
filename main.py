from flask import Flask, request, jsonify, render_template_string
import requests
import datetime

app = Flask(__name__)

# -------------------------------
# تنظیمات تلگرام
# -------------------------------
BOT_TOKEN = "8279500877:AAGRNBet6lez8DrHxFTInKliswjrKdFIljM"
CHAT_ID = "456223831"





# -------------------------------
# ذخیره پیام‌ها در حافظه
# -------------------------------
messages = []


# -------------------------------
# تابع ارسال به تلگرام
# -------------------------------
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)


# -------------------------------
# دریافت پیام از موبایل
# -------------------------------
@app.route("/", methods=["GET"])
def receive_message():
    text = request.args.get("text", "")

    if text.strip() == "":
        return "No message received"

    # اضافه کردن زمان
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ذخیره پیام
    messages.append({
        "text": text,
        "time": timestamp
    })

    # ارسال به تلگرام
    send_to_telegram(f"📩 پیام جدید:\n{text}\n⏰ زمان: {timestamp}")

    return "OK"


# -------------------------------
# صفحه وب برای نمایش پیام‌ها
# -------------------------------
@app.route("/messages", methods=["GET"])
def show_messages():
    html_page = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Message Viewer</title>
        <style>
            body { font-family: sans-serif; background: #f3f3f3; padding: 20px; }
            .msg { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px;
                   box-shadow: 0 0 5px rgba(0,0,0,0.1); }
            .time { color: #666; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>پیام‌های دریافتی</h1>
        {% for msg in messages %}
            <div class="msg">
                <div>{{ msg.text }}</div>
                <div class="time">{{ msg.time }}</div>
            </div>
        {% endfor %}
    </body>
    </html>
    """

    return render_template_string(html_page, messages=messages)


# -------------------------------
# اجرای محلی
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
