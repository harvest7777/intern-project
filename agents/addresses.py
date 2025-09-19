import os
from uagents_core.identity import Identity
from uagents import Model
from dotenv import load_dotenv

load_dotenv()

def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return Identity.from_seed(seed=value, index=0).address

class AgentAddresses(Model):
    ORCHESTRATOR: str = require_env("ORCHESTRATOR_AGENT_SEED_PHRASE")
    WEATHER: str = require_env("WEATHER_AGENT_SEED_PHRASE")

AGENT_ADDRESSES = AgentAddresses()
