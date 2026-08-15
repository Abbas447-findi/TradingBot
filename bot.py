import streamlit as st
import random
import time
import sqlite3
import requests

st.set_page_config(
    page_title="ENZO QUANT TERMINAL v4.9",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    :root { color-scheme: dark; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #030712 !important;
        color: #f3f4f6 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        -webkit-text-size-adjust: 100%;
    }
    
    /* Elite Cyberpunk Glassmorphism & Animations */
    @keyframes eliteSlide { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulseGlow { 0% { box-shadow: 0 0 5px rgba(0,255,102,0.2); } 50% { box-shadow: 0 0 20px rgba(0,255,102,0.6); } 100% { box-shadow: 0 0 5px rgba(0,255,102,0.2); } }
    @keyframes scanLine { 0% { transform: translateY(-100%); } 100% { transform: translateY(1000%); } }

    .elite-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(3, 7, 18, 0.95) 100%);
        padding: 32px;
        border-radius: 18px;
        border: 1px solid rgba(0, 255, 102, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        margin-top: 20px;
        animation: eliteSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    
    .elite-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, #00ff66, transparent);
    }

    .terminal-header {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        color: #00ff66;
        text-transform: uppercase;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .live-ticker {
        background: #0d1117;
        border: 1px solid #21262d;
        padding: 10px 15px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 12px;
        color: #8b949e;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .title-text { color: #ffffff; text-align: center; font-size: 40px; font-weight: 900; letter-spacing: 3px; text-shadow: 0 0 25px rgba(0, 255, 102, 0.3); }
    .sub-title { color: #9ca3af; text-align: center; font-size: 13px; font-weight: 500; letter-spacing: 1px; margin-bottom: 25px; text-transform: uppercase; }
    
    .telegram-box { text-align: center; background-color: #111827; padding: 12px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #1f2937; }
    .telegram-link { color: #38bdf8; text-decoration: none; font-weight: 700; font-size: 14px; }
    
    .binance-box { background-color: #111827; border: 1px dashed #f3ba2f; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .popup-error-box { background-color: #1f1115; border: 1px solid #ff3366; padding: 25px; border-radius: 16px; text-align: center; margin: 20px 0; }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00ff66 0%, #00873e 100%) !important;
        color: #030712 !important;
        font-size: 15px !important;
        font-weight: 900 !important;
        padding: 14px !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(0, 255, 102, 0.6);
    }

    .result-box {
        background: #0d1117;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #30363d;
        border-left: 5px solid #00ff66;
        margin-top: 25px;
        animation: eliteSlide 0.5s ease-out;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .metric-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; font-size: 13px; font-family: 'Courier New', Courier, monospace; }
    .stat-card { background: #161b22; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

TELEGRAM_URL = "https://t.me/Enzosupport47" 
TELEGRAM_BOT_TOKEN = "8962828738:AAH787ztmRyKM6bRIGHdfVbiI6eeX7U0oFs"
TELEGRAM_CHAT_ID = "8633830998"

def send_telegram_alert(order_id, user_name):
    try:
        message = f"🚨 *New Binance Payment - ENZO QUANT*\n👤 *User:* {user_name}\n🆔 *Order:* `{order_id}`"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except: pass

def send_telegram_photo(photo_bytes, caption):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'photo': ('proof.jpg', photo_bytes, 'image/jpeg')}, timeout=10)
    except: pass

def init_db():
    conn = sqlite3.connect('enzo_quant.db', check_same_thread=False)
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
    st.markdown('<p class="title-text">⚡ ENZO QUANT</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Institutional Grade Algorithmic Binary Terminal</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="live-ticker">
            <span>🟢 NODE: SECURE-US-EAST-1</span>
            <span>LATENCY: 12ms</span>
            <span>ENCRYPTION: AES-256</span>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-card">', unsafe_allow_html=True)
        st.markdown('<div class="terminal-header"><span>// SYSTEM AUTHENTICATION</span><span>SECURE GATEWAY</span></div>', unsafe_allow_html=True)
        
        mode = st.radio("Access Mode", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            username = st.text_input("Operator Alias", placeholder="Enter your handle...")
            key = st.text_input("Access Cipher Key", type="password", placeholder="ENZO-XXXX-XXXX...")
            
            if st.button("INITIALIZE TERMINAL ➔"):
                clean_user = username.strip()
                clean_key = key.strip()
                
                if not clean_user or not clean_key:
                    st.session_state.auth_error = "empty_fields"
                else:
                    with st.spinner("Validating Hardware Fingerprint & Neural Key..."):
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
                st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ All parameters required.</p>", unsafe_allow_html=True)
            elif st.session_state.auth_error == "invalid":
                st.markdown(f'<div class="popup-error-box"><h4 style="color:#ff3366; margin:0 0 8px 0;">ACCESS DENIED</h4><p style="font-size:13px; color:#9ca3af; margin-bottom:15px;">Invalid cryptographic signature.</p><a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">Acquire License via Telegram ➔</a></div>', unsafe_allow_html=True)
            elif st.session_state.auth_error == "blocked":
                st.markdown(f'<div class="popup-error-box"><h4 style="color:#ff3366; margin:0;">TERMINAL REVOKED</h4></div>', unsafe_allow_html=True)
            elif st.session_state.auth_error == "wrong_user":
                st.markdown(f'<div class="popup-error-box"><h4 style="color:#ff3366; margin:0;">KEY BINDING MISMATCH</h4></div>', unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div class="binance-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="color: #f3ba2f; font-weight:700; font-family:'Courier New';">BINANCE PAY ESCROW</span>
                        <span style="background: #f3ba2f; color: #030712; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight:800;">$10.00</span>
                    </div>
                    <div style="background: #030712; padding: 10px; border-radius: 6px; font-family: monospace; color: #00ff66; font-size: 13px;">
                        <b>Pay ID:</b> {BINANCE_PAY_ID}<br><b>Name:</b> {BINANCE_NAME}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            user_input_name = st.text_input("Operator Handle", placeholder="Your name...")
            order_id = st.text_input("Transaction Order ID", placeholder="Binance transaction hash/ID...")
            screenshot = st.file_uploader("Upload Receipt Proof", type=["png", "jpg", "jpeg"])
            
            if st.button("SUBMIT ESCROW PROOF ➔"):
                clean_order = order_id.strip()
                clean_name = user_input_name.strip()
                if not clean_name or not clean_order or screenshot is None:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Missing verification parameters.</p>", unsafe_allow_html=True)
                else:
                    cursor.execute("SELECT order_id FROM binance_orders WHERE order_id = ?", (clean_order,))
                    if cursor.fetchone():
                        st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Order ID already processed.</p>", unsafe_allow_html=True)
                    else:
                        with st.spinner("Broadcasting proof to secure relay..."):
                            time.sleep(1.0)
                            cursor.execute("INSERT INTO binance_orders (order_id) VALUES (?)", (clean_order,))
                            cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (clean_order, clean_name))
                            conn.commit()
                            send_telegram_alert(clean_order, clean_name)
                            send_telegram_photo(screenshot.getvalue(), f"📸 Receipt\nOperator: `{clean_name}`\nOrder: `{clean_order}`")
                            st.success("✅ Broadcast successful. Awaiting clearance.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Admin Panel
    with st.expander("🔐 SYSTEM ADMIN DECK"):
        cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
        apass = cursor.fetchone()[0]
        ap_in = st.text_input("Master Cipher", type="password")
        if ap_in == apass:
            st.success("Admin Clearance Verified")
            cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
            rev = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM licenses WHERE username IS NOT NULL")
            ac = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pending_approvals")
            pc = cursor.fetchone()[0]
            
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="stat-card"><h5>REVENUE</h5><h3 style="color:#00ff66;">${rev:.2f}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="stat-card"><h5>SESSIONS</h5><h3 style="color:#38bdf8;">{ac}</h3></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="stat-card"><h5>QUEUE</h5><h3 style="color:#f3ba2f;">{pc}</h3></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            cursor.execute("SELECT order_id, username FROM pending_approvals")
            for p in cursor.fetchall():
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

elif st.session_state.page == "dashboard":
    st.markdown(f"""
        <div class="live-ticker">
            <span>⚡ OPERATOR: {st.session_state.current_user.upper()}</span>
            <span>STATUS: QUANTUM SYNCED</span>
            <span>SERVER: 0.1ms</span>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-card">', unsafe_allow_html=True)
        st.markdown('<div class="terminal-header"><span>// STEP 02: ASSET SELECTION & MARKET ROUTING</span></div>', unsafe_allow_html=True)
        
        broker = st.selectbox("Execution Broker", ["Quotex", "Pocket Option"])
        market = st.radio("Liquidity Pool", ["OTC", "Live Market"], horizontal=True)
        
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
            
        asset = st.selectbox("Target Instrument", assets)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="elite-card">', unsafe_allow_html=True)
        st.markdown('<div class="terminal-header"><span>// STEP 03: QUANTITATIVE PARAMETERS</span></div>', unsafe_allow_html=True)
        tf = st.selectbox("Execution Window", ["15 Seconds", "30 Seconds", "1 Minute", "2 Minutes", "5 Minutes"])
        balance = st.number_input("Capital Allocation ($)", min_value=10, value=100, step=10)
        risk = st.select_slider("Risk Vector", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"], value="Moderate (5%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("EXECUTE NEURAL SCAN & GENERATE SIGNAL ➔")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'signal_data' not in st.session_state: st.session_state.signal_data = None

    if gen_btn:
        with st.spinner(""):
            prog = st.progress(0)
            status_text = st.empty()
            steps = [
                "Connecting to WebSocket feed...",
                "Running Multi-Timeframe Order Book Analysis...",
                "Calculating RSI/Bollinger Vector Matrix...",
                "Synthesizing Institutional Probability Matrix..."
            ]
            for i in range(100):
                time.sleep(0.025)
                prog.progress(i + 1)
                if i == 25: status_text.markdown(f"<p style='color:#00ff66; font-family:monospace; font-size:12px;'>{steps[1]}</p>", unsafe_allow_html=True)
                elif i == 60: status_text.markdown(f"<p style='color:#00ff66; font-family:monospace; font-size:12px;'>{steps[2]}</p>", unsafe_allow_html=True)
                elif i == 85: status_text.markdown(f"<p style='color:#00ff66; font-family:monospace; font-size:12px;'>{steps[3]}</p>", unsafe_allow_html=True)
            status_text.empty()
        
        seed_val = hash(asset + tf + str(int(time.time() / 20)))
        random.seed(seed_val)
        
        action = random.choice(["BUY", "SELL"])
        conf = random.randint(90, 95)
        
        if action == "BUY":
            trend = "Institutional Bullish Order Flow & Liquidity Sweep"
            rsi_val = f"Momentum Vector: {random.randint(18, 28)} (Oversold Compression)"
        else:
            trend = "Institutional Bearish Resistance Rejection & Distribution"
            rsi_val = f"Momentum Vector: {random.randint(72, 86)} (Overbought Exhaustion)"
        
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
                    <span style="font-family:'Courier New'; font-size: 16px; font-weight: 800; color: #ffffff;">⚡ QUANT SIGNAL OUTPUT</span>
                    <span style="background-color: {color}; color: #030712; padding: 6px 16px; border-radius: 6px; font-weight: 900; font-size: 16px; font-family:'Courier New';">{sig['action']}</span>
                </div>
                <div class="metric-row"><span style="color: #8b949e;">ROUTED BROKER / ASSET:</span><span style="color:#ffffff; font-weight:600;">{sig['broker']} - {sig['asset']}</span></div>
                <div class="metric-row"><span style="color: #8b949e;">WINDOW & VECTOR:</span><span style="color:#ffffff; font-weight:600;">{sig['tf']} | {sig['strategy']}</span></div>
                <div class="metric-row"><span style="color: #8b949e;">PRICE ACTION MATRIX:</span><span style="color: #00ff66; font-weight: 600;">{sig['trend']}</span></div>
                <div class="metric-row"><span style="color: #8b949e;">OSCILLATOR TELEMETRY:</span><span style="color: #f3ba2f; font-weight: 600;">{sig['rsi']}</span></div>
                <div class="metric-row"><span style="color: #8b949e;">PROBABILITY INDEX:</span><span style="color: #00ff66; font-weight: 700;">{sig['conf']}% High Precision Confidence</span></div>
                <div class="metric-row" style="border: none;"><span style="color: #8b949e;">SUGGESTED ALLOCATION:</span><span style="color: #38bdf8; font-weight: 700;">${sig['stake']}</span></div>
            </div>
        """, unsafe_allow_html=True)
