import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SentryMesh AI API", version="1.0.0")

client = OpenAI(
base_url="https://api.nebius.ai/v1",
api_key=os.getenv("NEBIUS_API_KEY")
)

class IncidentRequest(BaseModel):
service_name: str
error_logs: str
stack_trace: str

@app.post("/api/triage")
async def triage_incident(data: IncidentRequest):
try:
triage_prompt = f"""
Analyze the following incident logs for service {data.service_name}:
Logs: {data.error_logs}
Stack Trace: {data.stack_trace}

    Extract the core anom
Extract the core anomaly, affected modules, and preliminary error signature.
    """
    
    triage_response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-instruct",
        messages=[{"role": "user", "content": triage_prompt}],
        temperature=0.1,
        max_tokens=512
    )
    
    triage_result = triage_response.choices[0].message.content

    reasoning_prompt = f"""
    Based on this triage output:
    {triage_result}
    
    Perform a comprehensive root-cause analysis and formulate an exact code-level patch strategy.
    """
    
    reasoning_response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-instruct",
        messages=[{"role": "user", "content": reasoning_prompt}],
        temperature=0.2,
        max_tokens=1024
    )
    
    patch_strategy = reasoning_response.choices[0].message.content

    return {
        "status": "success",
        "service": data.service_name,
        "triage_summary": triage_result,
        "remediation_strategy": patch_strategy
    }
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
if name == "main":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
