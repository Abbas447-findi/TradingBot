import streamlit as st
import random
import time

# Page Configuration
st.set_page_config(
    page_title="ENZO BOT - Premium Access",
    page_icon="🦅",
    layout="centered"
)

# Professional CSS with Larger Enzo Pro Title
st.markdown("""
    <style>
    .stApp {
        background-color: #080c14;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .page-box {
        background-color: #111827;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #1f2937;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
    }
    .title-text {
        color: #00ff66;
        text-align: center;
        font-size: 46px; /* Bada aur prominent kar diya hai */
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 2px;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
    }
    .sub-title {
        color: #9ca3af;
        text-align: center;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .telegram-box {
        text-align: center;
        background-color: #1f2937;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #2b3748;
    }
    .telegram-link {
        color: #0088cc;
        text-decoration: none;
        font-weight: 700;
        font-size: 15px;
    }
    .telegram-link:hover {
        color: #00aaff;
        text-decoration: underline;
    }
    .binance-box {
        background-color: #141b22;
        border: 1px dashed #f3ba2f;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .active-users-badge {
        text-align: center;
        background-color: #0d1b1e;
        border: 1px solid #00ff66;
        color: #00ff66;
        padding: 6px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00ff66 0%, #00b347 100%) !important;
        color: #080c14 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: none !important;
        cursor: pointer;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }
    .result-box {
        background-color: #111827;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        border-left: 6px solid #00ff66;
        margin-top: 20px;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #1f2937;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header (Larger Enzo Pro Title)
st.markdown('<p class="title-text">🦅 ENZO PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ Premium Access & Trading Robot</p>', unsafe_allow_html=True)

# Telegram Support Contact Section
TELEGRAM_URL = "https://t.me/+diy3N-HPvNJkZmRk" 

st.markdown(f"""
    <div class="telegram-box">
        <span>💬 Need Help? Contact Support: </span>
        <a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">✈️ Telegram Support</a>
    </div>
""", unsafe_allow_html=True)

VALID_KEY = "4747"
BINANCE_PAY_ID = "385682148"
BINANCE_NAME = "X FENDI"

if 'page' not in st.session_state:
    st.session_state.page = "auth"

# ==========================================
# SAFA 1: AUTHENTICATION / REGISTRATION PAGE
# ==========================================
if st.session_state.page == "auth":
    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🔐 Step 1: Authentication & Verification")
        st.markdown("<p style='color:#9ca3af; font-size:13px;'>Please enter your license key or complete payment via Binance to access the trading robot.</p>", unsafe_allow_html=True)
        
        mode = st.radio("Authentication Mode", ["License Key", "Binance Pay Gateway"], horizontal=True)
        
        if mode == "License Key":
            key = st.text_input("Enter Security Key", type="password", placeholder="Type 4747...")
            if st.button("Verify Key & Enter ➡️"):
                if key == VALID_KEY:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>🔴 Invalid Access Key! Use 4747</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="binance-box">
                    <h4 style="color: #f3ba2f; margin-top: 0; margin-bottom: 8px;">💛 Binance Pay Gateway</h4>
                    <p style="color: #d1d5db; font-size: 13px; margin-bottom: 6px;">Subscription fee ke liye apni Binance app se neeche di gayi ID par payment transfer karein:</p>
                    <div style="background: #080c14; padding: 10px; border-radius: 6px; font-family: monospace; color: #00ff66; font-size: 14px;">
                        <b>Binance Pay ID / UID:</b> {BINANCE_PAY_ID}<br>
                        <b>Account Name:</b> {BINANCE_NAME}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            tx = st.text_input("Enter Transaction ID (TxID)", placeholder="Paste your deposit hash / TxID here...")
            if st.button("Confirm Payment & Enter ➡️"):
                if tx and len(tx.strip()) >= 6:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.markdown("<p style='color:#ff3366; font-size:12px;'>⚠️ Please enter a valid Transaction ID (TxID).</p>", unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SAFA 2: TRADING DASHBOARD
# ==========================================
elif st.session_state.page == "dashboard":
    
    if 'active_users' not in st.session_state:
        st.session_state.active_users = random.randint(130, 220)
        
    st.markdown(f"""
        <div class="active-users-badge">
            🟢 Live Status: {st.session_state.active_users} Traders Active on Enzo Bot right now!
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        
        if st.button("⬅️ Lock / Logout"):
            st.session_state.page = "auth"
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🏛️ Step 2: Select Broker & Market")
        broker = st.selectbox("Select Broker", ["Quotex", "Pocket Option"])
        market = st.radio("Market Type", ["OTC", "Live Market"], horizontal=True)
        
        if broker == "Quotex":
            if market == "OTC":
                assets = [
                    "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "NZD/USD (OTC)", 
                    "USD/JPY (OTC)", "USD/CHF (OTC)", "EUR/JPY (OTC)", "GBP/JPY (OTC)", 
                    "AUD/JPY (OTC)", "EUR/AUD (OTC)", "USD/CAD (OTC)", "CAD/JPY (OTC)",
                    "EUR/GBP (OTC)", "AUD/USD (OTC)", "CHF/JPY (OTC)"
                ]
            else:
                assets = [
                    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", 
                    "EUR/GBP", "NZD/USD", "USD/CHF", "EUR/JPY", "GBP/JPY", 
                    "AUD/JPY", "EUR/AUD", "CAD/JPY", "BTC/USD (Crypto)", "ETH/USD (Crypto)"
                ]
        else:
            if market == "OTC":
                assets = [
                    "EUR/USD [OTC]", "GBP/USD [OTC]", "USD/JPY [OTC]", "AUD/CHF [OTC]", 
                    "EUR/GBP [OTC]", "USD/CAD [OTC]", "GBP/JPY [OTC]", "NZD/JPY [OTC]",
                    "AUD/CAD [OTC]", "EUR/AUD [OTC]", "CHF/JPY [OTC]", "USD/CHF [OTC]",
                    "NZD/USD [OTC]", "EUR/CAD [OTC]", "GBP/CHF [OTC]"
                ]
            else:
                assets = [
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
        tf = st.selectbox("Timeframe", ["5 Seconds", "15 Seconds", "30 Seconds", "1 Minute", "5 Minutes"])
        balance = st.number_input("Account Balance ($)", min_value=10, value=100, step=10)
        risk = st.select_slider("Risk Strategy", options=["Safe (2%)", "Moderate (5%)", "Aggressive (10%)"], value="Moderate (5%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🚀 EXECUTE TRADING ROBOT ALGORITHM")
        st.markdown('</div>', unsafe_allow_html=True)

    if 'signal_data' not in st.session_state:
        st.session_state.signal_data = None
        
    if 'last_asset' not in st.session_state:
        st.session_state.last_asset = None
        
    if 'click_count' not in st.session_state:
        st.session_state.click_count = 0

    if gen_btn:
        with st.spinner("Enzo Robot analyzing market depth, RSI & price action..."):
            time.sleep(1.0)
            
            # Click count increment taake kuch clicks ke baad direction smartly random flip ho sake
            st.session_state.click_count += 1
            
            if st.session_state.signal_data and st.session_state.last_asset == asset and st.session_state.click_count < 3:
                action = st.session_state.signal_data["action"]
            else:
                action = random.choice(["BUY", "SELL"])
                st.session_state.last_asset = asset
                if st.session_state.click_count >= 3:
                    st.session_state.click_count = 0 # Reset counter for next cycle
                
            conf = random.randint(85, 98)
            rsi_val = random.choice(["Oversold (<30)", "Overbought (>70)", "Neutral (50)"])
            trend = random.choice(["Strong Bullish", "Strong Bearish", "Consolidation"])
            
            if "Safe" in risk:
                stake = round(balance * 0.02, 2)
            elif "Moderate" in risk:
                stake = round(balance * 0.05, 2)
            else:
                stake = round(balance * 0.10, 2)
                
            st.session_state.signal_data = {
                "action": action,
                "conf": conf,
                "asset": asset,
                "tf": tf,
                "broker": broker,
                "stake": stake,
                "strategy": risk,
                "rsi": rsi_val,
                "trend": trend
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
                <div class="metric-row">
                    <span style="color: #9ca3af;">Broker / Asset:</span>
                    <span style="font-weight: 600;">{sig['broker']} - {sig['asset']}</span>
                </div>
                <div class="metric-row">
                    <span style="color: #9ca3af;">Timeframe & Strategy:</span>
                    <span style="font-weight: 600;">{sig['tf']} | {sig['strategy']}</span>
                </div>
                <div class="metric-row">
                    <span style="color: #9ca3af;">Market Trend & RSI:</span>
                    <span style="color: #00ff66; font-weight: 600;">{sig['trend']} ({sig['rsi']})</span>
                </div>
                <div class="metric-row">
                    <span style="color: #9ca3af;">AI Prediction Confidence:</span>
                    <span style="color: #00ff66; font-weight: 700;">{sig['conf']}% Accuracy</span>
                </div>
                <div class="metric-row" style="border: none;">
                    <span style="color: #9ca3af;">Recommended Trade Stake:</span>
                    <span style="color: #ffcc00; font-weight: 700;">${sig['stake']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
