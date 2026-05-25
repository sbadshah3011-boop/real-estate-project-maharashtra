import os

def update_pricing():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the sidebar CTA button
    btn_search = '<button class="saas-cta-btn email-btn" onclick="openCheckout()">Subscribe — ₹999/mo</button>'
    btn_replace = '<button class="saas-cta-btn email-btn" onclick="openCheckout()">Subscribe Now</button>'
    html = html.replace(btn_search, btn_replace)

    # 2. Update the checkout modal plan summary to have two clickable cards
    plan_search = """      <div class="plan-summary">
        <div>
          <div class="plan-name">Maharashtra Realty Brief</div>
          <div class="plan-desc">Daily Intelligence at 6:00 AM</div>
        </div>
        <div class="plan-price">₹999<span style="font-size:12px;color:#94a3b8;font-weight:400">/mo</span></div>
      </div>"""
    
    plan_replace = """      <div class="plan-summary" style="display:flex; flex-direction:column; gap:14px; align-items:stretch;">
        <div>
          <div class="plan-name" style="font-size:16px;">Maharashtra Realty Brief</div>
          <div class="plan-desc">Daily Intelligence at 6:00 AM</div>
        </div>
        <div style="display:flex; gap:10px;">
          <div class="plan-tab active" style="flex:1; text-align:center; padding:12px; background:transparent; border:1px solid #334155; border-radius:6px; cursor:pointer;" onclick="selectPlan(99, this)">
             <div style="font-size:18px; font-weight:800; color:#f8fafc;">₹99</div>
             <div style="font-size:11px; color:#94a3b8; margin-top:2px;">per month</div>
          </div>
          <div class="plan-tab" style="flex:1; text-align:center; padding:12px; border:1px solid #334155; border-radius:6px; cursor:pointer; position:relative;" onclick="selectPlan(999, this)">
             <div style="position:absolute; top:-10px; right:-5px; background:#fbbf24; color:#000; font-size:9px; font-weight:800; padding:2px 6px; border-radius:10px;">SAVE 15%</div>
             <div style="font-size:18px; font-weight:800; color:#f8fafc;">₹999</div>
             <div style="font-size:11px; color:#94a3b8; margin-top:2px;">for 12 months</div>
          </div>
        </div>
      </div>"""
    html = html.replace(plan_search, plan_replace)

    # 3. Update the Pay button
    pay_btn_search = '<button class="btn-pay" id="btn-pay" onclick="processPayment()">Pay ₹999 & Subscribe</button>'
    pay_btn_replace = '<button class="btn-pay" id="btn-pay" onclick="processPayment()">Pay ₹99 & Subscribe</button>'
    html = html.replace(pay_btn_search, pay_btn_replace)

    # 4. Add the selectPlan Javascript function
    js_search = 'function switchPayTab(id, el) {'
    js_replace = """let currentPlan = 99;
function selectPlan(price, el) {
  document.querySelectorAll('.plan-tab').forEach(t=>{
    t.style.background = 'transparent';
    t.style.borderColor = '#334155';
  });
  el.style.background = 'rgba(59,130,246,0.1)';
  el.style.borderColor = '#3b82f6';
  currentPlan = price;
  document.getElementById('btn-pay').innerText = `Pay ₹${price} & Subscribe`;
}

function switchPayTab(id, el) {"""
    
    if "function selectPlan" not in html:
        html = html.replace(js_search, js_replace)

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated pricing display in dashboard.html")

if __name__ == "__main__":
    update_pricing()
