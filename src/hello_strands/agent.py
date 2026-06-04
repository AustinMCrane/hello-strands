import os

from strands import Agent
from strands.models.openai import OpenAIModel
from .tools import get_rand_message


def create_agent(system_prompt: str | None = None) -> Agent:
    """Create a Strands agent backed by an OpenAI-compatible endpoint."""
    base_url = os.environ["OPENAI_BASE_URL"]
    api_key = os.environ.get("OPENAI_API_KEY", "placeholder")
    model_id = os.environ.get("MODEL_ID", "gpt-4o")
    tools = [get_rand_message]

    model = OpenAIModel(
        client_args={
            "api_key": api_key,
            "base_url": base_url,
        },
        model_id=model_id,
    )

    return Agent(model=model, tools=tools, system_prompt=system_prompt or None)
