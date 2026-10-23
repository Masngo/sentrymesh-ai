# SentryMesh AI 🛡️
> Autonomous Multi-Agent Incident Response & Code Self-Healing Engine powered by NVIDIA Nemotron models on Nebius Token Factory.

## Architecture
SentryMesh AI decouples incident resolution into an agentic pipeline:
1. **Triage Agent (NVIDIA Nemotron-3 Nano):** Parses high-throughput telemetry, log spikes, and trace dumps to extract anomaly signatures.
2. **Remediation Agent (NVIDIA Nemotron-3 Ultra):** Evaluates deep system context, performs root-cause analysis, and generates code patches with verification tests.

## Features
- **FastAPI Core Engine:** High-performance async microservice REST interface.
- **Streamlit Command Center:** Interactive UI for live telemetry and manual triage overrides.
- **Docker & Docker Compose:** Ready for instant local or cloud deployment.

## Quick Start
```bash
# 1. Export Nebius Token Factory Key
export NEBIUS_API_KEY="your-nebius-api-key"

# 2. Spin up using Docker Compose
docker-compose up --build
Access the Command Center at http://localhost:8501 and FastAPI Docs at http://localhost:8000/docs.
