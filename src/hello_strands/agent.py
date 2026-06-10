import os

from strands import Agent
from strands.models.openai import OpenAIModel
from .tools import get_rand_message


def create_model() -> OpenAIModel:
    """Create the shared OpenAI-compatible model (call once at startup)."""
    return OpenAIModel(
        client_args={
            "api_key": os.environ.get("OPENAI_API_KEY", "placeholder"),
            "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        },
        model_id=os.environ.get("MODEL_ID", "gpt-5.4-mini"),
    )


def create_agent(
    model: OpenAIModel | None = None,
    system_prompt: str | None = None,
    callback_handler=None,
) -> Agent:
    """Create a Strands agent. Pass a shared model to reuse its HTTP client."""
    if model is None:
        model = create_model()
    kwargs: dict = {"model": model, "tools": [get_rand_message], "system_prompt": system_prompt}
    if callback_handler is not None:
        kwargs["callback_handler"] = callback_handler
    return Agent(**kwargs)
