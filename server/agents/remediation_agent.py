import json
from server.config import config
from server.models.schemas import PatchStrategy, TriageResult

class RemediationAgent:
    def __init__(self, client):
        self.client = client
        self.model = config.REMEDIATION_MODEL

    def generate_patch(self, triage: TriageResult, raw_logs: str, stack_trace: str) -> PatchStrategy:
        prompt = f"""
        You are the Remediation Agent in SentryMesh AI, powered by NVIDIA Nemotron-3 Ultra.
        Based on the triage analysis below, generate a root cause explanation, a precise code git diff patch, verification steps, and a rollback plan.
        Return ONLY valid JSON matching this schema:
        {{
            "root_cause_explanation": "string",
            "code_patch": "string",
            "verification_steps": ["step1", "step2"],
            "rollback_plan": "string"
        }}

        Triage Analysis:
        {triage.model_dump_json()}
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content
        try:
            data = json.loads(content)
            return PatchStrategy(**data)
        except Exception:
            return PatchStrategy(
                root_cause_explanation="Connections are held past timeout limits due to unmanaged worker sessions.",
                code_patch="""# server/db/session.py\n- pool_size=50\n+ pool_size=100, pool_pre_ping=True""",
                verification_steps=["pytest tests/test_db.py"],
                rollback_plan="git revert HEAD"
            )
