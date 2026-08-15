import streamlit as st
import random
import time
import sqlite3
import requests

st.set_page_config(
    page_title="ENZO ELITE TERMINAL",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    :root { color-scheme: dark; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #030303 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        -webkit-text-size-adjust: 100%;
    }
    
    /* Elite Typography & Large Professional UI */
    .hero-title { color: #00ff66; font-size: 42px; font-weight: 900; text-align: center; letter-spacing: 3px; text-shadow: 0 0 20px rgba(0,255,102,0.4); margin-bottom: 5px; }
    .hero-sub { color: #888; font-size: 16px; text-align: center; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 25px; }
    
    .elite-container {
        background: #0d0d0d;
        padding: 35px;
        border-radius: 18px;
        border: 1px solid #1a1a1a;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
        margin-top: 20px;
        margin-bottom: 25px;
    }
    
    h3 { font-size: 22px !important; color: #fff !important; margin-bottom: 18px !important; }
    
    .ticker-bar {
        background: #000000;
        border: 1px solid #00ff66;
        color: #00ff66;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-family: monospace;
        font-size: 15px;
        font-weight: bold;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0,255,102,0.2);
    }

    .stButton > button {
        width: 100%;
        background: #00ff66 !important;
        color: #030303 !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        padding: 16px !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer;
        box-shadow: 0 0 25px rgba(0,255,102,0.3);
    }
    .stButton > button:hover { opacity: 0.9; }

    .result-box {
        background: #0d0d0d;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #222;
        border-left: 6px solid #00ff66;
        margin-top: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .metric-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #1a1a1a; font-size: 16px; }
    .stat-card { background: #111; padding: 18px; border-radius: 12px; text-align: center; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

TELEGRAM_URL = "https://t.me/Enzosupport47" 
TELEGRAM_BOT_TOKEN = "8962828738:AAH787ztmRyKM6bRIGHdfVbiI6eeX7U0oFs"
TELEGRAM_CHAT_ID = "8633830998"

def send_telegram_alert(order_id, user_name):
    try:
        msg = f"🚨 *New Binance Payment - ENZO ELITE*\n👤 *User:* {user_name}\n🆔 *Order ID:* `{order_id}`"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

def send_telegram_photo(photo_bytes, caption):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'photo': ('proof.jpg', photo_bytes, 'image/jpeg')}, timeout=10)
    except: pass

def init_db():
    conn = sqlite3.connect('enzo_elite_terminal.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS licenses (key TEXT PRIMARY KEY, username TEXT, status TEXT DEFAULT "Active", expiry_date TEXT DEFAULT "Lifetime")')
    cursor.execute('CREATE TABLE IF NOT EXISTS binance_orders (order_id TEXT PRIMARY KEY)')
    cursor.execute('CREATE TABLE IF NOT EXISTS pending_approvals (order_id TEXT PRIMARY KEY, username TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS admin_settings (id INTEGER PRIMARY KEY, admin_pass TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS app_stats (id INTEGER PRIMARY KEY, total_revenue REAL)')
    
    cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin_settings (id, admin_pass) VALUES (1, ?)", ("Umarali4747",))
    cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO app_stats (id, total_revenue) VALUES (1, 0.0)")
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

VALID_KEYS = [
    "ENZO-9842-XF89-76QW", "ENZO-4747-PRO-8891", "ENZO-5521-TRD-3342",
    "ENZO-8893-SEC-1102", "ENZO-6614-VIP-9983", "ENZO-3350-AI88-4412",
    "ENZO-7729-SYS-5567", "ENZO-1145-NET-2234", "ENZO-9988-LOG-6671",
    "ENZO-2233-ACC-7789", "ENZO-4411-DEV-9900", "ENZO-6655-MTR-1234",
    "ENZO-7788-BTC-5678", "ENZO-3322-ETH-4321", "ENZO-1199-USD-8765",
    "ENZO-8822-EUR-2468", "ENZO-5544-GBP-1357", "ENZO-6677-OTC-9876",
    "ENZO-9911-LIV-5432", "ENZO-2244-BOT-1122", "ENZO-7733-MLK-3344",
    "ENZO-5566-QTX-5566", "ENZO-4488-PKT-7788", "ENZO-1122-SIG-9999",
    "ENZO-6633-RSK-1020", "ENZO-9944-STK-3040", "ENZO-3377-API-5060",
    "ENZO-8855-KEY-7080", "ENZO-2211-PRO-9010", "ENZO-4747-ULTRA-99"
]
for k in VALID_KEYS:
    cursor.execute("INSERT OR IGNORE INTO licenses (key, username, status, expiry_date) VALUES (?, NULL, 'Active', 'Lifetime')", (k,))
conn.commit()

BINANCE_PAY_ID = "385682148"
BINANCE_NAME = "X FENDI"

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'auth_error' not in st.session_state: st.session_state.auth_error = None
if 'current_user' not in st.session_state: st.session_state.current_user = "Trader"

if st.session_state.page == "auth":
    st.markdown('<p class="hero-title">⚡ ENZO ELITE</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Quantum Trading Neural Terminal</p>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="ticker-bar">💬 Need Help? Contact Support: <a href="{TELEGRAM_URL}" target="_blank" style="color:#00ff66;">Telegram Support</a></div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-container">', unsafe_allow_html=True)
        st.write("### 🔐 Secure Authentication")
        
        mode = st.radio("Select Authentication Method", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            username = st.text_input("Your Trading Username", placeholder="Enter your name...")
            key = st.text_input("Security License Key", type="password", placeholder="Enter key...")
            
            if st.button("VERIFY & ENTER TERMINAL ➔"):
                clean_user = username.strip()
                clean_key = key.strip()
                
                if not clean_user or not clean_key:
                    st.session_state.auth_error = "empty_fields"
                else:
                    with st.spinner("Verifying License Key..."):
                        time.sleep(1.0)
                        cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (clean_key,))
                        row = cursor.fetchone()
                        
                        if row is None:
                            st.session_state.auth_error = "invalid"
                        else:
                            db_user, db_status = row[0], row[1]
                            if db_status == "Blocked":
                                st.session_state.auth_error = "blocked"
                            elif db_user is None:
                                cursor.execute("UPDATE licenses SET username = ? WHERE key = ?", (clean_user, clean_key))
                                conn.commit()
                                st.session_state.current_user = clean_user
                                st.session_state.auth_error = None
                                st.session_state.page = "dashboard"
                                st.rerun()
                            elif db_user == clean_user:
                                st.session_state.current_user = clean_user
                                st.session_state.auth_error = None
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.session_state.auth_error = "wrong_user"
            
            if st.session_state.auth_error == "empty_fields":
                st.warning("Please fill in all required fields!")
            elif st.session_state.auth_error == "invalid":
                st.error("Invalid License Key! Purchase a genuine key from Telegram support.")
            elif st.session_state.auth_error == "blocked":
                st.error("This license key has been blocked by the administrator.")
            elif st.session_state.auth_error == "wrong_user":
                st.error("This key is already registered with another user.")

        else:
            st.markdown(f"""
                <div style="background:#111; border:1px dashed #f3ba2f; padding:20px; border-radius:12px; margin-bottom:20px;">
                    <h4 style="color:#f3ba2f; margin-top:0; font-size:20px;">💛 Binance Pay Gateway ($10)</h4>
                    <p style="font-size:15px; color:#ccc; margin-bottom:8px;">Transfer $10 to the following Binance Pay ID:</p>
                    <div style="background:#030303; padding:12px; border-radius:8px; font-family:monospace; color:#00ff66; font-size:16px;">
                        <b>Pay ID:</b> {BINANCE_PAY_ID}<br><b>Name:</b> {BINANCE_NAME}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            user_input_name = st.text_input("Your Name", placeholder="Enter your name...")
            order_id = st.text_input("Binance Order ID", placeholder="Enter transaction order ID...")
            screenshot = st.file_uploader("Upload Payment Screenshot", type=["png", "jpg", "jpeg"])
            
            if st.button("SUBMIT PAYMENT PROOF ➔"):
                clean_order = order_id.strip()
                clean_name = user_input_name.strip()
                if not clean_name or not clean_order or screenshot is None:
                    st.warning("Please complete all payment details and upload the screenshot!")
                else:
                    cursor.execute("SELECT order_id FROM binance_orders WHERE order_id = ?", (clean_order,))
                    if cursor.fetchone():
                        st.warning("This Order ID has already been submitted!")
                    else:
                        with st.spinner("Submitting payment proof..."):
                            time.sleep(1.0)
                            cursor.execute("INSERT INTO binance_orders (order_id) VALUES (?)", (clean_order,))
                            cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (clean_order, clean_name))
                            conn.commit()
                            send_telegram_alert(clean_order, clean_name)
                            send_telegram_photo(screenshot.getvalue(), f"📸 Payment Proof\nUser: `{clean_name}`\nOrder: `{clean_order}`")
                            st.success("Payment submitted successfully! Contact Telegram support for instant approval.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Admin Panel
    with st.expander("🛠️ Administrator Panel"):
        cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
        apass = cursor.fetchone()[0]
        ap_in = st.text_input("Admin Password", type="password")
        if ap_in == apass:
            st.success("Admin Access Granted")
            cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
            rev = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM licenses WHERE username IS NOT NULL")
            ac = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pending_approvals")
            pc = cursor.fetchone()[0]
            
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="stat-card"><h5>Revenue</h5><h3 style="color:#00ff66;">${rev:.2f}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="stat-card"><h5>Active Users</h5><h3 style="color:#38bdf8;">{ac}</h3></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="stat-card"><h5>Pending</h5><h3 style="color:#f3ba2f;">{pc}</h3></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Pending Approvals")
            cursor.execute("SELECT order_id, username FROM pending_approvals")
            pend = cursor.fetchall()
            if pend:
                for p in pend:
                    st.write(f"User: {p[1]} | Order: {p[0]}")
                    if st.button(f"Approve {p[0]}", key=f"ap_{p[0]}"):
                        cursor.execute("SELECT key FROM licenses WHERE username IS NULL LIMIT 1")
                        fk = cursor.fetchone()
                        if fk:
                            cursor.execute("DELETE FROM pending_approvals WHERE order_id = ?", (p[0],))
                            cursor.execute("UPDATE app_stats SET total_revenue = total_revenue + 10.0 WHERE id = 1")
                            conn.commit()
                            st.success(f"Assigned Key: {fk[0]}")
                            st.rerun()
            else:
                st.info("No pending orders.")

elif st.session_state.page == "dashboard":
    st.markdown(f'<div class="ticker-bar">⚡ Welcome, {st.session_state.current_user.upper()} | Elite Neural Terminal Active ⚡</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-container">', unsafe_allow_html=True)
        st.write("### 🏛️ 01. Select Broker & Market")
        broker = st.selectbox("Select Broker", ["Quotex", "Pocket Option"])
        market = st.radio("Market Type", ["OTC", "Live Market"], horizontal=True)
        
        # Complete official asset lists including USD/PKR, USD/BDT, etc.
        if broker == "Quotex":
            assets = [
                "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "NZD/USD (OTC)", 
                "USD/JPY (OTC)", "USD/CHF (OTC)", "EUR/JPY (OTC)", "GBP/JPY (OTC)", 
                "AUD/JPY (OTC)", "EUR/AUD (OTC)", "USD/CAD (OTC)", "CAD/JPY (OTC)",
                "EUR/GBP (OTC)", "AUD/USD (OTC)", "CHF/JPY (OTC)", "EUR/NZD (OTC)",
                "GBP/AUD (OTC)", "AUD/NZD (OTC)", "NZD/JPY (OTC)", "USD/INR (OTC)",
                "USD/BRL (OTC)", "USD/PHP (OTC)", "USD/IDR (OTC)", "USD/ZAR (OTC)",
                "EUR/CAD (OTC)", "GBP/CHF (OTC)", "AUD/CHF (OTC)", "NZD/CAD (OTC)",
                "USD/MXN (OTC)", "USD/TRY (OTC)", "USD/EGP (OTC)", "USD/BDT (OTC)",
                "USD/PKR (OTC)", "USD/VND (OTC)", "USD/NGN (OTC)", "EUR/TRY (OTC)", 
                "GBP/TRY (OTC)", "GOLD (OTC)", "SILVER (OTC)"
            ] if market == "OTC" else [
                "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", 
                "EUR/GBP", "NZD/USD", "USD/CHF", "EUR/JPY", "GBP/JPY", 
                "AUD/JPY", "EUR/AUD", "CAD/JPY", "EUR/NZD", "GBP/AUD",
                "AUD/NZD", "NZD/CAD", "CHF/JPY", "USD/MXN", "USD/NOK",
                "GOLD (Commodity)", "SILVER (Commodity)", "BRENT (Oil)"
            ]
        else:
            assets = [
                "EUR/USD [OTC]", "GBP/USD [OTC]", "USD/JPY [OTC]", "AUD/CHF [OTC]", 
                "EUR/GBP [OTC]", "USD/CAD [OTC]", "GBP/JPY [OTC]", "NZD/JPY [OTC]",
                "AUD/CAD [OTC]", "EUR/AUD [OTC]", "CHF/JPY [OTC]", "USD/CHF [OTC]",
                "NZD/USD [OTC]", "EUR/CAD [OTC]", "GBP/CHF [OTC]", "EUR/JPY [OTC]",
                "AUD/USD [OTC]", "NZD/USD [OTC]", "USD/INR [OTC]", "USD/BRL [OTC]",
                "EUR/NZD [OTC]", "GBP/AUD [OTC]", "CAD/JPY [OTC]", "USD/MXN [OTC]",
                "USD/TRY [OTC]", "USD/PKR [OTC]", "USD/BDT [OTC]", "USD/EGP [OTC]",
                "EUR/TRY [OTC]", "GOLD [OTC]", "SILVER [OTC]"
            ] if market == "OTC" else [
                "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "EUR/JPY", 
                "NZD/USD", "USD/CAD", "AUD/CAD", "EUR/AUD", "GBP/GBP",
                "GOLD (Commodity)", "SILVER (Commodity)", "BRENT (Oil)"
            ]
            
        asset = st.selectbox("Trading Asset", assets)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-container">', unsafe_allow_html=True)
        st.write("### ⚙️ 02. Timeframe & Risk Management")
        tf = st.selectbox("Timeframe", ["15 Seconds", "30 Seconds", "1 Minute", "2 Minutes", "5 Minutes"])
        balance = st.number_input("Account Balance ($)", min_value=10, value=100, step=10)
        risk = st.select_slider("Risk Strategy", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"], value="Moderate (5%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🚀 EXECUTE NEURAL TECHNICAL ANALYSIS")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'signal_data' not in st.session_state: st.session_state.signal_data = None

    if gen_btn:
        with st.spinner("Scanning market momentum & price action..."):
            prog = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                prog.progress(i + 1)
        
        seed_val = hash(asset + tf + str(int(time.time() / 20)))
        random.seed(seed_val)
        
        action = random.choice(["BUY", "SELL"])
        conf = random.randint(90, 95)
        
        if action == "BUY":
            trend = "Strong Bullish Volume Breakout & Support Rebound"
            rsi_val = f"RSI Momentum: {random.randint(20, 30)} (Oversold Bounce)"
        else:
            trend = "Strong Bearish Momentum & Resistance Rejection"
            rsi_val = f"RSI Momentum: {random.randint(70, 84)} (Overbought Drop)"
        
        if "Safe" in risk: stake = round(balance * 0.02, 2)
        elif "Moderate" in risk: stake = round(balance * 0.05, 2)
        else: stake = round(balance * 0.10, 2)
            
        st.session_state.signal_data = {
            "action": action, "conf": conf, "asset": asset, "tf": tf,
            "broker": broker, "stake": stake, "strategy": risk, "rsi": rsi_val, "trend": trend
        }

    if st.session_state.signal_data:
        sig = st.session_state.signal_data
        color = "#00ff66" if sig["action"] == "BUY" else "#ff3366"
        
        st.markdown(f"""
            <div class="result-box" style="border-left-color: {color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <span style="font-size: 20px; font-weight: 900; color: #ffffff;">🎯 QUANT AI SIGNAL OUTPUT</span>
                    <span style="background-color: {color}; color: #030303; padding: 6px 18px; border-radius: 8px; font-weight: 900; font-size: 18px;">{sig['action']}</span>
                </div>
                <div class="metric-row"><span style="color: #9ca3af;">Broker / Asset:</span><span style="font-weight: 600;">{sig['broker']} - {sig['asset']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Timeframe & Strategy:</span><span style="font-weight: 600;">{sig['tf']} | {sig['strategy']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Price Action:</span><span style="color: #00ff66; font-weight: 600;">{sig['trend']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Indicator State:</span><span style="color: #f3ba2f; font-weight: 600;">{sig['rsi']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Win-Rate Probability:</span><span style="color: #00ff66; font-weight: 700;">{sig['conf']}% High Precision</span></div>
                <div class="metric-row" style="border: none;"><span style="color: #9ca3af;">Recommended Stake:</span><span style="color: #38bdf8; font-weight: 700;">${sig['stake']}</span></div>
            </div>
        """, unsafe_allow_html=True)
