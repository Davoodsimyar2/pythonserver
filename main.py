from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# یک متغیر ساده برای نگه‌داری آخرین داده دریافتی
last_data = {}
last_update = 0  # زمان آخرین آپدیت

@app.route("/data", methods=["POST"])
def receive_data():
    """دریافت داده جدید از ESP یا هر کلاینت دیگر"""
    global last_data, last_update
    last_data = request.json
    last_update = time.time()  # ثبت زمان دریافت
    print("Received data:", last_data)
    return jsonify({"status": "success", "received": last_data})

@app.route("/", methods=["GET"])
def home():
    """نمایش داده آخر در مرورگر"""
    if last_data:
        return f"""
        <h2>آخرین داده دریافتی:</h2>
        <pre>{last_data}</pre>
        """
    else:
        return "<h3>هنوز هیچ داده‌ای دریافت نشده است.</h3>"

@app.route("/poll", methods=["GET"])
def poll():
    """
    Long Polling:
    کلاینت (ESP) درخواست GET می‌زند،
    سرور تا timeout صبر می‌کند تا داده جدید بیاید.
    """
    global last_data, last_update
    timeout = 30  # ثانیه، حداکثر انتظار برای داده جدید
    start = time.time()

    while time.time() - start < timeout:
        if last_update > start:  # اگر داده جدید بعد از شروع درخواست آمد
            return jsonify(last_data)
        time.sleep(0.5)  # جلوگیری از مصرف CPU زیاد

    # هیچ داده جدیدی نیامده
    return jsonify({"status": "no new data"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
