import streamlit as st
import requests

st.set_page_config(
    page_title="SentryMesh AI - Command Center",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SentryMesh AI Command Center")
st.markdown("### Autonomous Multi-Agent Incident Response & Self-Healing Engine")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cluster Status", "Healthy", "99.99% Uptime")
col2.metric("Active Agents", "2 / 2 Online", "Nano & Ultra")
col3.metric("MTTR Reduction", "88.4%", "-14.2m avg")
col4.metric("Backend Engine", "FastAPI + Mock/Nebius", "Active")

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
            res = requests.post("http://localhost:8000/api/v1/incident/resolve", json=payload, timeout=10)
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
            st.error(f"Could not connect to FastAPI backend at http://localhost:8000. Make sure the server is running. Error: {e}")
