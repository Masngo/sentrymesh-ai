from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IncidentPayload(BaseModel):
    service_name: str = Field(..., example="payment-gateway")
    severity: str = Field("HIGH", example="CRITICAL")
    raw_logs: str = Field(..., example="ERROR: DB Connection Refused on port 5432")
    stack_trace: str = Field(..., example="Traceback (most recent call last): ... ConnectionTimeoutError")

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
