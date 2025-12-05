from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# لیست برای ذخیره پیام‌ها
messages = []

# توکن و chat_id تلگرام
BOT_TOKEN = "8279500877:AAGRNBet6lez8DrHxFTInKliswjrKdFIljM"
CHAT_ID = "456223831"

# ------------------------------------
# صفحه وب برای نمایش پیام‌ها
# ------------------------------------
@app.route("/")
def home():
    if not messages:
        return "<h3>No message received</h3>"

    html = "<h2>Received Messages:</h2><ul>"
    for m in messages:
        html += f"<li>{m}</li>"
    html += "</ul>"
    return html


# ------------------------------------
# API برای دریافت پیام از اندروید
# ------------------------------------
@app.route("/message", methods=["POST"])
def message():
    text = request.form.get("text")

    if not text:
        return "ERROR: No text provided", 400

    # ذخیره پیام در حافظه سرور
    messages.append(text)

    # ارسال به تلگرام
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": text})

    return "OK"


# ------------------------------------
# اجرای سرور
# ------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
