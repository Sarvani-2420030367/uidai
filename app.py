import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from auth import login
from roles import filter_data_by_role
from audit import log_action
from blockchain import generate_block_hash

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Enhanced UIDAI Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# LOGIN CHECK
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

user = st.session_state.user

# -----------------------
# SESSION STATE INIT
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "bg_color" not in st.session_state:
    st.session_state.bg_color = "#0d0c0c"

# -----------------------
# DATA LOAD (CACHED)
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("enhanced_uidai_risk_registry.csv")

df = load_data()
df = filter_data_by_role(df, user)

# -----------------------
# SIDEBAR SETTINGS
# -----------------------
st.sidebar.header("🎨 Appearance")
st.session_state.bg_color = st.sidebar.color_picker(
    "Choose Background Color",
    st.session_state.bg_color
)

# -----------------------
# SIDEBAR NAVIGATION (FIXED)
# -----------------------
menu_options = ["Dashboard", "Alerts", "Blockchain Audit", "Audit Logs", "Support"]

menu = st.sidebar.radio(
    "Navigation",
    menu_options,
    index=menu_options.index(st.session_state.page),
    key="nav_menu"
)

if st.session_state.page != st.session_state.nav_menu:
    st.session_state.page = st.session_state.nav_menu

# -----------------------
# GLOBAL STYLING
# -----------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {st.session_state.bg_color};
}}

.card {{
    background: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    text-align: center;
}}

.metric-title {{
    font-size: 18px;
    font-weight: 600;
    color: purple;
}}

.metric-value {{
    font-size: 28px;
    font-weight: bold;
    color: black;
}}

#floating-chat-btn button {{
    position: fixed;
    bottom: 25px;
    right: 25px;
    width: 60px !important;
    height: 60px !important;
    border-radius: 50% !important;
    font-size: 26px !important;
    background-color: #0d6efd !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35) !important;
    border: none !important;
    cursor: pointer;
    z-index: 999999;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# DASHBOARD
# -----------------------
if st.session_state.page == "Dashboard":
    st.title("🆔 Enhanced UIDAI Duplicate Risk Intelligence System")

    state = st.selectbox("State", df["state"].unique())
    districts = df[df["state"] == state]["district"].unique()

    if len(districts) == 0:
        st.warning("No districts available")
        st.stop()

    district = st.selectbox("District", districts)

    data = df[(df["state"] == state) & (df["district"] == district)]
    if data.empty:
        st.warning("No data available")
        st.stop()

    row = data.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"""
    <div class="card">
        <div class="metric-title">Enrollments</div>
        <div class="metric-value">{int(row["enrollments"])}</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
        <div class="metric-title">Demographic Updates</div>
        <div class="metric-value">{int(row["demo_updates"])}</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
        <div class="metric-title">Biometric Updates</div>
        <div class="metric-value">{int(row["bio_updates"])}</div>
    </div>
    """, unsafe_allow_html=True)

    c4.markdown(f"""
    <div class="card">
        <div class="metric-title">Risk Score</div>
        <div class="metric-value">{round(row["risk_score"], 2)}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if row["risk_level"] == "High":
        st.error("🚨 HIGH DUPLICATE RISK")
    elif row["risk_level"] == "Medium":
        st.warning("⚠️ MEDIUM DUPLICATE RISK")
    else:
        st.success("✅ LOW RISK")

    st.subheader("🔗 Blockchain Audit Proof")
    st.code(generate_block_hash(row))

    log_action(user["username"], f"Viewed {state} - {district}")
    
# -----------------------
# ALERTS
# -----------------------
elif st.session_state.page == "Alerts":
    st.header("🚨 High-Risk District Alerts")
    high = df[df["risk_level"] == "High"]
    if high.empty:
        st.success("No high-risk districts")
    else:
        st.dataframe(high[["state", "district", "risk_score"]])

# -----------------------
# BLOCKCHAIN AUDIT
# -----------------------
elif st.session_state.page == "Blockchain Audit":
    st.header("🔗 Blockchain Integrity Records")
    audit_df = df.copy()
    audit_df["block_hash"] = audit_df.apply(generate_block_hash, axis=1)
    st.dataframe(audit_df[["state", "district", "risk_level", "block_hash"]])

# -----------------------
# AUDIT LOGS
# -----------------------
elif st.session_state.page == "Audit Logs":
    st.header("📜 System Audit Logs")
    try:
        with open("audit_log.txt") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.info("No audit logs found")

# -----------------------
# SUPPORT (AI ASSISTANT)
# -----------------------
# -----------------------
elif st.session_state.page == "Support":
    st.header("🤖 UIDAI AI Assistant")
    st.markdown("Ask questions about risks, alerts, audits, or blockchain verification.")

    components.html("""
    <div style="width:100%;height:420px;">
        <iframe srcdoc='
        <html>
        <body>
        <div style="display:flex;flex-direction:column;height:100%;font-family:Arial,sans-serif;">
            <div style="background:#0d6efd;color:white;padding:12px;border-radius:8px 8px 0 0;font-weight:bold;">🤖 UIDAI AI Assistant</div>
            <div id="chat-body" style="flex:1;padding:10px;overflow-y:auto;font-size:14px;color:white">
                <p><b>AI:</b> Hi 👋 How can I help you?</p>
            </div>
            <div style="display:flex;border-top:1px solid #ddd;">
                <input type="text" id="msg" placeholder="Ask something..." style="flex:1;padding:8px;border:none;outline:none;">
                <button onclick="sendMsg()" style="padding:8px 12px;border:none;background:#0d6efd;color:white;cursor:pointer;">Send</button>
            </div>
        </div>
        <script>
        function sendMsg() {
            var input = document.getElementById("msg");
            var body = document.getElementById("chat-body");
            if(input.value.trim()==="") return;
            body.innerHTML += "<p><b>You:</b> " + input.value + "</p>";
            body.innerHTML += "<p><b>AI:</b> I can help explain risks, alerts, audits, and blockchain verification.</p>";
            body.scrollTop = body.scrollHeight;
            input.value="";
        }
        </script>
        </body>
        </html>'
        style="width:100%;height:100%;border:none;border-radius:15px;"></iframe>
    </div>
    """, height=450)


# -----------------------
# SIDEBAR ALERT SUMMARY
# -----------------------
st.sidebar.header("🚨 Alerts Summary")
count = len(df[df["risk_level"] == "High"])
if count:
    st.sidebar.error(f"{count} High-Risk District(s)")
else:
    st.sidebar.success("No High-Risk Districts")

# -----------------------
# FLOATING CHAT BUTTON (ONE CLICK FIXED)
# -----------------------
def open_support():
    st.session_state.page = "Support"
    st.session_state.nav_menu = "Support"

st.button("💬", key="floating_chat_btn", on_click=open_support)
