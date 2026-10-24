from pydantic import BaseModel, Field
from typing import List, Optional

class IncidentPayload(BaseModel):
    service_name: str = Field(..., description="Name of the affected microservice")
    severity: str = Field(..., description="Incident severity level (CRITICAL, HIGH, MEDIUM)")
    raw_logs: str = Field(..., description="Raw log stream snippet or exception header")
    stack_trace: Optional[str] = Field(None, description="Detailed stack trace if available")

class TriageResult(BaseModel):
    anomaly_signature: str
    affected_components: List[str]
    root_cause_category: str
    confidence_score: float

class PatchStrategy(BaseModel):
    root_cause_explanation: str
    code_patch: str
    verification_steps: List[str]
    rollback_plan: str

class AgenticPipelineResponse(BaseModel):
    incident_id: str
    service_name: str
    status: str
    triage: TriageResult
    remediation: PatchStrategy
    execution_time_seconds: float
