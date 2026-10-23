import json
from openai import OpenAI
from server.config import config
from server.models.schemas import TriageResult

class TriageAgent:
    def __init__(self, client: OpenAI):
        self.client = client

    def analyze(self, logs: str, stack_trace: str) -> TriageResult:
        prompt = f"""
        You are an expert Reliability Engineer Agent powered by NVIDIA Nemotron-3 Nano.
        Perform fast parallel triage on this incident:
        Logs: {logs}
        Stack Trace: {stack_trace}

        Respond STRICTLY in JSON format with keys:
        - "anomaly_signature": concise title
        - "affected_components": list of strings
        - "root_cause_category": category name
        - "confidence_score": float between 0.0 and 1.0
        """
        response = self.client.chat.completions.create(
            model=config.NANO_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return TriageResult(**data)
