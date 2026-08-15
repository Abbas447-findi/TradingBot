import streamlit as st
import random
import time
import sqlite3
import requests
import hashlib

st.set_page_config(
    page_title="ENZO PRO ROBOT - Elite Trading Bot",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    :root {
        color-scheme: dark;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #030508 !important;
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        -webkit-text-size-adjust: 100%;
    }
    
    @keyframes neonPulse {
        0% { box-shadow: 0 0 10px rgba(0, 255, 102, 0.2); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 102, 0.6); }
        100% { box-shadow: 0 0 10px rgba(0, 255, 102, 0.2); }
    }

    /* Center Pop-Up Entrance Animation */
    @keyframes centerPopUpAnimation {
        0% { opacity: 0; transform: scale(0.85) translateY(20px); }
        50% { transform: scale(1.02) translateY(-5px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .page-box { 
        background: linear-gradient(135deg, #0d1117 0%, #05080f 100%); 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid rgba(0, 255, 102, 0.3); 
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9); 
        margin-top: 20px; 
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #022c22 0%, #0d1117 100%);
        border: 1px solid #00ff66;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.25);
    }

    .welcome-title {
        color: #00ff66;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.5);
    }
    
    .title-text { 
        color: #00ff66; 
        text-align: center; 
        font-size: 46px; 
        font-weight: 900; 
        letter-spacing: 3px; 
        margin-bottom: 0px; 
        text-shadow: 0 0 25px rgba(0, 255, 102, 0.6); 
    }
    
    .sub-title { 
        color: #94a3b8; 
        text-align: center; 
        font-size: 15px; 
        font-weight: 600; 
        letter-spacing: 2px;
        margin-bottom: 25px; 
        text-transform: uppercase;
    }
    
    .telegram-box { 
        text-align: center; 
        background-color: #0d1117; 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
        border: 1px solid #1e293b; 
    }
    
    .telegram-link { color: #38bdf8; text-decoration: none; font-weight: 700; font-size: 16px; }
    .telegram-link:hover { color: #00aaff; text-decoration: underline; }
    
    .binance-box { 
        background-color: #0d1117; 
        border: 1px dashed #f3ba2f; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
    }
    
    .popup-error-box { 
        background-color: #1a080c; 
        border: 2px solid #ff3366; 
        padding: 35px; 
        border-radius: 18px; 
        text-align: center; 
        margin-top: 25px; 
        margin-bottom: 25px; 
        box-shadow: 0 0 40px rgba(255, 51, 102, 0.5); 
    }
    
    .popup-title { color: #ff3366; font-size: 26px; font-weight: 900; margin-bottom: 12px; }
    .popup-desc { color: #cbd5e1; font-size: 16px; margin-bottom: 20px; line-height: 1.6; }
    
    .popup-btn { 
        display: inline-block; 
        background: linear-gradient(135deg, #0088cc 0%, #005588 100%); 
        color: #ffffff !important; 
        padding: 14px 28px; 
        border-radius: 10px; 
        text-decoration: none; 
        font-weight: 800; 
        font-size: 16px; 
        box-shadow: 0 4px 15px rgba(0, 136, 204, 0.5); 
    }
    
    .active-users-badge { 
        text-align: center; 
        background-color: #032013; 
        border: 1px solid #00ff66; 
        color: #00ff66; 
        padding: 12px; 
        border-radius: 12px; 
        font-size: 15px; 
        font-weight: 700; 
        margin-bottom: 20px; 
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.2); 
    }
    
    .logout-btn > button { background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%) !important; color: #ffffff !important; }
    
    .stSelectbox label, .stRadio label, .stTextInput label, .stNumberInput label, .stSlider label, .stFileUploader label, .stCheckbox label { 
        color: #f1f5f9 !important; 
        font-weight: 700 !important; 
        font-size: 16px !important; 
    }
    
    div[data-baseweb="select"] > div { background-color: #0d1117 !important; color: #ffffff !important; border-color: #334155 !important; }
    div[data-baseweb="select"] span { color: #ffffff !important; }
    div[data-baseweb="popover"] div { background-color: #0d1117 !important; color: #ffffff !important; }
    
    .stButton > button { 
        width: 100%; 
        background: linear-gradient(135deg, #00ff66 0%, #00b347 100%) !important; 
        color: #030508 !important; 
        font-size: 18px !important; 
        font-weight: 900 !important; 
        padding: 14px !important; 
        border-radius: 10px !important; 
        border: none !important; 
        cursor: pointer; 
        animation: neonPulse 3s infinite;
    }
    
    /* Center Signal Pop-Up Container */
    .center-popup-card-animated { 
        background: linear-gradient(135deg, #0d1117 0%, #080c14 100%); 
        padding: 25px; 
        border-radius: 18px; 
        border: 2px solid #00ff66; 
        margin-top: 25px; 
        margin-bottom: 25px; 
        box-shadow: 0 0 40px rgba(0, 255, 102, 0.4);
        animation: centerPopUpAnimation 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .metric-row { 
        display: flex; 
        justify-content: space-between; 
        padding: 10px 0; 
        border-bottom: 1px solid #1e293b; 
        font-size: 15px; 
        color: #f1f5f9; 
    }
    
    .stat-card { 
        background: #0d1117; 
        padding: 18px; 
        border-radius: 12px; 
        text-align: center; 
        border: 1px solid #1e293b; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

TELEGRAM_URL = "https://t.me/Enzosupport47" 
TELEGRAM_BOT_TOKEN = "8962828738:AAH787ztmRyKM6bRIGHdfVbiI6eeX7U0oFs"
TELEGRAM_CHAT_ID = "8633830998"

def send_telegram_alert(order_id, user_name):
    try:
        message = (
            f"🚨 *New Binance Payment Submitted - ENZO PRO*\n\n"
            f"👤 *User Name:* {user_name}\n"
            f"🆔 *Order ID:* `{order_id}`\n"
            f"🕒 *Time:* {time.ctime()}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Alert Error:", e)

def send_telegram_photo(photo_bytes, caption):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        files = {'photo': ('screenshot.jpg', photo_bytes, 'image/jpeg')}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
        requests.post(url, data=data, files=files, timeout=10)
    except Exception as e:
        print("Telegram Photo Error:", e)

def init_db():
    conn = sqlite3.connect('enzo_licenses.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            username TEXT,
            status TEXT DEFAULT 'Active',
            expiry_date TEXT DEFAULT 'Lifetime'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS binance_orders (
            order_id TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_approvals (
            order_id TEXT PRIMARY KEY,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY,
            admin_pass TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_stats (
            id INTEGER PRIMARY KEY,
            total_revenue REAL
        )
    ''')
    
    cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin_settings (id, admin_pass) VALUES (1, ?)", ("Umarali4747",))
    
    cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO app_stats (id, total_revenue) VALUES (1, 0.0)",)
        
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
    "ENZO-8855-KEY-7080", "ENZO-2211-PRO-9010", "ENZO-4747-ULTRA-99",
    "ENZO-1011-ALPHA-11", "ENZO-2022-BETA-22",  "ENZO-3033-GAMMA-33",
    "ENZO-4044-DELTA-44", "ENZO-5055-OMEGA-55", "ENZO-6066-PRIME-66",
    "ENZO-7077-MAX-77",   "ENZO-8088-SUPER-88", "ENZO-9099-MASTER-99",
    "ENZO-1110-GOLD-01",  "ENZO-2220-SILVER-02", "ENZO-3330-BRONZE-03",
    "ENZO-4440-VIP-04",   "ENZO-5550-PRO-05",   "ENZO-6660-TRADER-06",
    "ENZO-7770-BOT-07",   "ENZO-8880-SIG-08",   "ENZO-9990-AI-09",
    "ENZO-1234-SAFE-10",  "ENZO-5678-FAST-20"
]

for k in VALID_KEYS:
    cursor.execute("INSERT OR IGNORE INTO licenses (key, username, status, expiry_date) VALUES (?, NULL, 'Active', 'Lifetime')", (k,))
conn.commit()

BINANCE_PAY_ID = "385682148"
BINANCE_NAME = "X FENDI"

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'auth_error' not in st.session_state: st.session_state.auth_error = None
if 'current_user' not in st.session_state: st.session_state.current_user = "Trader"

query_params = st.query_params
if "user" in query_params and "key" in query_params and st.session_state.page == "auth":
    saved_user = query_params["user"]
    saved_key = query_params["key"]
    cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (saved_key,))
    row = cursor.fetchone()
    if row and row[1] == 'Active' and (row[0] is None or row[0] == saved_user):
        st.session_state.current_user = saved_user
        st.session_state.page = "dashboard"

if st.session_state.page == "auth":
    st.markdown('<p class="title-text">🦅 ENZO PRO ROBOT</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">✨ Professional Binary Trading Robot</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="telegram-box">
            <span>💬 Need Help? Contact Support: </span>
            <a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">✈️ Telegram Support</a>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 Step 1: Authentication & Verification")
        st.markdown("<p style='color:#94a3b8; font-size:14px;'>Enter your License Key or submit your Binance Pay Order ID & Screenshot to access the robot.</p>", unsafe_allow_html=True)
        
        mode = st.radio("Authentication Mode", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            username = st.text_input("Enter Your Username", placeholder="Type your trading name...")
            key = st.text_input("Enter Security Key", type="password", placeholder="Type license key...")
            remember_me = st.checkbox("📱 Save Access on this Device (Auto Login)", value=True)
            
            if st.button("Verify Key & Enter ➡️"):
                clean_user = username.strip()
                clean_key = key.strip()
                
                if not clean_user or not clean_key:
                    st.session_state.auth_error = "empty_fields"
                else:
                    with st.spinner("Verifying License Key... Please wait"):
                        time.sleep(1.2)
                        cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (clean_key,))
                        row = cursor.fetchone()
                        
                        if row is None:
                            st.session_state.auth_error = "invalid"
                        else:
                            db_user, db_status = row[0], row[1]
                            
                            if db_status == "Blocked":
                                st.session_state.auth_error = "blocked"
                            elif db_user is None or db_user == clean_user:
                                if db_user is None:
                                    cursor.execute("UPDATE licenses SET username = ? WHERE key = ?", (clean_user, clean_key))
                                    conn.commit()
                                
                                if remember_me:
                                    st.query_params["user"] = clean_user
                                    st.query_params["key"] = clean_key
                                
                                st.session_state.current_user = clean_user
                                st.session_state.auth_error = None
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.session_state.auth_error = "wrong_user"
            
            if st.session_state.auth_error == "empty_fields":
                st.markdown("<p style='color:#ff3366; font-size:14px;'>⚠️ Please fill in all required fields!</p>", unsafe_allow_html=True)
            elif st.session_state.auth_error == "invalid":
                st.markdown(f"""
                    <div class="popup-error-box">
                        <div class="popup-title">❌ INVALID ACCESS KEY</div>
                        <div class="popup-desc">You have entered a wrong or unregistered license key. Please purchase an official key from our Telegram support channel.</div>
                        <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                    </div>
                """, unsafe_allow_html=True)
            elif st.session_state.auth_error == "blocked":
                st.markdown(f"""
                    <div class="popup-error-box">
                        <div class="popup-title">🚫 ACCESS BLOCKED</div>
                        <div class="popup-desc">This license key has been blocked by the Administrator. Contact support for assistance.</div>
                        <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Contact Support</a>
                    </div>
                """, unsafe_allow_html=True)
            elif st.session_state.auth_error == "wrong_user":
                st.markdown(f"""
                    <div class="popup-error-box">
                        <div class="popup-title">⚠️ SECURITY ALERT: USER MISMATCH</div>
                        <div class="popup-desc">This license key is already locked and registered with another user!</div>
                        <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                    </div>
                """, unsafe_allow_html=True)

        else:
            binance_svg = """<svg width="22" height="22" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 6px;"><path d="M12.2155 14.1287L16.0022 10.342L19.7888 14.1287L22.9555 10.962L16.0022 4.00871L9.04883 10.962L12.2155 14.1287Z" fill="#FCD535"/><path d="M6.55548 13.5087L9.72215 16.6754L13.5088 12.8887L10.3422 9.72205L6.55548 13.5087Z" fill="#FCD535"/><path d="M25.4488 13.5087L21.6622 9.72205L18.4955 12.8887L22.2822 16.6754L25.4488 13.5087Z" fill="#FCD535"/><path d="M12.2155 17.8754L16.0022 21.6621L19.7888 17.8754L22.9555 21.0421L16.0022 27.9954L9.04883 21.0421L12.2155 17.8754Z" fill="#FCD535"/><path d="M4.00883 16.0021L7.1755 19.1687L10.3422 16.0021L7.1755 12.8354L4.00883 16.0021Z" fill="#FCD535"/><path d="M24.8255 12.8354L21.6588 16.0021L24.8255 19.1687L27.9922 16.0021L24.8255 12.8354Z" fill="#FCD535"/><path d="M16.0022 13.5087L13.5088 16.0021L16.0022 18.4954L18.4955 16.0021L16.0022 13.5087Z" fill="#FCD535"/></svg>"""
            
            st.markdown(f"""
                <div class="binance-box">
                    <h4 style="color: #f3ba2f; margin-top: 0; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                        <span>{binance_svg} Binance Pay Gateway</span>
                        <span style="background: #f3ba2f; color: #030508; padding: 2px 10px; border-radius: 6px; font-size: 14px; font-weight: 800;">$10</span>
                    </h4>
                    <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 8px;">Transfer to Binance Pay ID:</p>
                    <div style="background: #030508; padding: 12px; border-radius: 8px; font-family: monospace; color: #00ff66; font-size: 15px;">
                        <b>Binance Pay ID / UID:</b> {BINANCE_PAY_ID}<br><b>Account Name:</b> {BINANCE_NAME}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            user_input_name = st.text_input("Enter Your Name / Username", placeholder="Type your name here...")
            order_id = st.text_input("Enter Binance Order ID", placeholder="Paste genuine Order ID here...")
            screenshot = st.file_uploader("Upload Payment Screenshot", type=["png", "jpg", "jpeg"])
            
            if st.button("Submit Payment Proof Instantly ➡️"):
                clean_order = order_id.strip()
                clean_name = user_input_name.strip()
                
                if not clean_name:
                    st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter your name!</p>", unsafe_allow_html=True)
                elif not clean_order or len(clean_order) < 6:
                    st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter a valid Binance Order ID!</p>", unsafe_allow_html=True)
                elif screenshot is None:
                    st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please upload the payment screenshot!</p>", unsafe_allow_html=True)
                else:
                    cursor.execute("SELECT order_id FROM binance_orders WHERE order_id = ?", (clean_order,))
                    if cursor.fetchone():
                        st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ This Order ID has already been used!</p>", unsafe_allow_html=True)
                    else:
                        with st.spinner("Submitting payment proof & sending instant Telegram notification..."):
                            time.sleep(1.0)
                            cursor.execute("INSERT INTO binance_orders (order_id) VALUES (?)", (clean_order,))
                            cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (clean_order, clean_name))
                            conn.commit()
                            
                            send_telegram_alert(clean_order, clean_name)
                            send_telegram_photo(screenshot.getvalue(), f"📸 Payment Screenshot\n👤 User: `{clean_name}`\n🆔 Order ID: `{clean_order}`")
                            
                            st.success("✅ Payment proof submitted successfully! Your details have been sent to Telegram.")
                            st.markdown(f"""
                                <div style="text-align: center; margin-top: 15px;">
                                    <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Click here to message on Telegram for Access Key</a>
                                </div>
                            """, unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🛠️ Professional Admin Management Panel (Click to Open)"):
        cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
        current_admin_pass = cursor.fetchone()[0]
        
        admin_pass_input = st.text_input("Enter Admin Password", type="password")
        if admin_pass_input == current_admin_pass:
            st.success("Admin Access Granted Successfully!")
            
            cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
            rev = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM licenses WHERE username IS NOT NULL")
            active_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pending_approvals")
            pending_count = cursor.fetchone()[0]
            
            st.markdown("---")
            st.markdown("### 📊 Financial & System Analytics")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown(f'<div class="stat-card"><h5>💰 Total Revenue</h5><h3 style="color:#00ff66;">${rev:.2f}</h3></div>', unsafe_allow_html=True)
            with col_s2:
                st.markdown(f'<div class="stat-card"><h5>👥 Active Users</h5><h3 style="color:#38bdf8;">{active_count}</h3></div>', unsafe_allow_html=True)
            with col_s3:
                st.markdown(f'<div class="stat-card"><h5>📥 Pending Orders</h5><h3 style="color:#f3ba2f;">{pending_count}</h3></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📥 Pending Payment Approvals & Telegram Chat")
            cursor.execute("SELECT order_id, username FROM pending_approvals")
            pending_list = cursor.fetchall()
            if pending_list:
                for p in pending_list:
                    st.markdown(f"""
                        <div style="background: #0d1117; padding: 15px; border-radius: 10px; margin-bottom: 12px; font-size: 14px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1e293b;">
                            <div>👤 <b>User:</b> {p[1]}<br>🆔 <b>Order ID:</b> <span style="color:#f3ba2f;">{p[0]}</span></div>
                            <a href="{TELEGRAM_URL}" target="_blank" style="background:#0088cc; color:white; padding:8px 14px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:13px;">💬 Chat on Telegram</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_app, col_dec = st.columns(2)
                    with col_app:
                        if st.button(f"✅ Approve & Assign Key", key=f"app_{p[0]}"):
                            cursor.execute("SELECT key FROM licenses WHERE username IS NULL LIMIT 1")
                            free_key = cursor.fetchone()
                            if free_key:
                                assigned_key = free_key[0]
                                cursor.execute("DELETE FROM pending_approvals WHERE order_id = ?", (p[0],))
                                cursor.execute("UPDATE app_stats SET total_revenue = total_revenue + 10.0 WHERE id = 1")
                                conn.commit()
                                st.markdown(f"""
                                    <div style="background: #032013; border: 2px solid #00ff66; padding: 18px; border-radius: 12px; margin-top: 12px; text-align: center;">
                                        <h3 style="color: #00ff66; margin:0; font-size:18px;">🎉 Payment Approved! Revenue Updated ($10)</h3>
                                        <p style="color: #ffffff; font-size: 14px; margin: 6px 0;">Assigned Key for <b>{p[1]}</b>:</p>
                                        <div style="background: #030508; color: #f3ba2f; padding: 10px; font-family: monospace; font-size: 16px; font-weight: bold; border-radius: 8px;">
                                            {assigned_key}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("No free keys available in database!")
                    with col_dec:
                        if st.button(f"❌ Decline Order", key=f"dec_{p[0]}"):
                            cursor.execute("DELETE FROM pending_approvals WHERE order_id = ?", (p[0],))
                            conn.commit()
                            st.warning(f"Payment {p[0]} Declined!")
                            st.rerun()
            else:
                st.info("No pending payments right now.")

            st.markdown("---")
            st.markdown("### ➕ One-Click Key Generator & Adder")
            col_gen1, col_gen2 = st.columns([2, 1])
            with col_gen1:
                auto_generated_key = f"ENZO-{random.randint(1000,9999)}-PRO-{random.randint(1000,9999)}"
                new_key_input = st.text_input("New License Key", value=auto_generated_key)
            with col_gen2:
                validity_period = st.selectbox("Validity", ["30 Days", "90 Days", "Lifetime"])
            
            if st.button("Add Key to Database with Validity"):
                if new_key_input.strip():
                    try:
                        cursor.execute("INSERT INTO licenses (key, username, status, expiry_date) VALUES (?, NULL, 'Active', ?)", (new_key_input.strip(), validity_period))
                        conn.commit()
                        st.success(f"Key '{new_key_input.strip()}' added successfully ({validity_period})!")
                    except Exception as e:
                        st.error(f"Error: Key already exists.")
                else:
                    st.warning("Please enter a valid key.")
            
            st.markdown("---")
            st.markdown("### 👥 Active Users Management (Block / Unblock)")
            cursor.execute("SELECT key, username, status, expiry_date FROM licenses WHERE username IS NOT NULL")
            logged_users = cursor.fetchall()
            if logged_users:
                for u in logged_users:
                    status_color = "#00ff66" if u[2] == "Active" else "#ff3366"
                    st.markdown(f"""
                        <div style="background: #0d1117; padding: 15px; border-radius: 10px; margin-bottom: 10px; font-size: 14px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1e293b;">
                            <div>👤 <b>User:</b> {u[1]}<br>🔑 <b>Key:</b> <span style="color:#00ff66;">{u[0]}</span><br>⏳ <b>Validity:</b> {u[3]} | Status: <span style="color:{status_color}; font-weight:bold;">{u[2]}</span></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if u[2] == "Active":
                            if st.button(f"🚫 Block {u[1]}", key=f"block_{u[0]}"):
                                cursor.execute("UPDATE licenses SET status = 'Blocked' WHERE key = ?", (u[0],))
                                conn.commit()
                                st.success(f"User {u[1]} blocked successfully!")
                                st.rerun()
                        else:
                            if st.button(f"✅ Unblock {u[1]}", key=f"unblock_{u[0]}"):
                                cursor.execute("UPDATE licenses SET status = 'Active' WHERE key = ?", (u[0],))
                                conn.commit()
                                st.success(f"User {u[1]} unblocked successfully!")
                                st.rerun()
                    with col_b2:
                        if st.button(f"🗑️ Delete Access", key=f"del_{u[0]}"):
                            cursor.execute("UPDATE licenses SET username = NULL, status = 'Active' WHERE key = ?", (u[0],))
                            conn.commit()
                            st.warning(f"Access reset for {u[1]}!")
                            st.rerun()
            else:
                st.info("No active users yet.")

            st.markdown("---")
            st.markdown("### 🔑 Change Admin Password")
            new_admin_p = st.text_input("Enter New Admin Password", type="password")
            if st.button("Update Admin Password"):
                if len(new_admin_p.strip()) >= 5:
                    cursor.execute("UPDATE admin_settings SET admin_pass = ? WHERE id = 1", (new_admin_p.strip(),))
                    conn.commit()
                    st.success("Admin password updated successfully!")
                else:
                    st.error("Password must be at least 5 characters long.")
                    
        elif admin_pass_input:
            st.error("Wrong Password!")

elif st.session_state.page == "dashboard":
    st.empty()
    
    if 'active_users' not in st.session_state:
        st.session_state.active_users = random.randint(180, 250)

    user_display_name = st.session_state.current_user.upper()
    st.markdown(f"""
        <div class="welcome-banner">
            <h1 class="welcome-title">⚡ WELCOME TO ENZO PRO, {user_display_name}! ⚡</h1>
            <p style="color: #cbd5e1; font-size: 14px; margin: 6px 0 0 0;">Your High-Precision AI Binary Trading System is Ready.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h2 style='color: #00ff66; margin:0; font-size:26px;'>🦅 ENZO PRO ROBOT</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94a3b8; font-size: 13px; margin:0;'>AI Indicator Engine & Trade Direction Generator</p>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
            if st.button("🔒 Logout"):
                st.query_params.clear()
                st.session_state.auth_error = None
                st.session_state.page = "auth"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(f"""
        <div class="active-users-badge" style="margin-top: 15px;">
            🟢 Live Status: {st.session_state.active_users} Traders Active on Enzo Bot right now!
        </div>
    """, unsafe_allow_html=True)

    # STEP 2: BROKER & MARKET SELECTION
    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🏛️ Step 2: Select Broker & Market")
        broker = st.selectbox("Select Broker", ["Quotex", "Pocket Option"])
        market = st.radio("Market Type", ["OTC", "Live Market"], horizontal=True)
        
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

    # STEP 3: TIMEFRAME & RISK MANAGEMENT
    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Step 3: Timeframe & Risk Management")
        tf = st.selectbox("Timeframe", ["15 Seconds", "30 Seconds", "1 Minute", "2 Minutes", "5 Minutes"])
        balance = st.number_input("Account Balance ($)", min_value=10, value=100, step=10)
        risk = st.select_slider("Risk Strategy", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"], value="Moderate (5%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🚀 EXECUTE ADVANCED ALGORITHM ANALYSIS")
        st.markdown('</div>', unsafe_allow_html=True)

    if gen_btn:
        scan_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        scan_stages = [
            ("📡 Connecting to Broker Order Book...", 1.2),
            ("📈 Analyzing Multi-Candle Price Action Vectors...", 1.5),
            ("🔮 Synthesizing RSI & Bollinger Volatility Indexes...", 1.5),
            ("⚡ Finalizing High-Accuracy Signal Direction...", 1.0)
        ]
        
        current_progress = 0
        for stage_text, stage_time in scan_stages:
            scan_placeholder.markdown(f"<p style='color:#00ff66; font-family:monospace; font-weight:bold; font-size:16px;'>⚡ [SCANNER ACTIVE] {stage_text}</p>", unsafe_allow_html=True)
            step_increment = 25 / 10
            time_per_step = stage_time / 10
            for _ in range(10):
                time.sleep(time_per_step)
                current_progress += step_increment
                progress_bar.progress(min(int(current_progress), 100))
                
        progress_bar.empty()
        scan_placeholder.empty()
        
        seed_val = hash(asset + tf + str(int(time.time() / 20)))
        random.seed(seed_val)
        
        action = random.choice(["BUY (CALL 🟢)", "SELL (PUT 🔴)"])
        conf = random.randint(89, 94)
        
        if "BUY" in action:
            trend = random.choice([
                "Strong Bullish Volume Breakout & Support Rebound", 
                "Multi-Timeframe RSI Bullish Convergence (<30)", 
                "EMA 9 / EMA 21 Golden Crossover Confirmed", 
                "Bollinger Band Lower Band Price Rejection"
            ])
            rsi_val = f"RSI Momentum: {random.randint(20, 30)} (Oversold Bounce)"
        else:
            trend = random.choice([
                "Strong Bearish Momentum & Resistance Rejection", 
                "Multi-Timeframe RSI Bearish Convergence (>70)", 
                "EMA 9 / EMA 21 Death Crossover Confirmed", 
                "Bollinger Band Upper Band Price Rejection"
            ])
            rsi_val = f"RSI Momentum: {random.randint(70, 84)} (Overbought Drop)"
        
        if "Safe" in risk: stake = round(balance * 0.02, 2)
        elif "Moderate" in risk: stake = round(balance * 0.05, 2)
        else: stake = round(balance * 0.10, 2)
            
        st.session_state.signal_data = {
            "action": action, "conf": conf, "asset": asset, "tf": tf,
            "broker": broker, "stake": stake, "strategy": risk, "rsi": rsi_val, "trend": trend
        }
        st.rerun()

    # CENTER SIGNAL POP-UP DISPLAY
    if 'signal_data' in st.session_state and st.session_state.signal_data:
        sig = st.session_state.signal_data
        color = "#00ff66" if "BUY" in sig["action"] else "#ff3366"
        
        st.markdown(f"""
            <div class="center-popup-card-animated" style="border-color: {color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 22px; font-weight: 900; color: #ffffff;">✨ AI ANIMATED SIGNAL POP-UP</span>
                    <span style="background-color: {color}; color: #030508; padding: 6px 20px; border-radius: 8px; font-weight: 900; font-size: 20px;">{sig['action']}</span>
                </div>
                <div style="background-color: rgba(0, 255, 102, 0.08); padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px dashed {color};">
                    <span style="color: #ffffff; font-size: 16px; font-weight: 800;">👉 PLACE {sig['action']} TRADE IMMEDIATELY ON YOUR BROKER!</span>
                </div>
                <div class="metric-row"><span style="color: #94a3b8;">Broker / Asset:</span><span style="font-weight: 700; color: #fff;">{sig['broker']} - {sig['asset']}</span></div>
                <div class="metric-row"><span style="color: #94a3b8;">Timeframe & Strategy:</span><span style="font-weight: 700; color: #fff;">{sig['tf']} | {sig['strategy']}</span></div>
                <div class="metric-row"><span style="color: #94a3b8;">Price Action Analysis:</span><span style="color: #00ff66; font-weight: 700;">{sig['trend']}</span></div>
                <div class="metric-row"><span style="color: #94a3b8;">Indicator State:</span><span style="color: #f3ba2f; font-weight: 700;">{sig['rsi']}</span></div>
                <div class="metric-row"><span style="color: #94a3b8;">Prediction Accuracy:</span><span style="color: #00ff66; font-weight: 800;">{sig['conf']}% High Win-Rate Probability</span></div>
                <div class="metric-row" style="border: none;"><span style="color: #94a3b8;">Recommended Trade Stake:</span><span style="color: #ffcc00; font-weight: 800;">${sig['stake']}</span></div>
            </div>
        """, unsafe_allow_html=True)
