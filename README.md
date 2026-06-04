# hello-strands

A [Strands Agents](https://strandsagents.com) scaffold with two interfaces:

- **CLI** — interactive or one-shot prompt
- **HTTP API** — OpenAI-compatible `POST /v1/chat/completions` with streaming

## Setup

```bash
cp .env.example .env
# edit .env with your endpoint URL, API key, and model name
```

## CLI

```bash
# one-shot
uv run hello-strands "What is the capital of France?"

# interactive REPL
uv run hello-strands
```

## HTTP API (OpenAI-compatible)

```bash
uv run hello-strands-api
# or with options
HOST=127.0.0.1 PORT=8080 RELOAD=true uv run hello-strands-api
```

Endpoints:

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/chat/completions` | Chat completions (streaming supported) |
| `GET` | `/v1/models` | List available models |

### Example — non-streaming

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello!"}]}'
```

### Example — streaming

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello!"}],"stream":true}'
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
| `OPENAI_BASE_URL` | yes | — | Base URL of the OpenAI-compatible model endpoint |
| `OPENAI_API_KEY` | no | `placeholder` | API key for the endpoint |
| `MODEL_ID` | no | `gpt-4o` | Model identifier to request |
| `HOST` | no | `0.0.0.0` | Server bind address |
| `PORT` | no | `8000` | Server port |
| `RELOAD` | no | `false` | Enable uvicorn hot-reload (dev only) |

## Project structure

```
src/hello_strands/
├── agent.py          # shared agent factory (reads env vars)
├── cli.py            # CLI entry point
├── server.py         # uvicorn server entry point
└── api/
    ├── app.py        # FastAPI app with lifespan
    ├── routes.py     # POST /v1/chat/completions + GET /v1/models
    └── schemas.py    # OpenAI-compatible Pydantic models
```
