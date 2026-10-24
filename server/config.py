import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "")
    NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.nebius.ai/v1/")
    TRIAGE_MODEL = "nvidia/nemotron-3-nano-4b"
    REMEDIATION_MODEL = "nvidia/nemotron-3-ultra-70b"

config = Config()
