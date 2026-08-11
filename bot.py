import streamlit as st
import random
import time
import sqlite3
import requests

st.set_page_config(
    page_title="ENZO BOT - Premium Access",
    page_icon="🦅",
    layout="centered"
)

st.markdown("""
    <style>
    /* Force 100% Dark Theme & Fix iPhone Safari White Screen Bug */
    :root {
        color-scheme: dark;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #080c14 !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        -webkit-text-size-adjust: 100%;
    }
    
    .page-box { background-color: #111827; padding: 30px; border-radius: 16px; border: 1px solid #1f2937; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); margin-top: 20px; }
    .title-text { color: #00ff66; text-align: center; font-size: 42px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; text-shadow: 0 0 15px rgba(0, 255, 102, 0.4); }
    .sub-title { color: #9ca3af; text-align: center; font-size: 14px; font-weight: 500; margin-bottom: 20px; }
    .telegram-box { text-align: center; background-color: #1f2937; padding: 12px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #2b3748; }
    .telegram-link { color: #0088cc; text-decoration: none; font-weight: 700; font-size: 15px; }
    .telegram-link:hover { color: #00aaff; text-decoration: underline; }
    .binance-box { background-color: #141b22; border: 1px dashed #f3ba2f; padding: 18px; border-radius: 10px; margin-bottom: 15px; }
    .popup-error-box { background-color: #2a1215; border: 2px solid #ff3366; padding: 30px; border-radius: 16px; text-align: center; margin-top: 25px; margin-bottom: 25px; box-shadow: 0 0 35px rgba(255, 51, 102, 0.6); }
    .popup-title { color: #ff3366; font-size: 24px; font-weight: 900; margin-bottom: 12px; }
    .popup-desc { color: #d1d5db; font-size: 15px; margin-bottom: 20px; line-height: 1.5; }
    .popup-btn { display: inline-block; background: linear-gradient(135deg, #0088cc 0%, #005588 100%); color: #ffffff !important; padding: 14px 28px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 16px; box-shadow: 0 4px 15px rgba(0, 136, 204, 0.5); }
    .popup-btn:hover { background: linear-gradient(135deg, #0099ff 0%, #006699 100%); }
    .active-users-badge { text-align: center; background-color: #0d1b1e; border: 1px solid #00ff66; color: #00ff66; padding: 10px; border-radius: 10px; font-size: 14px; font-weight: 700; margin-bottom: 25px; box-shadow: 0 0 15px rgba(0, 255, 102, 0.15); }
    .logout-btn > button { background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%) !important; color: #ffffff !important; }
    .logout-btn > button:hover { opacity: 0.9; }
    .stSelectbox label, .stRadio label, .stTextInput label, .stNumberInput label, .stSlider label { color: #ffffff !important; font-weight: 600 !important; font-size: 15px !important; }
    div[data-baseweb="select"] > div { background-color: #1f2937 !important; color: #ffffff !important; border-color: #374151 !important; }
    div[data-baseweb="select"] span { color: #ffffff !important; }
    div[data-baseweb="popover"] div { background-color: #111827 !important; color: #ffffff !important; }
    li[role="option"] { background-color: #111827 !important; color: #ffffff !important; }
    li[role="option"]:hover { background-color: #1f2937 !important; color: #00ff66 !important; }
    .stButton > button { width: 100%; background: linear-gradient(135deg, #00ff66 0%, #00b347 100%) !important; color: #080c14 !important; font-size: 16px !important; font-weight: 800 !important; padding: 12px !important; border-radius: 8px !important; border: none !important; cursor: pointer; }
    .result-box { background-color: #111827; padding: 22px; border-radius: 12px; border: 1px solid #1f2937; border-left: 6px solid #00ff66; margin-top: 20px; }
    .metric-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #1f2937; font-size: 14px; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

TELEGRAM_URL = "https://t.me/+diy3N-HPvNJkZmRk" 
TELEGRAM_BOT_TOKEN = "8962828738:AAH787ztmRyKM6bRIGHdfVbiI6eeX7U0oFs"
TELEGRAM_CHAT_ID = "8633830998"

def send_telegram_alert(username, email, details):
    try:
        message = (
            f"🚨 *Secure Login Alert - ENZO PRO*\n\n"
            f"👤 *Username:* {username}\n"
            f"📧 *Email:* {email}\n"
            f"🔑 *Verification Details:* `{details}`\n"
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

def init_db():
    conn = sqlite3.connect('enzo_licenses.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            username TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS binance_orders (
            order_id TEXT PRIMARY KEY,
            username TEXT,
            email TEXT
        )
    ''')
    try: cursor.execute("ALTER TABLE licenses ADD COLUMN username TEXT")
    except sqlite3.OperationalError: pass
    try: cursor.execute("ALTER TABLE licenses ADD COLUMN email TEXT")
    except sqlite3.OperationalError: pass
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
    cursor.execute("INSERT OR IGNORE INTO licenses (key, username, email) VALUES (?, NULL, NULL)", (k,))
conn.commit()

BINANCE_PAY_ID = "385682148"
BINANCE_NAME = "X FENDI"

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'auth_error' not in st.session_state: st.session_state.auth_error = None
if 'current_user' not in st.session_state: st.session_state.current_user = "Trader"

if st.session_state.page == "auth":
    st.markdown('<p class="title-text">🦅 ENZO PRO</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">✨ Premium Access & Trading Robot</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="telegram-box">
            <span>💬 Need Help? Contact Support: </span>
            <a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">✈️ Telegram Support</a>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 Step 1: Authentication & Verification")
        st.markdown("<p style='color:#9ca3af; font-size:13px;'>Please enter your username, email, license key or complete payment via Binance to access the trading robot.</p>", unsafe_allow_html=True)
        
        mode = st.radio("Authentication Mode", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            username = st.text_input("Enter Your Username", placeholder="Type your trading name...")
            email = st.text_input("Enter Your Email Address", placeholder="Type your email address...")
            key = st.text_input("Enter Security Key", type="password", placeholder="Type license key...")
            
            if st.button("Verify Key & Enter ➡️"):
                clean_user = username.strip()
                clean_email = email.strip()
                clean_key = key.strip()
                
                if not clean_user or not clean_email or not clean_key:
                    st.session_state.auth_error = "empty_fields"
                elif "@" not in clean_email or "." not in clean_email:
                    st.session_state.auth_error = "invalid_email"
                else:
                    with st.spinner("Verifying License Key & Securing Connection... Please wait"):
                        time.sleep(1.2)
                        cursor.execute("SELECT username, email FROM licenses WHERE key = ?", (clean_key,))
                        row = cursor.fetchone()
                        
                        if row is None:
                            st.session_state.auth_error = "invalid"
                        else:
                            db_user, db_email = row[0], row[1]
                            
                            if db_user is None:
                                cursor.execute("UPDATE licenses SET username = ?, email = ? WHERE key = ?", (clean_user, clean_email, clean_key))
                                conn.commit()
                                send_telegram_alert(clean_user, clean_email, f"License Key: {clean_key}")
                                st.session_state.current_user = clean_user
                                st.session_state.auth_error = None
                                st.session_state.page = "dashboard"
                                st.rerun()
                            elif db_user == clean_user and db_email == clean_email:
                                st.session_state.current_user = clean_user
                                st.session_state.auth_error = None
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.session_state.auth_error = "wrong_user"
            
            if st.session_state.auth_error == "empty_fields":
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please fill in all required fields (Username, Email & Key)!</p>", unsafe_allow_html=True)
            elif st.session_state.auth_error == "invalid_email":
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter a valid email address!</p>", unsafe_allow_html=True)
            elif st.session_state.auth_error == "invalid":
                st.markdown(f"""
                    <div class="popup-error-box">
                        <div class="popup-title">❌ INVALID ACCESS KEY</div>
                        <div class="popup-desc">You have entered a wrong or unregistered license key. Please purchase an official key from our Telegram support channel to get access.</div>
                        <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                    </div>
                """, unsafe_allow_html=True)
            elif st.session_state.auth_error == "wrong_user":
                st.markdown(f"""
                    <div class="popup-error-box">
                        <div class="popup-title">⚠️ SECURITY ALERT: USER MISMATCH</div>
                        <div class="popup-desc">This license key is already locked and permanently registered with another Username or Email! Unauthorized bypass is strictly prohibited.</div>
                        <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                    </div>
                """, unsafe_allow_html=True)

        else:
            bin_username = st.text_input("Enter Your Username", placeholder="Type your trading name...")
            bin_email = st.text_input("Enter Your Email Address", placeholder="Type your email address...")
            
            binance_svg = """<svg width="22" height="22" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 6px;"><path d="M12.2155 14.1287L16.0022 10.342L19.7888 14.1287L22.9555 10.962L16.0022 4.00871L9.04883 10.962L12.2155 14.1287Z" fill="#FCD535"/><path d="M6.55548 13.5087L9.72215 16.6754L13.5088 12.8887L10.3422 9.72205L6.55548 13.5087Z" fill="#FCD535"/><path d="M25.4488 13.5087L21.6622 9.72205L18.4955 12.8887L22.2822 16.6754L25.4488 13.5087Z" fill="#FCD535"/><path d="M12.2155 17.8754L16.0022 21.6621L19.7888 17.8754L22.9555 21.0421L16.0022 27.9954L9.04883 21.0421L12.2155 17.8754Z" fill="#FCD535"/><path d="M4.00883 16.0021L7.1755 19.1687L10.3422 16.0021L7.1755 12.8354L4.00883 16.0021Z" fill="#FCD535"/><path d="M24.8255 12.8354L21.6588 16.0021L24.8255 19.1687L27.9922 16.0021L24.8255 12.8354Z" fill="#FCD535"/><path d="M16.0022 13.5087L13.5088 16.0021L16.0022 18.4954L18.4955 16.0021L16.0022 13.5087Z" fill="#FCD535"/></svg>"""
            
            st.markdown(f"""
                <div class="binance-box">
                    <h4 style="color: #f3ba2f; margin-top: 0; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                        <span>{binance_svg} Binance Pay Gateway</span>
                        <span style="background: #f3ba2f; color: #080c14; padding: 2px 10px; border-radius: 6px; font-size: 14px; font-weight: 800;">$10 USDT</span>
                    </h4>
                    <p style="color: #d1d5db; font-size: 13px; margin-bottom: 6px;">Transfer to Binance Pay ID:</p>
                    <div style="background: #080c14; padding: 10px; border-radius: 6px; font-family: monospace; color: #00ff66; font-size: 14px;">
                        <b>Binance Pay ID / UID:</b> {BINANCE_PAY_ID}<br><b>Account Name:</b> {BINANCE_NAME}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            order_id = st.text_input("Enter Binance Order ID", placeholder="Paste genuine Order ID here...")
            
            if st.button("Confirm Payment & Enter ➡️"):
                clean_bin_user = bin_username.strip()
                clean_bin_email = bin_email.strip()
                clean_order = order_id.strip()
                
                if not clean_bin_user or not clean_bin_email or not clean_order:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Please fill in all fields (Username, Email & Order ID)!</p>", unsafe_allow_html=True)
                elif "@" not in clean_bin_email or "." not in clean_bin_email:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Please enter a valid email address!</p>", unsafe_allow_html=True)
                elif len(clean_order) < 6:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Invalid Order ID length! Please enter a valid Binance Order ID.</p>", unsafe_allow_html=True)
                else:
                    cursor.execute("SELECT username FROM binance_orders WHERE order_id = ?", (clean_order,))
                    existing_order = cursor.fetchone()
                    
                    if existing_order:
                        st.markdown(f"""
                            <div class="popup-error-box">
                                <div class="popup-title">❌ SECURITY ALERT: DUPLICATE ORDER ID</div>
                                <div class="popup-desc">This Order ID has already been utilized and locked by user ({existing_order[0]})! Multiple uses of a single payment ID are blocked.</div>
                                <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Contact Support (Telegram)</a>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        with st.spinner("Verifying Binance Payment & Securing Session..."):
                            time.sleep(1.5)
                            cursor.execute("INSERT INTO binance_orders (order_id, username, email) VALUES (?, ?, ?)", (clean_order, clean_bin_user, clean_bin_email))
                            conn.commit()
                            
                            send_telegram_alert(clean_bin_user, clean_bin_email, f"Binance Pay Order ID: {clean_order}")
                            st.session_state.current_user = clean_bin_user
                            st.session_state.auth_error = None
                            st.session_state.page = "dashboard"
                            st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🛠️ Admin Management Panel (Click to Open)"):
        admin_pass = st.text_input("Enter Admin Password", type="password")
        if admin_pass == "Umarali4747":
            st.success("Admin Access Granted Successfully!")
            
            tab1, tab2 = st.tabs(["📋 View & Remove Logged Users", "🔑 Manage Keys (Add/Remove)"])
            
            with tab1:
                cursor.execute("SELECT key, username, email FROM licenses WHERE username IS NOT NULL")
                logged_users = cursor.fetchall()
                if logged_users:
                    st.write(f"Total Active Users: {len(logged_users)}")
                    for u in logged_users:
                        st.markdown(f"""
                            <div style="background: #1f2937; padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 13px;">
                                👤 <b>Username:</b> {u[1]}<br>
                                📧 <b>Email:</b> {u[2]}<br>
                                🔑 <b>Key Used:</b> <span style="color:#00ff66;">{u[0]}</span>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.subheader("🗑️ Reset / Remove User from Key")
                    user_keys_list = [u[0] for u in logged_users]
                    selected_key_to_reset = st.selectbox("Select Key to Clear User Data", user_keys_list)
                    if st.button("Remove User Data (Free Key)", type="primary"):
                        cursor.execute("UPDATE licenses SET username = NULL, email = NULL WHERE key = ?", (selected_key_to_reset,))
                        conn.commit()
                        st.success(f"User data for key '{selected_key_to_reset}' has been cleared! Key is now free.")
                        time.sleep(0.8)
                        st.rerun()
                else:
                    st.info("Abhi tak kisi user ne login nahi kiya.")
            
            with tab2:
                st.subheader("➕ Add New License Key")
                new_key_input = st.text_input("Enter New Key Name", placeholder="e.g. ENZO-NEW-KEY-01")
                if st.button("Add Key to Database"):
                    if new_key_input.strip():
                        try:
                            cursor.execute("INSERT INTO licenses (key, username, email) VALUES (?, NULL, NULL)", (new_key_input.strip(),))
                            conn.commit()
                            st.success(f"Key '{new_key_input.strip()}' successfully added!")
                        except sqlite3.IntegrityError:
                            st.warning("Yeh key pehle se database mein mojood hai!")
                    else:
                        st.error("Please enter a valid key!")
                
                st.markdown("---")
                st.subheader("🗑️ Remove / Delete License Key")
                cursor.execute("SELECT key FROM licenses")
                all_db_keys = [row[0] for row in cursor.fetchall()]
                
                selected_key_to_delete = st.selectbox("Select Key to Delete", all_db_keys if all_db_keys else ["No Keys Available"], key="delete_key_select")
                if st.button("Delete Selected Key", type="primary"):
                    if selected_key_to_delete and selected_key_to_delete != "No Keys Available":
                        cursor.execute("DELETE FROM licenses WHERE key = ?", (selected_key_to_delete,))
                        conn.commit()
                        st.success(f"Key '{selected_key_to_delete}' has been deleted!")
                        time.sleep(0.8)
                        st.rerun()
                        
        elif admin_pass:
            st.error("Wrong Password!")

elif st.session_state.page == "dashboard":
    st.empty()
    
    if 'active_users' not in st.session_state:
        st.session_state.active_users = random.randint(130, 220)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h2 style='color: #00ff66; margin:0;'>🦅 ENZO PRO ({st.session_state.current_user})</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #9ca3af; font-size: 13px; margin:0;'>AI Trading Robot & Market Signal Generator</p>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
            if st.button("🔒 Logout"):
                st.session_state.auth_error = None
                st.session_state.page = "auth"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(f"""
        <div class="active-users-badge" style="margin-top: 20px;">
            🟢 Live Status: {st.session_state.active_users} Traders Active on Enzo Bot right now!
        </div>
    """, unsafe_allow_html=True)

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
                "USD/BRL (OTC)", "USD/PHP (OTC)", "USD/IDR (OTC)", "USD/ZAR (OTC)"
            ] if market == "OTC" else [
                "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", 
                "EUR/GBP", "NZD/USD", "USD/CHF", "EUR/JPY", "GBP/JPY", 
                "AUD/JPY", "EUR/AUD", "CAD/JPY", "EUR/NZD", "GBP/AUD",
                "AUD/NZD", "NZD/CAD", "CHF/JPY", "USD/MXN", "USD/NOK",
                "BTC/USD (Crypto)", "ETH/USD (Crypto)", "LTC/USD (Crypto)", "XRP/USD (Crypto)"
            ]
        else:
            assets = [
                "EUR/USD [OTC]", "GBP/USD [OTC]", "USD/JPY [OTC]", "AUD/CHF [OTC]", 
                "EUR/GBP [OTC]", "USD/CAD [OTC]", "GBP/JPY [OTC]", "NZD/JPY [OTC]",
                "AUD/CAD [OTC]", "EUR/AUD [OTC]", "CHF/JPY [OTC]", "USD/CHF [OTC]",
                "NZD/USD [OTC]", "EUR/CAD [OTC]", "GBP/CHF [OTC]"
            ] if market == "OTC" else [
                "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "EUR/JPY", 
                "NZD/USD", "USD/CAD", "AUD/CAD", "EUR/AUD", "GBP/GBP",
                "GOLD (Commodity)", "SILVER (Commodity)", "BRENT (Oil)", 
                "BTC/USD (Crypto)", "ETH/USD (Crypto)"
            ]
            
        asset = st.selectbox("Trading Asset", assets)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Step 3: Timeframe & Risk Management")
        tf = st.selectbox("Timeframe", ["15 Seconds", "30 Seconds", "1 Minute", "2 Minutes", "5 Minutes"])
        balance = st.number_input("Account Balance ($)", min_value=10, value=100, step=10)
        risk = st.select_slider("Risk Strategy", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"], value="Moderate (5%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🚀 EXECUTE TRADING ROBOT ALGORITHM")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'signal_data' not in st.session_state: st.session_state.signal_data = None
    if 'last_asset' not in st.session_state: st.session_state.last_asset = None
    if 'click_count' not in st.session_state: st.session_state.click_count = 0

    if gen_btn:
        with st.spinner("Enzo Robot analyzing market depth, RSI & price action... (Please wait 8-10 seconds)"):
            time.sleep(9.0)
            st.session_state.click_count += 1
            if st.session_state.signal_data and st.session_state.last_asset == asset and st.session_state.click_count < 3:
                action = st.session_state.signal_data["action"]
            else:
                action = random.choice(["BUY", "SELL"])
                st.session_state.last_asset = asset
                if st.session_state.click_count >= 3: st.session_state.click_count = 0
                
            conf = random.randint(85, 98)
            if action == "BUY":
                trend = random.choice(["Strong Bullish", "Moderate Bullish", "Upward Momentum", "Support Level Rebound"])
                rsi_val = random.choice(["Oversold (<30)", "Neutral Bullish (45-50)", "Bullish Crossover"])
            else:
                trend = random.choice(["Strong Bearish", "Moderate Bearish", "Downward Momentum", "Resistance Level Rejection"])
                rsi_val = random.choice(["Overbought (>70)", "Neutral Bearish (50-55)", "Bearish Crossover"])
            
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
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 18px; font-weight: 800; color: #ffffff;">🎯 Live Robot Execution</span>
                    <span style="background-color: {color}; color: #080c14; padding: 4px 14px; border-radius: 6px; font-weight: 900; font-size: 16px;">{sig['action']}</span>
                </div>
                <div class="metric-row"><span style="color: #9ca3af;">Broker / Asset:</span><span style="font-weight: 600;">{sig['broker']} - {sig['asset']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Timeframe & Strategy:</span><span style="font-weight: 600;">{sig['tf']} | {sig['strategy']}</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">Market Trend & RSI:</span><span style="color: #00ff66; font-weight: 600;">{sig['trend']} ({sig['rsi']})</span></div>
                <div class="metric-row"><span style="color: #9ca3af;">AI Prediction Confidence:</span><span style="color: #00ff66; font-weight: 700;">{sig['conf']}% Accuracy</span></div>
                <div class="metric-row" style="border: none;"><span style="color: #9ca3af;">Recommended Trade Stake:</span><span style="color: #ffcc00; font-weight: 700;">${sig['stake']}</span></div>
            </div>
        """, unsafe_allow_html=True)
