# main.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from my Python server!"

@app.route('/device', methods=['POST'])
def device():
    data = request.json
    return jsonify({
        "status": "ok",
        "received": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)