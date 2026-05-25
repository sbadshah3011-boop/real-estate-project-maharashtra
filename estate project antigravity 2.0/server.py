from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "live_data.json")

app = Flask(__name__)
CORS(app)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"message": "No data yet"}

@app.route("/")
def index():
    return send_file(os.path.join(BASE_DIR, "dashboard.html"))

@app.route("/api/data")
def get_data():
    return jsonify(load_data())

@app.route("/api/status")
def status():
    return jsonify({
        "status": "running",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/api/refresh")
def refresh():
    return jsonify({
        "message": "Refresh temporarily disabled"
    })

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    return jsonify({"status": "ok"})
