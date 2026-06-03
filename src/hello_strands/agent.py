import os

from strands import Agent
from strands.models.openai import OpenAIModel


def create_agent() -> Agent:
    """Create a Strands agent backed by an OpenAI-compatible endpoint."""
    base_url = os.environ["OPENAI_BASE_URL"]
    api_key = os.environ.get("OPENAI_API_KEY", "placeholder")
    model_id = os.environ.get("MODEL_ID", "gpt-4o")

    model = OpenAIModel(
        client_args={
            "api_key": api_key,
            "base_url": base_url,
        },
        model_id=model_id,
    )

    return Agent(model=model)
