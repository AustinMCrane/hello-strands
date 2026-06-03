# hello-strands

A minimal [Strands Agents](https://strandsagents.com) scaffold using an OpenAI-compatible model endpoint.

## Setup

```bash
cp .env.example .env
# edit .env with your endpoint URL, API key, and model name
```

## Run

```bash
uv run hello-strands
uv run hello-strands "What is the capital of France?"
```

## Develop

```bash
uv sync --group dev
uv run pytest
uv run ruff check src/
```

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_BASE_URL` | yes | — | Base URL of the OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | no | `placeholder` | API key for the endpoint |
| `MODEL_ID` | no | `gpt-4o` | Model identifier to request |
