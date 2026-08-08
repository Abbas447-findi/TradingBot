import streamlit as st
import random
import time

# Page Configuration for Dark Mobile-like Layout
st.set_page_config(page_title="Tokio Edge", layout="centered")

# Custom Dark Theme CSS matching Tokio Edge Style
st.markdown("""
    <style>
    .stApp {
        background-color: #0b131b;
        color: #ffffff;
    }
    .header-card {
        background-color: #121e2b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1f3348;
        text-align: center;
        margin-bottom: 20px;
    }
    .intro-card {
        background-color: #121e2b;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #1f3348;
        text-align: center;
        margin-top: 30px;
    }
    .stats-card {
        background-color: #121e2b;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #1f3348;
        text-align: center;
        margin-bottom: 20px;
        font-size: 14px;
        color: #8da2b5;
    }
    .call-box {
        padding: 22px;
        border-radius: 12px;
        background-color: #132f22;
        border: 2px solid #28a745;
        color: #5fff88;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .put-box {
        padding: 22px;
        border-radius: 12px;
        background-color: #3b181c;
        border: 2px solid #dc3545;
        color: #ff7b88;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .telegram-btn {
        display: inline-flex;
        align-items: center;
        background-color: #229ed9;
        color: white !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: bold;
        text-decoration: none;
        margin-top: 10px;
        border: 1px solid #1782b5;
    }
    .telegram-btn:hover {
        background-color: #1f8ec4;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization for multi-step flow
if 'step' not in st.session_state:
    st.session_state.step = "intro"

if 'is_authorized' not in st.session_state:
    st.session_state.is_authorized = False

if 'selected_broker' not in st.session_state:
    st.session_state.selected_broker = None

if 'selected_pair' not in st.session_state:
    st.session_state.selected_pair = None

# Random active traders counter for live feel
active_traders = random.randint(110, 155)

# --- STEP 1: CLASSIC INTRO SCREEN ---
if st.session_state.step == "intro":
    st.markdown("""
        <div class="intro-card">
            <h1 style="color: #00ffcc; font-size: 38px; margin-bottom: 10px;">Tokio Edge</h1>
            <p style="color: #8da2b5; font-size: 18px; margin-bottom: 30px;">Binary Options Trading Robot</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="stats-card">
            🟢 System Status: <b style="color: #5fff88;">ONLINE</b> &nbsp;&nbsp;|&nbsp;&nbsp; 👥 Active Traders: <b style="color: #00ffcc;">{active_traders} Online</b>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 LAUNCH ROBOT", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.015)
            progress_bar.progress(i + 1)
            if i == 30:
                status_text.text("Booting Tokio Edge core engine...")
            elif i == 70:
                status_text.text("Establishing secure portal connection...")
                
        time.sleep(0.5)
        st.session_state.step = "security"
        st.rerun()

# --- STEP 2: SECURITY VERIFICATION ---
elif st.session_state.step == "security":
    if st.button("⬅️ Back to Intro"):
        st.session_state.step = "intro"
        st.rerun()
        
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <h2 style="color: #00ffcc; margin: 0;">Tokio Edge</h2>
            <span style="background-color: #121e2b; padding: 5px 12px; border-radius: 20px; color: #00ffcc; font-size: 14px; border: 1px solid #1f3348;">SECURE PORTAL</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🔐 Access Verification Required")
    st.write("Please enter your **License Key** to unlock the Tokio Edge robot:")
    
    tab1, tab2 = st.tabs(["💎 Paid Subscription", "🤝 Free Access via Referral"])
    
    with tab1:
        key_input = st.text_input("Verify License Key", type="password")
        if st.button("Verify Key"):
            valid_keys = ["TOKIO-8821", "EDGE-9943", "OTC-5562", "VIP-7714", "PRO-3329", "4747"]
            
            if key_input in valid_keys:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    time.sleep(0.015)
                    progress_bar.progress(i + 1)
                    if i == 40:
                        status_text.text("Validating unique license key...")
                    elif i == 80:
                        status_text.text("Access granted! Loading brokers...")
                        
                time.sleep(0.5)
                st.session_state.is_authorized = True
                st.session_state.step = "broker"
                st.rerun()
            else:
                st.error("Invalid License Key. Please contact official support.")
                
    with tab2:
        st.markdown("1. Create your account using our official partner link: [Click Here](https://broker-link.com/register?ref=tokioedge)")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("2. For **Official Support & Contact** (Send your Trade ID here):")
        
        st.markdown('''
            <div>
                <a href="https://t.me/+LD-j3-_Xiak1M2Zk" target="_blank" class="telegram-btn">
                    📱 &nbsp; Telegram Official Support
                </a>
            </div>
        ''', unsafe_allow_html=True)

# --- STEP 3 & 4: BROKER & PAIR SELECTION / TRADING ROBOT ---
else:
    # Top Bar Header
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <h2 style="color: #00ffcc; margin: 0;">Tokio Edge</h2>
            <span style="background-color: #121e2b; padding: 5px 12px; border-radius: 20px; color: #00ffcc; font-size: 14px; border: 1px solid #1f3348;">SYSTEM ACTIVE</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Step 3: Choose Broker (Side-by-side in a Row)
    if st.session_state.selected_broker is None:
        if st.button("⬅️ Back to Security"):
            st.session_state.step = "security"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌐 Select Your Trading Platform")
        st.write("Choose the broker you want to trade on:")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.markdown("""
                <style>
                div.stButton > button:nth-of-type(1) {
                    background-color: #ffffff !important;
                    color: #dc3545 !important;
                    border: 2px solid #dc3545 !important;
                    font-weight: bold !important;
                }
                </style>
            """, unsafe_allow_html=True)
            if st.button("🔴 Quotex", use_container_width=True):
                st.session_state.selected_broker = "Quotex"
                st.rerun()
                
        with col_b2:
            st.markdown("""
                <style>
                div.stButton > button:nth-of-type(2) {
                    background-color: #007bff !important;
                    color: #ffffff !important;
                    border: 2px solid #0056b3 !important;
                    font-weight: bold !important;
                }
                </style>
            """, unsafe_allow_html=True)
            if st.button("🔵 Pocket Option", use_container_width=True):
                st.session_state.selected_broker = "Pocket Option"
                st.rerun()
                
    # Step 4: Choose Pair based on Broker
    elif st.session_state.selected_pair is None:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin:0;">Active Platform: <span style="color: #00ffcc;">{st.session_state.selected_broker}</span></h3>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬅️ Change Platform"):
            st.session_state.selected_broker = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Select Currency / OTC Pair")
        
        search_query = st.text_input("🔍 Search pairs...", "")
        
        # Define pairs depending on the broker selected
        if st.session_state.selected_broker == "Quotex":
            pairs_list = [
                "EUR/USD OTC", "GBP/USD OTC", "AUD/USD OTC", "USD/JPY OTC",
                "EUR/GBP OTC", "USD/CAD OTC", "NZD/USD OTC", "EUR/JPY OTC",
                "GBP/JPY OTC", "AUD/JPY OTC", "CHF/JPY OTC", "BTC/USD OTC"
            ]
        else: # Pocket Option pairs
            pairs_list = [
                "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/CHF (OTC)", "EUR/JPY (OTC)",
                "AUD/CAD (OTC)", "EUR/CAD (OTC)", "GBP/AUD (OTC)", "AUD/NZD (OTC)",
                "NZD/JPY (OTC)", "CAD/JPY (OTC)", "USD/INR (OTC)", "Crypto Index OTC"
            ]
            
        filtered_pairs = [p for p in pairs_list if search_query.lower() in p.lower()]
        
        cols = st.columns(2)
        for idx, pair in enumerate(filtered_pairs):
            with cols[idx % 2]:
                if st.button(f"📊 {pair}", key=f"btn_{pair}", use_container_width=True):
                    st.session_state.selected_pair = pair
                    st.rerun()

    # Step 5: Signal Generation Dashboard with Timeframes
    else:
        random_accuracy = random.randint(82, 97)
        
        st.markdown(f"""
            <div class="header-card">
                <p style="color: #00ffcc; margin:0; font-size:14px;">Platform: {st.session_state.selected_broker}</p>
                <h3>Active Asset: <span style="color: #00ffcc;">{st.session_state.selected_pair}</span></h3>
                <p style="color: #8da2b5; margin: 0;">Volatility: <b style="color: #00ffcc;">OPTIMAL</b> &nbsp;&nbsp;|&nbsp;&nbsp; Accuracy: <b style="color: #00ffcc;">{random_accuracy}%</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬅️ BACK TO PAIRS", use_container_width=True):
            st.session_state.selected_pair = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Timeframe Selector Added Here
        st.markdown("### ⏱️ Select Expiry Timeframe")
        timeframe = st.selectbox("Choose timeframe:", ["30 Seconds", "1 Minute", "2 Minutes", "5 Minutes"], label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 GENERATE SIGNAL NOW", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                time.sleep(0.020)
                progress_bar.progress(i + 1)
                if i == 20:
                    status_text.text(f"Connecting to {st.session_state.selected_broker} feed...")
                elif i == 50:
                    status_text.text(f"Analyzing {timeframe} candle momentum...")
                elif i == 80:
                    status_text.text("Calculating Support & Resistance levels...")
                    
            status_text.empty()
            progress_bar.empty()
            
            dummy_price = round(random.uniform(1.0500, 1.1500), 4)
            support = round(dummy_price - 0.0015, 4)
            resistance = round(dummy_price + 0.0015, 4)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Price", f"{dummy_price}")
            c2.metric("Support", f"{support}")
            c3.metric("Resistance", f"{resistance}")
            
            st.markdown(f"<p style='color: #8da2b5; text-align: center; margin-top: 10px;'>Expiry Timeframe: <b style='color: #00ffcc;'>{timeframe}</b></p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            signal = random.choice(["CALL", "PUT"])
            
            if signal == "CALL":
                st.markdown(f'''
                    <div class="call-box">
                        🟢 CALL (UP) SIGNAL<br>
                        <span style="font-size:14px; color:#a3ffb8; font-weight:normal;">Price is at Support level. Strong upward momentum ({timeframe}).</span>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="put-box">
                        🔴 PUT (DOWN) SIGNAL<br>
                        <span style="font-size:14px; color:#ffb0b8; font-weight:normal;">Price is at Resistance level. Downward reversal expected ({timeframe}).</span>
                    </div>
                ''', unsafe_allow_html=True)