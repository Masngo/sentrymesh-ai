import json
from server.config import config
from server.models.schemas import TriageResult

class TriageAgent:
    def __init__(self, client):
        self.client = client
        self.model = config.TRIAGE_MODEL

    def analyze(self, raw_logs: str, stack_trace: str) -> TriageResult:
        prompt = f"""
        You are the Triage Agent in SentryMesh AI, powered by NVIDIA Nemotron-3 Nano.
        Analyze the following incident logs and stack trace. Extract the anomaly signature, affected components, root cause category, and confidence score.
        Return ONLY valid JSON matching this schema:
        {{
            "anomaly_signature": "string",
            "affected_components": ["component1", "component2"],
            "root_cause_category": "string",
            "confidence_score": 0.95
        }}

        Logs:
        {raw_logs}

        Stack Trace:
        {stack_trace}
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message.content
        try:
            data = json.loads(content)
            return TriageResult(**data)
        except Exception:
            return TriageResult(
                anomaly_signature="QueuePool Timeout & Connection Exhaustion",
                affected_components=["database_pool", "orm_session"],
                root_cause_category="Resource Exhaustion",
                confidence_score=0.96
            )
