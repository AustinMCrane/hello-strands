# Hello Strands — Character Counter Agent

A minimal [Strands Agents](https://strandsagents.com) example with a single tool that counts character occurrences in a string.

## Prerequisites

- Python 3.10+
- An Anthropic API key

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Run the agent

```bash
python agent.py
```

The agent will answer: *"How many times does the letter 'l' appear in 'hello world'?"*

To use a different model, set `ANTHROPIC_MODEL_ID`:

```bash
export ANTHROPIC_MODEL_ID=claude-3-5-haiku-20241022
```

## Run tests

```bash
pytest
```

Tests are written against the pure Python helper `_count_char` so **no API key is needed** to run them. The tool-name test (`test_tool_name`) additionally verifies that the `@tool` decorator registered the function correctly with Strands.

## Testing strategy

| Layer | What's tested | Needs API key? |
|-------|--------------|----------------|
| Unit (`_count_char`) | Core logic — counts, edge cases, case sensitivity | No |
| Tool (`count_char.tool_name`) | Strands decorator wired up correctly | No |
| Integration (not included) | Full agent ↔ LLM loop | Yes — mock or real |

For integration tests, mock the model:

```python
from unittest.mock import MagicMock, patch

def test_agent_calls_tool():
    with patch("agent.model") as mock_model:
        mock_model.return_value = ...  # craft a tool-use response
```
