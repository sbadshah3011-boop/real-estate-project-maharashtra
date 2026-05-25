import sys
from flask import Flask, jsonify, send_from_directory, send_file, request
from flask_cors import CORS
import json
import os
import threading
import schedule
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "live_data.json")

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "No data yet — click Refresh Now in the dashboard"}


# ── ROUTES ──

@app.route("/")
def index():
    """Serve the dashboard."""
    return send_file(os.path.join(BASE_DIR, "dashboard.html"))


@app.route("/api/data")
def get_data():
    """Return latest scraped data as JSON."""
    return jsonify(load_data())


@app.route("/api/refresh")
def refresh():
    """Trigger scraper + notifier manually."""
    try:
        from scraper import run_scraper
        from notifier import send_email
        print(f"\n[Server] Manual refresh triggered at {datetime.now().strftime('%H:%M:%S')}")
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
    """Health check."""
    data = load_data()
    return jsonify({
        "server": "running",
        "last_updated": data.get("last_updated", "never"),
        "data_fresh": data.get("data_fresh", False),
        "source": data.get("source", "unknown"),
        "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    """Handle new SaaS subscriptions."""
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        if not name or not email:
            return jsonify({"status": "error", "message": "Missing name or email"}), 400

        sub_file = os.path.join(BASE_DIR, "subscribers.json")
        subs = []
        if os.path.exists(sub_file):
            with open(sub_file, "r", encoding="utf-8") as f:
                subs = json.load(f)

        # Add or update subscriber
        existing = next((s for s in subs if s["email"] == email), None)
        if not existing:
            subs.append({
                "name": name,
                "email": email,
                "date_subscribed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            with open(sub_file, "w", encoding="utf-8") as f:
                json.dump(subs, f, indent=2)
            print(f"[Server] New subscriber added: {name} ({email})")

        return jsonify({"status": "ok", "message": "Subscribed successfully"})
    except Exception as e:
        print(f"[Server] Subscribe error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ── SCHEDULER ──

def scheduled_job():
    """Run at 6:00 AM every day."""
    print(f"\n[Scheduler] ⏰ Running daily job at {datetime.now().strftime('%H:%M:%S')}")
    try:
        from scraper import run_scraper
        from notifier import send_email
        run_scraper()
        send_email()
        print("[Scheduler] ✅ Daily job complete")
    except Exception as e:
        print(f"[Scheduler] ❌ Error: {e}")


def run_scheduler():
    """Background thread that runs the daily scheduler."""
    schedule.every().day.at("06:00").do(scheduled_job)
    print("[Scheduler] Scheduled daily job at 06:00 AM IST")
    while True:
        schedule.run_pending()
        time.sleep(60)


# ── STARTUP ──

def startup():
    """Run scraper on first start if no data exists."""
    if not os.path.exists(DATA_FILE):
        print("[Server] No data found — running initial scrape...")
        try:
            from scraper import run_scraper
            run_scraper()
        except Exception as e:
            print(f"[Server] Initial scrape error: {e}")
    else:
        data = load_data()
        print(f"[Server] Existing data found — last updated: {data.get('last_updated','unknown')}")


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🏙️  Pune Estate — Intelligence Dashboard Server")
    print("="*55)
    print(f"  Dashboard: http://localhost:5000")
    print(f"  API:       http://localhost:5000/api/data")
    print(f"  Refresh:   http://localhost:5000/api/refresh")
    print("="*55 + "\n")

    # Run startup check
    startup()

    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
