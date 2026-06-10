# hello-strands

A [Strands Agents](https://strandsagents.com) template with two interfaces:

- **CLI** — interactive REPL or one-shot prompt, with streaming output
- **HTTP API** — OpenAI-compatible server (chat completions, streaming, models list)

Use this as a starting point: clone, set your env vars, add tools, and go.

---

## Quickstart

```bash
cp .env.example .env
# fill in OPENAI_BASE_URL, OPENAI_API_KEY, MODEL_ID
uv sync
```

## CLI

```bash
# one-shot
uv run hello-strands "What is the capital of France?"

# interactive REPL (type 'exit' to quit)
uv run hello-strands
```

## HTTP API

```bash
uv run hello-strands-api
# with options
HOST=127.0.0.1 PORT=8080 RELOAD=true uv run hello-strands-api
```

Endpoints:

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/chat/completions` | Chat completions (streaming + non-streaming) |
| `GET` | `/v1/models` | List available models |
| `GET` | `/v1/models/{model_id}` | Get a single model |

### Non-streaming

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.4-mini","messages":[{"role":"user","content":"Hello!"}]}'
```

### Streaming

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.4-mini","messages":[{"role":"user","content":"Hello!"}],"stream":true}'
```

---

## Using with opencode

An `opencode.jsonc` is included. Start the API server, then open opencode in this directory — it will pick up the config automatically and list the model.

```bash
uv run hello-strands-api &
opencode
```

The `apiKey` in `opencode.jsonc` reads from `${OPENAI_API_KEY}` — export it in your shell before launching:

```bash
export $(grep -v '^#' .env | xargs)
opencode
```

---

## Using with Open WebUI

1. Start the API server: `uv run hello-strands-api`
2. In Open WebUI → Settings → Connections → add an OpenAI-compatible connection pointing to `http://localhost:8000`
3. The model will appear in the model selector

---

## Customizing this template

### Add tools

Add tool functions to `src/hello_strands/tools/` decorated with `@tool`, export them from `tools/__init__.py`, and register them in `create_agent()` in `agent.py`:

```python
tools = [get_rand_message, your_new_tool]
```

### Change the model

Set `MODEL_ID` in `.env`. The same value is used by the CLI, the API server, and the `/v1/models` endpoint.

### Change the system prompt

Pass `system_prompt=` to `create_agent()`, or send a `{"role":"system","content":"..."}` message at the start of the conversation via the API.

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Base URL of the OpenAI-compatible model endpoint |
| `OPENAI_API_KEY` | `placeholder` | API key for the endpoint |
| `MODEL_ID` | `gpt-5.4-mini` | Model identifier |
| `CORS_ORIGINS` | `*` | Comma-separated list of allowed CORS origins |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `RELOAD` | `false` | Enable uvicorn hot-reload (dev only) |

## Project structure

```
src/hello_strands/
├── agent.py          # create_model() and create_agent() — customize tools here
├── cli.py            # CLI entry point
├── server.py         # uvicorn entry point
├── tools/
│   └── rand.py       # example tool — replace with your own
└── api/
    ├── app.py        # FastAPI app + CORS + lifespan (shared model)
    ├── routes.py     # /v1/chat/completions, /v1/models
    └── schemas.py    # OpenAI-compatible Pydantic models
```

## Develop

```bash
uv sync --group dev
uv run pytest
uv run ruff check src/
```
