import json
from openai import OpenAI
from server.config import config
from server.models.schemas import TriageResult, PatchStrategy

class RemediationAgent:
    def __init__(self, client: OpenAI):
        self.client = client

    def generate_patch(self, triage: TriageResult, logs: str, stack_trace: str) -> PatchStrategy:
        prompt = f"""
        You are an Autonomous Self-Healing Remediation Agent powered by NVIDIA Nemotron-3 Ultra.
        Triage Summary: {triage.model_dump_json()}
        Original Stack Trace: {stack_trace}

        Formulate an precise code patch and remediation strategy.
        Respond STRICTLY in JSON format with keys:
        - "root_cause_explanation": deep architectural analysis
        - "code_patch": exact git diff or code fix
        - "verification_steps": list of verification commands/tests
        - "rollback_plan": steps to undo if deployment fails
        """
        response = self.client.chat.completions.create(
            model=config.ULTRA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return PatchStrategy(**data)
