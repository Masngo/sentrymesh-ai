import streamlit as st
import requests
import json
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="SentryMesh AI | Command Center",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SentryMesh AI Command Center")
st.caption("Autonomous Self-Healing & Multi-Agent Incident Response Engine (Nebius x NVIDIA)")

st.sidebar.header("Nebius System Status")
st.sidebar.success("Engine: Nebius Token Factory")
st.sidebar.info("Agents: Nemotron-3 Nano & Nemotron-3 Ultra")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚨 Trigger Simulated Incident")
    service = st.text_input("Service Name", "payment-processor-v2")
    severity = st.selectbox("Severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=3)
    raw_logs = st.text_area("Raw Incident Logs", "ERROR 2026-10-23 21:00:12 [db_pool]: Connection pool exhausted. Max limit 50 reached.")
    stack_trace = st.text_area("Stack Trace", "sqlalchemy.exc.TimeoutError: QueuePool limit of size 50 overflow 10 reached, connection timed out.")

    if st.button("⚡ Dispatch SentryMesh Agents", type="primary"):
        payload = {
            "service_name": service,
            "severity": severity,
            "raw_logs": raw_logs,
            "stack_trace": stack_trace
        }
        with st.spinner("Nemotron Agents triaging and formulating code patch..."):
            try:
                res = requests.post(f"{BACKEND_URL}/api/v1/incident/resolve", json=payload)
                if res.status_code == 200:
                    st.session_state["result"] = res.json()
                else:
                    st.error(f"Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with col2:
    st.subheader("🤖 Multi-Agent Response Telemetry")
    if "result" in st.session_state:
        data = st.session_state["result"]
        st.success(f"Incident {data['incident_id']} Resolved in {data['execution_time_seconds']}s")
        
        st.markdown("### 🔍 Triage Agent (Nemotron-3 Nano)")
        st.json(data["triage"])
        
        st.markdown("### 🛠️ Remediation Agent (Nemotron-3 Ultra)")
        st.markdown(f"**Root Cause:** {data['remediation']['root_cause_explanation']}")
        st.code(data['remediation']['code_patch'], language="python")
        st.markdown("**Verification Steps:**")
        for step in data['remediation']['verification_steps']:
            st.markdown(f"- {step}")
    else:
        st.info("Submit an incident log on the left to observe real-time agentic triage and patching.")
