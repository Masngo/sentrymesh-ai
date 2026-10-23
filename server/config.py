import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NEBIUS_API_KEY: str = os.getenv("NEBIUS_API_KEY", "")
    NEBIUS_BASE_URL: str = "https://api.nebius.ai/v1"
    
    # NVIDIA Nemotron Models via Nebius Token Factory
    NANO_MODEL: str = "nvidia/nemotron-3-nano-30b-instruct"
    SUPER_MODEL: str = "nvidia/nemotron-3-super-120b-instruct"
    ULTRA_MODEL: str = "nvidia/nemotron-3-ultra-550b-instruct"

config = Config()
