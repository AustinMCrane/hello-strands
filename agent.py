import os
from strands import Agent, tool
from strands.models.anthropic import AnthropicModel


def _count_char(string: str, char: str) -> int:
    return string.count(char)


@tool
def count_char(string: str, char: str) -> int:
    """Count how many times a character appears in a string."""
    return _count_char(string, char)


model = AnthropicModel(
    model_id=os.environ.get("ANTHROPIC_MODEL_ID", "claude-3-5-sonnet-20241022"),
    max_tokens=1024,
)


def create_agent() -> Agent:
    """Return a fresh Agent with no conversation history."""
    return Agent(
        system_prompt="You are a helpful assistant. Use the count_char tool when asked about character occurrences in strings.",
        model=model,
        tools=[count_char],
    )


agent = create_agent()

if __name__ == "__main__":
    result = agent("How many times does the letter 'l' appear in 'hello world'?")
    print(result)
