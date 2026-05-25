import sys
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "live_data.json")

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "No data yet"}


@app.route("/")
def index():
    return send_file(os.path.join(BASE_DIR, "dashboard.html"))


@app.route("/api/data")
def get_data():
    return jsonify(load_data())


@app.route("/api/refresh")
def refresh():
    try:
        from scraper import run_scraper
        from notifier import send_email

        data = run_scraper()
        sent = send_email()

        return jsonify({
            "status": "ok",
            "refreshed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email_sent": sent,
            "source": data.get("source", "unknown")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/status")
def status():
    data = load_data()
    return jsonify({
        "server": "running",
        "last_updated": data.get("last_updated", "never"),
        "data_fresh": data.get("data_fresh", False)
    })


@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"status": "error"}), 400

        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500