# SentryMesh AI 🛡️
> Autonomous Multi-Agent Incident Response & Code Self-Healing Engine powered by NVIDIA Nemotron models on Nebius Token Factory.

[![Streamlit Cloud Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sentrymesh-ai-xi7vaxaebip4gbgzgvxvyp.streamlit.app)
[![Nebius x NVIDIA Hackathon](https://img.shields.io/badge/Hackathon-Nebius%20%2F%20NVIDIA-blueviolet)](https://devpost.com)

---

## 🚀 Live Demo & Access
* **Interactive Command Center UI:** [sentrymesh-ai-xi7vaxaebip4gbgzgvxvyp.streamlit.app](https://sentrymesh-ai-xi7vaxaebip4gbgzgvxvyp.streamlit.app)
* **Backend API Docs:** Hosted locally via FastAPI (`/docs`) or via Docker Compose.

---

## 🧠 Architecture & Nebius Integration
SentryMesh AI decouples incident resolution into a high-performance agentic pipeline leveraging **NVIDIA open-source models** hosted on **Nebius Token Factory**:

1. **Triage Agent (NVIDIA Nemotron-3 Nano via Nebius):** Parses high-throughput telemetry, log spikes, and trace dumps to extract anomaly signatures and classify incident severity.
2. **Remediation Agent (NVIDIA Nemotron-3 Ultra via Nebius):** Evaluates deep system context, performs root-cause analysis, and generates automated code patches with verification test suites.

---

## ✨ Features
- **FastAPI Core Engine:** High-performance async microservice REST interface for agent orchestration.
- **Streamlit Command Center:** A mission-control dark theme UI for live telemetry monitoring, log analysis, and manual triage overrides.
- **Docker & Docker Compose:** Instant containerized deployment supporting multi-environment orchestration.

---

## 🛠️ Quick Start & Installation

### Option 1: Local Docker Deployment
```bash
# 1. Clone the repository
git clone [https://github.com/Masngo/sentrymesh-ai.git](https://github.com/Masngo/sentrymesh-ai.git)
cd sentrymesh-ai

# 2. Set your Nebius API Key
export NEBIUS_API_KEY="your-nebius-api-key"

# 3. Spin up using Docker Compose
docker-compose up --build
Access the Command Center UI at http://localhost:8501

Access FastAPI interactive documentation at http://localhost:8000/docs
cd UI
pip install -r ../requirements.txt
streamlit run app.py
🏆 Hackathon Track
Submitted for the Nebius x NVIDIA Global AI Hackathon — Coding and Agentic Engineering Track.
