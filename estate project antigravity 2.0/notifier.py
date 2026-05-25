import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DATA_FILE   = os.path.join(BASE_DIR, "live_data.json")


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def build_email_html(data):
    """Build a beautiful HTML email from the market data."""
    summary  = data.get("summary", {})
    markets  = data.get("markets", [])
    updated  = data.get("last_updated_date", datetime.now().strftime("%d %B %Y"))
    source   = data.get("source", "Research data")
    fresh    = data.get("data_fresh", False)

    # Top 3 markets by appreciation
    top3 = sorted(markets, key=lambda x: x.get("appr", 0), reverse=True)[:3]

    top3_rows = ""
    for m in top3:
        top3_rows += f"""
        <tr>
          <td style="padding:10px 14px;border-bottom:1px solid #1e2640;color:#94a3b8">{m.get('city', '')}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #1e2640;font-weight:600;color:#e8eaf6">{m['locality']}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #1e2640;color:#94a3b8">{m['standard']}</td>
          <td style="padding:10px 14px;border-bottom:1px solid #1e2640;font-weight:700;color:#22c55e">{m['appr']}%</td>
          <td style="padding:10px 14px;border-bottom:1px solid #1e2640;color:#94a3b8;font-size:12px">{m['drivers']}</td>
        </tr>"""

    freshness_badge = (
        '<span style="background:#14b8a6;color:#fff;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700">🟢 LIVE DATA</span>'
        if fresh else
        '<span style="background:#f59e0b;color:#000;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700">📦 CACHED DATA</span>'
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Maharashtra Realty Brief</title>
</head>
<body style="margin:0;padding:0;background:#0b0f1c;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:620px;margin:0 auto;background:#0b0f1c;padding:0 0 40px 0">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg,#1a2040,#0e1628);padding:32px 32px 24px;border-bottom:2px solid #3b82f6">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
      <span style="font-size:28px">🏙️</span>
      <div>
        <div style="font-size:22px;font-weight:800;color:#e8eaf6;letter-spacing:-0.5px">Maharashtra Estate</div>
        <div style="font-size:11px;color:#60a5fa;text-transform:uppercase;letter-spacing:2px;font-weight:600">State-Wide Intelligence Brief</div>
      </div>
    </div>
    <div style="margin-top:16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
      <div style="font-size:18px;font-weight:700;color:#e8eaf6">📅 {updated}</div>
      {freshness_badge}
    </div>
    <div style="margin-top:8px;font-size:11px;color:#4b5680">Source: {source}</div>
  </div>

  <!-- MARKET PULSE -->
  <div style="padding:24px 32px 0">
    <div style="font-size:14px;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px">⚡ Market Pulse</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">

      <div style="background:#131828;border:1px solid #1e2640;border-radius:10px;padding:16px;border-top:2px solid #14b8a6">
        <div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Repo Rate</div>
        <div style="font-size:20px;font-weight:800;color:#2dd4bf">{summary.get('repo_rate','5.25%')}</div>
        <div style="font-size:11px;color:#4b5680;margin-top:4px">RBI Dec 2025</div>
      </div>

      <div style="background:#131828;border:1px solid #1e2640;border-radius:10px;padding:16px;border-top:2px solid #3b82f6">
        <div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Best Loan Rate</div>
        <div style="font-size:16px;font-weight:800;color:#60a5fa">{summary.get('best_loan_rate','7.20%')}</div>
        <div style="font-size:11px;color:#4b5680;margin-top:4px">HDFC Bank</div>
      </div>

      <div style="background:#131828;border:1px solid #1e2640;border-radius:10px;padding:16px;border-top:2px solid #f59e0b">
        <div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">AI Sentiment</div>
        <div style="font-size:20px;font-weight:800;color:#fbbf24">{summary.get('sentiment_score',7.8)}/10</div>
        <div style="font-size:11px;color:#4b5680;margin-top:4px">{summary.get('sentiment_label','Bullish')}</div>
      </div>

    </div>
  </div>

  <!-- TOP 3 MICRO-MARKETS -->
  <div style="padding:24px 32px 0">
    <div style="font-size:14px;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px">📍 Top 3 Micro-Markets by Appreciation</div>
    <div style="background:#131828;border:1px solid #1e2640;border-radius:10px;overflow:hidden">
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="background:#0e1220">
            <th style="padding:10px 14px;text-align:left;font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;font-weight:600">CITY</th>
            <th style="padding:10px 14px;text-align:left;font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;font-weight:600">LOCALITY</th>
            <th style="padding:10px 14px;text-align:left;font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;font-weight:600">PRICE / SQFT</th>
            <th style="padding:10px 14px;text-align:left;font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;font-weight:600">YOY %</th>
            <th style="padding:10px 14px;text-align:left;font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px;font-weight:600">WHY</th>
          </tr>
        </thead>
        <tbody>{top3_rows}</tbody>
      </table>
    </div>
  </div>

  <!-- HOT PROJECT -->
  <div style="padding:24px 32px 0">
    <div style="font-size:14px;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px">🏗️ Hot Project of the Day</div>
    <div style="background:#131828;border:1px solid #3b82f6;border-radius:10px;padding:20px;border-left:4px solid #3b82f6">
      <div style="font-size:16px;font-weight:700;color:#e8eaf6;margin-bottom:4px">{summary.get('hot_project','Godrej The Gale, Hinjewadi')}</div>
      <div style="font-size:12px;color:#94a3b8;margin-bottom:12px">Hinjewadi Phase 1 · 1–5.5 BHK · From ₹71L · RERA Registered</div>
      <div style="display:inline-block;background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);padding:3px 10px;border-radius:4px;font-size:10px;font-weight:700;text-transform:uppercase">PREMIUM LAUNCH</div>
    </div>
  </div>

  <!-- BROKER TIP -->
  <div style="padding:24px 32px 0">
    <div style="font-size:14px;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px">⚡ Broker Tip of the Day</div>
    <div style="background:linear-gradient(135deg,rgba(20,184,166,0.1),rgba(59,130,246,0.1));border:1px solid rgba(20,184,166,0.25);border-radius:10px;padding:20px">
      <div style="font-size:14px;color:#e8eaf6;line-height:1.7">{summary.get('broker_tip','Scan the RERA QR code on every project brochure before recommending it to clients.')}</div>
    </div>
  </div>

  <!-- KEY NUMBERS -->
  <div style="padding:24px 32px 0">
    <div style="font-size:14px;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px">📊 Key Numbers</div>
    <div style="background:#131828;border:1px solid #1e2640;border-radius:10px;padding:20px">
      <div style="display:flex;flex-wrap:wrap;gap:16px">
        <div style="min-width:120px"><div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px">Projects Tracked</div><div style="font-size:18px;font-weight:700;color:#e8eaf6;margin-top:4px">{summary.get('total_projects_tracked',41)}</div></div>
        <div style="min-width:120px"><div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px">RERA Suspended</div><div style="font-size:18px;font-weight:700;color:#f43f5e;margin-top:4px">{summary.get('rera_suspended','1,905+')}</div></div>
        <div style="min-width:120px"><div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px">Avg Ticket Size</div><div style="font-size:18px;font-weight:700;color:#e8eaf6;margin-top:4px">{summary.get('avg_ticket_size','₹78L')}</div></div>
        <div style="min-width:120px"><div style="font-size:10px;color:#4b5680;text-transform:uppercase;letter-spacing:1px">Top Zone YoY</div><div style="font-size:18px;font-weight:700;color:#22c55e;margin-top:4px">{summary.get('top_zone_appr','14%')}</div></div>
      </div>
    </div>
  </div>

  <!-- CTA -->
  <div style="padding:32px 32px 0;text-align:center">
    <a href="{load_config().get('dashboard_url','http://localhost:5000')}"
       style="display:inline-block;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;text-decoration:none;padding:14px 36px;border-radius:10px;font-size:14px;font-weight:700;letter-spacing:0.5px">
      🌐 Open Full Dashboard
    </a>
    <div style="margin-top:12px;font-size:11px;color:#4b5680">
      http://localhost:5000 · Run <code style="background:#131828;padding:2px 6px;border-radius:4px;color:#60a5fa">start.bat</code> if not already running
    </div>
  </div>

  <!-- FOOTER -->
  <div style="padding:32px 32px 0;text-align:center;border-top:1px solid #1e2640;margin-top:32px">
    <div style="font-size:11px;color:#4b5680">
      Generated by Antigravity AI · Maharashtra Estate Intelligence System<br/>
      This email is sent to {load_config()["recipient_email"]} daily at {load_config().get("send_time", "06:00")} IST
    </div>
  </div>

</div>
</body>
</html>
"""
    return html


def send_email():
    """Send the daily Pune Realty Brief email."""
    config = load_config()
    data   = load_data()

    if not data:
        print("[Notifier] No live_data.json found — run scraper.py first")
        return False

    today   = datetime.now().strftime("%d %B %Y")
    subject = f"🏠 Maharashtra Realty Brief — {today} | Sentiment {data.get('summary',{}).get('sentiment_score',7.8)}/10"

    html_body = build_email_html(data)

    # Build email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = config["gmail_user"]

    # Plain text fallback
    plain = f"""
Maharashtra Realty Brief — {today}

Repo Rate: {data['summary'].get('repo_rate','5.25%')}
Best Loan Rate: {data['summary'].get('best_loan_rate','7.20% HDFC')}
AI Sentiment: {data['summary'].get('sentiment_score',7.8)}/10 — {data['summary'].get('sentiment_label','Bullish')}
Top Zone: {data['summary'].get('top_zone','Mahalunge')} at {data['summary'].get('top_zone_appr','14%')} YoY

Open dashboard: {config.get('dashboard_url','http://localhost:5000')}
"""
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # Determine recipients
    to_emails = [config["recipient_email"]]
    sub_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subscribers.json")
    if os.path.exists(sub_file):
        try:
            with open(sub_file, "r", encoding="utf-8") as f:
                subs = json.load(f)
                for s in subs:
                    if s["email"] not in to_emails:
                        to_emails.append(s["email"])
        except Exception as e:
            print(f"[Notifier] Could not load subscribers: {e}")

    try:
        print(f"[Notifier] Connecting to Gmail SMTP...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(config["gmail_user"], config["gmail_app_password"])
            
            for email in to_emails:
                # Update To field for each recipient
                msg.replace_header("To", email) if "To" in msg else msg.add_header("To", email)
                server.sendmail(config["gmail_user"], email, msg.as_string())
                print(f"[Notifier] ✅ Email sent to {email}")
                
        print(f"[Notifier] Subject: {subject}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[Notifier] ❌ Gmail authentication failed — check App Password in config.json")
        return False
    except Exception as e:
        print(f"[Notifier] ❌ Email error: {e}")
        return False


if __name__ == "__main__":
    result = send_email()
    if result:
        print("\n✅ Email delivered successfully!")
    else:
        print("\n❌ Email failed — check the error above.")
