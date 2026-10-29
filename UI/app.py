import os
import sys
import time
import threading
import importlib

import requests
import streamlit as st
import uvicorn

st.set_page_config(
    page_title="SentryMesh AI - Command Center",
    page_icon="🛡️",
    layout="wide"
)

# Make the repo root importable (UI/app.py -> repo root)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

API_URL = "http://127.0.0.1:8000"

# Candidate locations of your FastAPI `app` object. Edit to match your repo.
BACKEND_CANDIDATES = [
    "server.main",
]


def start_backend():
    fastapi_app = None
    for module_path in BACKEND_CANDIDATES:
        try:
            module = importlib.import_module(module_path)
            fastapi_app = getattr(module, "app")
            break
        except (ImportError, AttributeError):
            continue
    if fastapi_app is None:
        return False, "Could not find the FastAPI app. Update BACKEND_CANDIDATES."

    config = uvicorn.Config(fastapi_app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run, daemon=True).start()

    # Wait up to ~10s for the server to accept connections
    for _ in range(20):
        try:
            requests.get(API_URL + "/docs", timeout=1)
            return True, "ok"
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False, "Backend started but did not respond in time."


backend_ok, backend_msg = start_backend()
if not backend_ok:
    st.error(f"Backend failed to start: {backend_msg}")

st.title("🛡️ SentryMesh AI Command Center")
st.markdown("### Autonomous Multi-Agent Incident Response & Self-Healing Engine")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cluster Status", "Healthy", "99.99% Uptime")
col2.metric("Active Agents", "2 / 2 Online", "Nano & Ultra")
col3.metric("MTTR Reduction", "88.4%", "-14.2m avg")
col4.metric("Backend Engine", "FastAPI + Mock/Nebius", "Active" if backend_ok else "Offline")

st.markdown("### ⚡ Trigger Simulated Incident")

service_name = st.selectbox("Target Microservice", ["payment-processor", "auth-gateway", "order-fulfillment", "inventory-sync"])
severity = st.selectbox("Incident Severity", ["CRITICAL", "HIGH", "MEDIUM"])
raw_logs = st.text_area("Raw Error Logs / Exception", "sqlalchemy.exc.TimeoutError: QueuePool limit of size 50 overflow 10 reached, connection timed out after 30.00s")
stack_trace = st.text_area("Stack Trace Snippet", "File 'server/db/session.py', line 42, in get_session\n    conn = pool.connect()\nTimeoutError: QueuePool overflow")

if st.button("🚀 Dispatch SentryMesh Agents"):
    with st.spinner("Orchestrating multi-agent pipeline (Nemotron-3 Nano -> Ultra)..."):
        try:
            payload = {
                "service_name": service_name,
                "severity": severity,
                "raw_logs": raw_logs,
                "stack_trace": stack_trace
            }
            res = requests.post(f"{API_URL}/api/v1/incident/resolve", json=payload, timeout=60)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Incident {data['incident_id']} successfully resolved in {data['execution_time_seconds']}s!")

                tab1, tab2, tab3 = st.tabs(["🔍 Triage Diagnostic", "🛠️ Code Remediation Patch", "📋 Execution Telemetry"])

                with tab1:
                    st.json(data["triage"])
                with tab2:
                    st.markdown(f"**Root Cause Explanation:**\n{data['remediation']['root_cause_explanation']}")
                    st.markdown("**Generated Code Patch (Git Diff):**")
                    st.code(data["remediation"]["code_patch"], language="diff")
                    st.markdown("**Verification Steps:**")
                    for step in data["remediation"]["verification_steps"]:
                        st.checkbox(step, value=True)
                with tab3:
                    st.json(data)
            else:
                st.error(f"Backend error: {res.text}")
        except Exception as e:
            st.error(f"Could not connect to the backend at {API_URL}. Error: {e}")