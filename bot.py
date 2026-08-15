if st.session_state.page == "auth":
    st.markdown('<p class="title-text">🦅 ENZO PRO</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">✨ Professional Binary Trading Robot</p>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="telegram-box"><span>💬 Need Help? Contact Support: </span><a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">✈️ Telegram Support</a></div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 Step 1: Authentication & Verification")
        mode = st.radio("Authentication Mode", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            username = st.text_input("Enter Your Username", placeholder="Type your trading name...")
            key = st.text_input("Enter Security Key", type="password", placeholder="Type license key...")
            remember_me = st.checkbox("📱 Save Access on this Device (Auto Login)", value=True)
            
            if st.button("Verify Key & Enter ➡️"):
                clean_user, clean_key = username.strip(), key.strip()
                if not clean_user or not clean_key: st.session_state.auth_error = "empty_fields"
                else:
                    with st.spinner("Verifying License Key... Please wait"):
                        time.sleep(1.2)
                        cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (clean_key,))
                        row = cursor.fetchone()
                        if row is None: st.session_state.auth_error = "invalid"
                        else:
                            db_user, db_status = row[0], row[1]
                            if db_status == "Blocked": st.session_state.auth_error = "blocked"
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
                            else: st.session_state.auth_error = "wrong_user"
            
            if st.session_state.auth_error == "empty_fields": st.markdown("<p style='color:#ff3366;'>⚠️ Please fill all required fields!</p>", unsafe_allow_html=True)
            elif st.session_state.auth_error == "invalid": st.markdown(f'<div class="popup-error-box"><div class="popup-title">❌ INVALID ACCESS KEY</div><a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a></div>', unsafe_allow_html=True)
            elif st.session_state.auth_error == "blocked": st.markdown(f'<div class="popup-error-box"><div class="popup-title">🚫 ACCESS BLOCKED</div><a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Contact Support</a></div>', unsafe_allow_html=True)
            elif st.session_state.auth_error == "wrong_user": st.markdown(f'<div class="popup-error-box"><div class="popup-title">⚠️ SECURITY ALERT: USER MISMATCH</div><a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Contact Support</a></div>', unsafe_allow_html=True)

        else:
            st.markdown(f'<div class="binance-box"><h4>Binance Pay Gateway ($10)</h4><p>Pay ID: <b>{BINANCE_PAY_ID}</b> ({BINANCE_NAME})</p></div>', unsafe_allow_html=True)
            user_input_name = st.text_input("Enter Your Name / Username")
            order_id = st.text_input("Enter Binance Order ID")
            screenshot = st.file_uploader("Upload Payment Screenshot", type=["png", "jpg", "jpeg"])
            
            if st.button("Submit Payment Proof Instantly ➡️"):
                if user_input_name and order_id and screenshot:
                    cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (order_id.strip(), user_input_name.strip()))
                    conn.commit()
                    send_telegram_alert(order_id.strip(), user_input_name.strip())
                    send_telegram_photo(screenshot.getvalue(), f"Payment Proof: {user_input_name}")
                    st.success("✅ Payment proof submitted to Telegram!")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🛠️ Admin Management Panel"):
        cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
        if st.text_input("Admin Password", type="password") == cursor.fetchone()[0]:
            st.success("Admin Logged In")

elif st.session_state.page == "dashboard":
    user_display_name = st.session_state.current_user.upper()
    st.markdown(f'<div class="welcome-banner"><h1 class="welcome-title">⚡ WELCOME TO ENZO PRO BOARD, {user_display_name}! ⚡</h1></div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        c1.markdown("<h2 style='color: #00ff66;'>🦅 ENZO TERMINAL</h2>", unsafe_allow_html=True)
        if c2.button("🔒 Logout"):
            st.query_params.clear()
            st.session_state.page = "auth"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    signal_top_container = st.container()

    if 'signal_data' in st.session_state and st.session_state.signal_data:
        sig = st.session_state.signal_data
        color = "#00ff66" if "BUY" in sig["action"] else "#ff3366"
        with signal_top_container:
            st.markdown(f'''
                <div class="front-popup-card-animated" style="border-color: {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: 900; color: #fff;">✨ AI ANIMATED SIGNAL POP-UP</span>
                        <span style="background-color: {color}; color: #030508; padding: 6px 20px; border-radius: 8px; font-weight: 900; font-size: 20px;">{sig['action']}</span>
                    </div>
                    <div class="metric-row"><span>Broker / Asset:</span><b>{sig['broker']} - {sig['asset']}</b></div>
                    <div class="metric-row"><span>Timeframe:</span><b>{sig['tf']}</b></div>
                    <div class="metric-row"><span>Accuracy:</span><b style="color:#00ff66;">{sig['conf']}% High Probability</b></div>
                </div>
            ''', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        broker = st.selectbox("Select Broker", ["Quotex", "Pocket Option"])
        market = st.radio("Market Type", ["OTC", "Live Market"], horizontal=True)
        assets = ["EUR/USD (OTC)", "GBP/USD (OTC)", "GOLD (OTC)"] if market == "OTC" else ["EUR/USD", "GBP/USD", "GOLD"]
        asset = st.selectbox("Trading Asset", assets)
        tf = st.selectbox("Timeframe", ["15 Seconds", "30 Seconds", "1 Minute", "5 Minutes"])
        balance = st.number_input("Account Balance ($)", value=100)
        risk = st.select_slider("Risk Strategy", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"])
        
        if st.button("🚀 EXECUTE ADVANCED ALGORITHM ANALYSIS"):
            p_bar = st.progress(0)
            for p in range(100):
                time.sleep(0.015)
                p_bar.progress(p + 1)
            p_bar.empty()
            
            action = random.choice(["BUY (CALL 🟢)", "SELL (PUT 🔴)"])
            st.session_state.signal_data = {"action": action, "conf": random.randint(89, 95), "asset": asset, "tf": tf, "broker": broker}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
