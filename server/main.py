import time
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

from server.config import config
from server.models.schemas import IncidentPayload, AgenticPipelineResponse
from server.agents.triage_agent import TriageAgent
from server.agents.remediation_agent import RemediationAgent

app = FastAPI(
    title="SentryMesh AI - Autonomous Multi-Agent Incident Engine",
    description="Tiered multi-agent incident response using NVIDIA Nemotron models on Nebius Cloud",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url=config.NEBIUS_BASE_URL,
    api_key=config.NEBIUS_API_KEY or "placeholder_key"
)

triage_agent = TriageAgent(client)
remediation_agent = RemediationAgent(client)

@app.get("/health")
def health_check():
    return {"status": "online", "engine": "Nebius Token Factory / NVIDIA Nemotron-3"}

@app.post("/api/v1/incident/resolve", response_model=AgenticPipelineResponse)
async def resolve_incident(payload: IncidentPayload):
    start_time = time.time()
    incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    
    try:
        # Step 1: Nano Agent Triage
        triage_summary = triage_agent.analyze(payload.raw_logs, payload.stack_trace)
        
        # Step 2: Ultra Agent Remediation
        remediation_patch = remediation_agent.generate_patch(
            triage_summary, payload.raw_logs, payload.stack_trace
        )
        
        elapsed = round(time.time() - start_time, 2)
        
        return AgenticPipelineResponse(
            incident_id=incident_id,
            service_name=payload.service_name,
            status="RESOLVED_AND_PATCHED",
            triage=triage_summary,
            remediation=remediation_patch,
            execution_time_seconds=elapsed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agentic Pipeline Failure: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
