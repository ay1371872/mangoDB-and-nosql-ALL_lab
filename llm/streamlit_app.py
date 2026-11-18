"""Streamlit Interactive Threat Intelligence & Autonomous Remediation Frontend
Synthesizes Appendix A.5 with real-time Threat Intelligence, RAG Chat, and Bot Controls.
Student: Ayush Yadav (USN: 24BTLCL003) | Course: 23CSE528 NoSQL Databases using MongoDB
"""

import os
import requests
import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page layout
st.set_page_config(
    page_title="Threat Intel AI | MongoDB NoSQL",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- Custom Styling ---
st.markdown("""
<style>
    .main-header { font-size: 28px; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 15px; color: #4B5563; margin-bottom: 15px; }
    .metric-card { background-color: #F3F4F6; border-radius: 8px; padding: 12px; border-left: 4px solid #1E3A8A; }
    .threat-tag-active { background-color: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
    .threat-tag-anticip { background-color: #FEF3C7; color: #92400E; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
    .threat-tag-evolve { background-color: #F3E8FF; color: #6B21A8; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
    .threat-tag-resolved { background-color: #D1FAE5; color: #065F46; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
</style>
""", unsafe_allow_html=True)


# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am your **Threat Intelligence AI Assistant**, powered by **MongoDB Atlas Vector Search** "
                "and synthetic RAG. I track **Anticipated**, **Active**, **Evolving**, and **Resolved** threats "
                "across **Linux, Windows, macOS, Android, and iOS**.\n\n"
                "Ask me about any security advisory, request mitigation scripts, or ask the background bot to scan your machine!"
            )
        }
    ]

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-ayush-{int(datetime.utcnow().timestamp())}"


# --- Header ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<div class="main-header">🛡️ Threat Intelligence AI Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">JAIN University • 23CSE528 NoSQL Databases using MongoDB • Ayush Yadav (24BTLCL003)</div>', unsafe_allow_html=True)
with col_head2:
    st.caption(f"**Session:** `{st.session_state.session_id[:18]}...`")


# --- Fetch Backend Diagnostics ---
backend_online = False
health_data = {}
try:
    resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
    if resp.status_code == 200:
        backend_online = True
        health_data = resp.json()
except Exception:
    backend_online = False


# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Platform Controls")
    
    # Status indicator
    if backend_online:
        st.success(f"🟢 Backend Online ({health_data.get('llm_backend', 'SLM')})")
        st.caption(f"Database: {health_data.get('mongo_status', 'Unknown')}")
    else:
        st.error("🔴 Backend Offline (Start `threat_intel_api.py`)")

    st.markdown("---")
    st.subheader("🔍 Threat Filters")
    platform_choice = st.selectbox("Target Platform", ["All", "Windows", "Linux", "macOS", "Android", "iOS"])
    status_choice = st.selectbox("Threat Status", ["All", "Active", "Anticipated", "Evolving", "Resolved"])

    st.markdown("---")
    st.subheader("🤖 Autonomous Scanner Bot")
    st.info("The background daemon audits listening ports and operating system exposures.")
    
    if st.button("🚀 Run System Vulnerability Scan", use_container_width=True):
        if backend_online:
            with st.spinner("Bot auditing system telemetry and network ports..."):
                try:
                    s_resp = requests.post(f"{BACKEND_URL}/scan", json={}, timeout=15)
                    if s_resp.status_code == 200:
                        s_data = s_resp.json()
                        st.success(f"Audit Complete! Host: {s_data.get('host')}")
                        st.write(f"• Open Ports: `{s_data.get('open_ports')}`")
                        st.write(f"• Vulnerabilities: `{len(s_data.get('vulnerabilities_detected', []))}`")
                        st.rerun()
                except Exception as ex:
                    st.error(f"Scan failed: {ex}")
        else:
            st.warning("Backend must be running to execute scan.")

    if st.button("⚡ Feed 100,000 Parameters to DB", use_container_width=True):
        if backend_online:
            with st.spinner("Ingesting 100,000 threat parameters into MongoDB (Bulk Operations)..."):
                try:
                    f_res = requests.post(f"{BACKEND_URL}/feed-100k", timeout=180)
                    if f_res.status_code == 200:
                        d = f_res.json()
                        st.success(f"✅ Ingested {d.get('parameters_fed', 100000):,} parameters in {d.get('elapsed_seconds')}s! Throughput: {d.get('throughput'):,.0f} docs/sec")
                        st.rerun()
                except Exception as ex:
                    st.error(f"Ingestion error: {ex}")
        else:
            st.warning("Backend required.")

    if st.button("🔄 Reset / Re-seed Intelligence DB", use_container_width=True):
        import subprocess
        subprocess.run(["python", "seed_threat_data.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        st.success("MongoDB Threat collection re-seeded!")
        st.rerun()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --- Real-Time Analytics Banner (Exercise 5 Aggregation) ---
stats_data = {"categories": {"Anticipated": 0, "Active": 0, "Evolving": 0, "Resolved": 0}, "total_threats": 0}
if backend_online:
    try:
        s_res = requests.get(f"{BACKEND_URL}/stats", timeout=3)
        if s_res.status_code == 200:
            stats_data = s_res.json()
    except Exception:
        pass

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Total Threats", stats_data.get("total_threats", 0))
m2.metric("🔴 Active", stats_data["categories"].get("Active", 0))
m3.metric("🟡 Anticipated", stats_data["categories"].get("Anticipated", 0))
m4.metric("🟣 Evolving", stats_data["categories"].get("Evolving", 0))
m5.metric("🟢 Resolved", stats_data["categories"].get("Resolved", 0))
param_count_display = health_data.get("telemetry_parameters_count", 0)
m6.metric("⚡ 100K Telemetry", f"{param_count_display:,}" if param_count_display else "0")

st.markdown("---")


# --- Main Tabs ---
tab_chat, tab_matrix, tab_bot, tab_100k = st.tabs([
    "💬 Conversational Threat AI",
    "📊 Threat Intelligence Matrix",
    "🤖 Scanner Bot & Audit Trail",
    "⚡ 100K Scale Telemetry"
])


# === TAB 1: Conversational Chat ===
with tab_chat:
    # Example Prompt Quick Buttons
    st.caption("Quick Queries:")
    c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
    quick_prompt = None
    if c_btn1.button("🔴 Active Windows Threats", use_container_width=True):
        quick_prompt = "What are the Active threats currently affecting Windows?"
    if c_btn2.button("🟣 Evolving Linux Exploits", use_container_width=True):
        quick_prompt = "List evolving Linux kernel privilege escalation threats."
    if c_btn3.button("🟡 Anticipated Zero-Days", use_container_width=True):
        quick_prompt = "What are the anticipated zero-days across Android and iOS?"
    if c_btn4.button("⚡ Mitigate CVE-2024-21413", use_container_width=True):
        quick_prompt = "Mitigate CVE-2024-21413 on my system immediately."

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📚 Retrieved MongoDB Threat Records ({len(msg['sources'])})"):
                    for s in msg["sources"]:
                        st.markdown(f"**[{s.get('cve_id')}] {s.get('title')}** | Platform: `{s.get('platform')}` | CVSS: `{s.get('cvss')}` (RAG Score: `{s.get('score', 0):.4f}`)")
                        st.caption(f"Procedure: {s.get('mitigation_procedure')[:130]}...")

    # Chat Input
    user_query = st.chat_input("Ask about CVEs, platform vulnerabilities, or type 'mitigate CVE-XXXX'...")
    final_input = quick_prompt if quick_prompt else user_query

    if final_input:
        st.session_state.messages.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.markdown(final_input)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving MongoDB Threat Context & Synthesizing Advisory..."):
                if backend_online:
                    try:
                        chat_payload = {
                            "session_id": st.session_state.session_id,
                            "message": final_input,
                            "platform": None if platform_choice == "All" else platform_choice,
                            "status": None if status_choice == "All" else status_choice
                        }
                        c_res = requests.post(f"{BACKEND_URL}/chat", json=chat_payload, timeout=60)
                        if c_res.status_code == 200:
                            data = c_res.json()
                            st.markdown(data["response"])
                            sources = data.get("sources", [])
                            if sources:
                                with st.expander(f"📚 Grounded MongoDB Threat Context ({len(sources)} items)"):
                                    for s in sources:
                                        st.write(f"- **{s.get('cve_id')}**: {s.get('title')} (Platform: {s.get('platform')}, CVSS: {s.get('cvss')})")
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": data["response"],
                                "sources": sources
                            })
                        else:
                            st.error(f"Backend returned HTTP {c_res.status_code}: {c_res.text}")
                    except Exception as err:
                        st.error(f"Communication error: {err}")
                else:
                    st.error("Backend offline. Please start `threat_intel_api.py` first.")


# === TAB 2: Threat Matrix & 1-Click Interactive Mitigation ===
with tab_matrix:
    st.subheader("📋 Operational Threat Matrix")
    
    if backend_online:
        t_params = {}
        if platform_choice != "All":
            t_params["platform"] = platform_choice
        if status_choice != "All":
            t_params["status"] = status_choice

        try:
            t_res = requests.get(f"{BACKEND_URL}/threats", params=t_params, timeout=5)
            threats_list = t_res.json().get("threats", [])
            
            if threats_list:
                for t in threats_list:
                    with st.container():
                        col_cve, col_info, col_act = st.columns([2, 5, 2])
                        with col_cve:
                            st.markdown(f"### `{t['cve_id']}`")
                            st.caption(f"Platform: **{t['platform']}** | CVSS: **{t['cvss']}**")
                            # Status badge
                            status = t["status"]
                            badge_cls = {
                                "Active": "threat-tag-active",
                                "Anticipated": "threat-tag-anticip",
                                "Evolving": "threat-tag-evolve",
                                "Resolved": "threat-tag-resolved"
                            }.get(status, "threat-tag-active")
                            st.markdown(f'<span class="{badge_cls}">{status.upper()}</span>', unsafe_allow_html=True)

                        with col_info:
                            st.markdown(f"**{t['title']}**")
                            st.write(t["description"])
                            with st.expander("🛠️ Mitigation Procedure & Command"):
                                st.markdown(f"**Procedure:** {t['mitigation_procedure']}")
                                if t.get("automated_fix_command"):
                                    st.code(t["automated_fix_command"], language="bash")
                                if t.get("mitigated_at"):
                                    st.success(f"Mitigated At: {t['mitigated_at']}")

                        with col_act:
                            if t["status"] in ["Active", "Evolving"]:
                                if st.button(f"⚡ Mitigate", key=f"mit_{t['cve_id']}", use_container_width=True):
                                    with st.spinner("Applying mitigation transaction in MongoDB..."):
                                        m_req = requests.post(
                                            f"{BACKEND_URL}/mitigate",
                                            json={"cve_id": t["cve_id"], "confirm": True, "operator": "Ayush Yadav"},
                                            timeout=10
                                        )
                                        if m_req.status_code == 200:
                                            st.toast(f"✅ {t['cve_id']} successfully mitigated!", icon="🛡️")
                                            st.rerun()
                                        else:
                                            st.error("Mitigation failed.")
                            else:
                                st.button("✅ Resolved", key=f"res_{t['cve_id']}", disabled=True, use_container_width=True)

                        st.divider()
            else:
                st.info("No threats found matching current filter.")
        except Exception as ex:
            st.error(f"Error loading threats: {ex}")
    else:
        st.warning("Connect backend to view live threat matrix.")


# === TAB 3: Scanner Bot & Audit Trail ===
with tab_bot:
    st.subheader("🤖 Background Vulnerability Scanner & Diagnostics")
    
    col_host1, col_host2 = st.columns(2)
    with col_host1:
        st.markdown("#### 💻 Local Host Status")
        import socket, platform as py_plat
        st.write(f"- **Operating System:** `{py_plat.system()} {py_plat.release()}`")
        st.write(f"- **Host Architecture:** `{py_plat.machine()}`")
        st.write(f"- **Host Machine Name:** `{socket.gethostname()}`")
    with col_host2:
        st.markdown("#### 🔒 Security Enforcement Policy")
        st.write("- **Database Storage:** `MongoDB Atlas / Local NoSQL`")
        st.write("- **Consistency Level:** `w:majority (ACID Transactional Auditing)`")
        st.write("- **Vector Indexing:** `384-dimensional HNSW Cosine Vectors`")

    st.markdown("---")
    st.subheader("📜 System Audit Trail (MongoDB `audit_log`)")
    if backend_online:
        try:
            a_res = requests.get(f"{BACKEND_URL}/audit", timeout=5)
            logs = a_res.json().get("audit_logs", [])
            if logs:
                df_logs = pd.DataFrame(logs)
                st.dataframe(df_logs, use_container_width=True)
            else:
                st.info("No audit logs recorded yet.")
        except Exception as ex:
            st.error(f"Failed to fetch audit trail: {ex}")


# === TAB 4: 100,000 Parameter High-Scale Telemetry ===
with tab_100k:
    st.subheader("⚡ 100,000 Security Parameter Ingestion & Analytics")
    st.markdown(
        "Demonstrates high-throughput bulk insertion, compound indexing (`IXSCAN`), "
        "and multi-stage aggregation pipelines over **100,000 structured cyber parameters** in MongoDB (Exercises 5, 6 & 7)."
    )

    if backend_online:
        try:
            p_res = requests.get(f"{BACKEND_URL}/parameters/stats", timeout=5)
            p_data = p_res.json()
            
            p_total = p_data.get("total_parameters", 0)
            if p_total > 0:
                p_c1, p_c2, p_c3 = st.columns(3)
                p_c1.metric("Total Parameters Stored", f"{p_total:,}")
                p_c2.metric("🚨 Anomalies Detected", f"{p_data.get('anomalous_parameters', 0):,}")
                p_c3.metric("🛡️ Normal Parameters", f"{p_data.get('normal_parameters', 0):,}")

                st.markdown("#### 📊 Platform Distribution of 100,000 Parameters")
                dist = p_data.get("platform_distribution", {})
                if dist:
                    df_dist = pd.DataFrame(list(dist.items()), columns=["Platform", "Parameter Count"])
                    st.bar_chart(df_dist.set_index("Platform"))

                st.markdown("#### ⚡ Active Compound Indexes")
                st.code(
                    "- db.threat_parameters.createIndex({ platform: 1, threat_status: 1, is_anomaly: 1 })\n"
                    "- db.threat_parameters.createIndex({ severity: 1, cvss_score: -1 })\n"
                    "- db.threat_parameters.createIndex({ param_id: 1 }, { unique: true })",
                    language="javascript"
                )
            else:
                st.info("No parameters loaded yet. Click the button below to feed 100,000 parameters into MongoDB.")
                if st.button("🚀 Ingest 100,000 Parameters Now"):
                    with st.spinner("Ingesting 100,000 records into MongoDB..."):
                        requests.post(f"{BACKEND_URL}/feed-100k", timeout=180)
                        st.success("Successfully ingested 100,000 parameters!")
                        st.rerun()
        except Exception as ex:
            st.error(f"Failed to fetch parameter telemetry: {ex}")
    else:
        st.warning("Backend required to inspect 100k telemetry.")
