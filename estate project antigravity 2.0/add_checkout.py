import os

def update_dashboard():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CSS
    css_injection = """
    /* ── CHECKOUT MODAL ── */
    .modal-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; align-items:center; justify-content:center; backdrop-filter:blur(5px); }
    .modal { background:#0f172a; width:450px; max-width:90%; border-radius:16px; border:1px solid #1e293b; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 25px 50px -12px rgba(0,0,0,0.5); font-family:'Inter',sans-serif; }
    .modal-header { background:linear-gradient(135deg,#1e293b,#0f172a); padding:20px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; }
    .modal-title { font-size:16px; font-weight:700; color:#f8fafc; }
    .modal-close { cursor:pointer; font-size:20px; color:#94a3b8; line-height:1; }
    .modal-body { padding:24px; }
    
    .plan-summary { background:#1e293b; padding:16px; border-radius:8px; margin-bottom:20px; border:1px solid #334155; display:flex; justify-content:space-between; align-items:center;}
    .plan-name { font-size:14px; font-weight:600; color:#e2e8f0; margin-bottom:4px;}
    .plan-desc { font-size:12px; color:#94a3b8; }
    .plan-price { font-size:18px; font-weight:800; color:#22c55e; }
    
    .form-group { margin-bottom:16px; }
    .form-group label { display:block; font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:6px; }
    .form-group input { width:100%; box-sizing:border-box; background:#1e293b; border:1px solid #334155; color:#f8fafc; padding:10px 14px; border-radius:6px; font-size:14px; outline:none; transition:border 0.2s;}
    .form-group input:focus { border-color:#3b82f6; }
    
    .pay-tabs { display:flex; gap:8px; margin-bottom:16px; border-bottom:1px solid #1e293b; padding-bottom:12px;}
    .pay-tab { padding:8px 12px; background:transparent; border:1px solid #334155; border-radius:6px; color:#94a3b8; font-size:12px; cursor:pointer; font-weight:600;}
    .pay-tab.active { background:rgba(59,130,246,0.1); border-color:#3b82f6; color:#3b82f6;}
    
    .pay-content { display:none; }
    .pay-content.active { display:block; }
    .qr-box { text-align:center; padding:20px; background:#1e293b; border-radius:8px; border:1px dashed #334155;}
    
    .btn-pay { width:100%; padding:14px; background:#3b82f6; color:#fff; font-size:14px; font-weight:700; border:none; border-radius:8px; cursor:pointer; margin-top:10px; transition:all 0.2s; }
    .btn-pay:hover { background:#2563eb; }
    .btn-pay.loading { background:#475569; pointer-events:none; }
    
    /* ── BASE CSS ── */
"""
    if "/* ── CHECKOUT MODAL ── */" not in html:
        html = html.replace("/* ── BASE CSS ── */", css_injection)

    # 2. HTML
    html_injection = """
<!-- ══ CHECKOUT MODAL ══ -->
<div class="modal-overlay" id="checkout-modal">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-title">Secure Checkout</div>
      <div class="modal-close" onclick="closeCheckout()">×</div>
    </div>
    <div class="modal-body">
      <div class="plan-summary">
        <div>
          <div class="plan-name">Maharashtra Realty Brief</div>
          <div class="plan-desc">Daily Intelligence at 6:00 AM</div>
        </div>
        <div class="plan-price">₹999<span style="font-size:12px;color:#94a3b8;font-weight:400">/mo</span></div>
      </div>
      
      <div class="form-group">
        <label>Full Name</label>
        <input type="text" id="sub-name" placeholder="Rahul Desai" required>
      </div>
      <div class="form-group">
        <label>Email Address</label>
        <input type="email" id="sub-email" placeholder="rahul@example.com" required>
      </div>
      
      <div class="form-group" style="margin-top:24px;">
        <label>Payment Method</label>
        <div class="pay-tabs">
          <div class="pay-tab active" onclick="switchPayTab('upi', this)">UPI / QR</div>
          <div class="pay-tab" onclick="switchPayTab('card', this)">Card</div>
          <div class="pay-tab" onclick="switchPayTab('net', this)">Net Banking</div>
        </div>
        
        <div id="pay-upi" class="pay-content active">
          <div class="qr-box">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=upi://pay?pa=test@razorpay&pn=MahaEstate" alt="QR" style="background:#fff;padding:5px;border-radius:4px;margin-bottom:10px;">
            <div style="font-size:11px;color:#94a3b8;">Scan with GPay, PhonePe, Paytm</div>
          </div>
        </div>
        <div id="pay-card" class="pay-content">
          <input type="text" placeholder="Card Number" style="width:100%;padding:10px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:6px;margin-bottom:8px;box-sizing:border-box;">
          <div style="display:flex;gap:8px;">
            <input type="text" placeholder="MM/YY" style="width:50%;padding:10px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:6px;box-sizing:border-box;">
            <input type="text" placeholder="CVV" style="width:50%;padding:10px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:6px;box-sizing:border-box;">
          </div>
        </div>
        <div id="pay-net" class="pay-content">
           <select style="width:100%;padding:10px;background:#1e293b;border:1px solid #334155;color:#fff;border-radius:6px;outline:none;">
             <option>HDFC Bank</option>
             <option>State Bank of India</option>
             <option>ICICI Bank</option>
             <option>Axis Bank</option>
           </select>
        </div>
      </div>
      
      <button class="btn-pay" id="btn-pay" onclick="processPayment()">Pay ₹999 & Subscribe</button>
      <div style="text-align:center;margin-top:12px;font-size:10px;color:#64748b;display:flex;align-items:center;justify-content:center;gap:4px;">
        <span>🔒</span> Secured by Razorpay Simulation
      </div>
    </div>
  </div>
</div>

<div class="dashboard-wrap">
"""
    if "checkout-modal" not in html:
        html = html.replace('<div class="dashboard-wrap">', html_injection)

    # 3. Modify button to open checkout
    old_btn = '''<button class="saas-cta-btn email-btn" onclick="alert('Subscription integration coming soon!')">Subscribe — ₹999/mo</button>'''
    new_btn = '''<button class="saas-cta-btn email-btn" onclick="openCheckout()">Subscribe — ₹999/mo</button>'''
    html = html.replace(old_btn, new_btn)

    # 4. JavaScript
    js_injection = """
// ── CHECKOUT LOGIC ──
function openCheckout() {
  document.getElementById('checkout-modal').style.display = 'flex';
}
function closeCheckout() {
  document.getElementById('checkout-modal').style.display = 'none';
}
function switchPayTab(id, el) {
  document.querySelectorAll('.pay-tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.pay-content').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('pay-'+id).classList.add('active');
}

async function processPayment() {
  const name = document.getElementById('sub-name').value;
  const email = document.getElementById('sub-email').value;
  if(!name || !email || !email.includes('@')) {
    alert("Please enter a valid name and email.");
    return;
  }
  
  const btn = document.getElementById('btn-pay');
  btn.classList.add('loading');
  btn.innerText = "Processing Payment...";
  
  // Simulate payment gateway delay
  setTimeout(async () => {
    btn.innerText = "Verifying...";
    
    // Call backend API
    try {
      const res = await fetch(`${API}/subscribe`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, email})
      });
      const data = await res.json();
      if(data.status === 'ok') {
        btn.style.background = '#22c55e';
        btn.innerText = "Payment Successful! ✓";
        setTimeout(() => {
          closeCheckout();
          btn.style.background = '#3b82f6';
          btn.innerText = "Pay ₹999 & Subscribe";
          btn.classList.remove('loading');
          alert(`Welcome aboard, ${name}! You will now receive the daily email at ${email}.`);
        }, 1500);
      } else {
        throw new Error("Backend error");
      }
    } catch(e) {
      btn.innerText = "Error! Try Again.";
      btn.style.background = '#ef4444';
      setTimeout(() => {
        btn.style.background = '#3b82f6';
        btn.innerText = "Pay ₹999 & Subscribe";
        btn.classList.remove('loading');
      }, 2000);
    }
  }, 2000);
}

// ── RENDER MARKETS ──
"""
    if "function openCheckout()" not in html:
        html = html.replace("// ── RENDER MARKETS ──", js_injection)

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added Checkout Modal to Dashboard.")

if __name__ == "__main__":
    update_dashboard()
