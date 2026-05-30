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

## Run unit tests

```bash
pytest
```

Tests run against the pure Python helper `_count_char` — **no API key needed**.

## Run evals

Evals measure the agent’s end-to-end accuracy and performance using [`strands-agents-evals`](https://pypi.org/project/strands-agents-evals/).

```bash
python evals/run_evals.py
```

This runs 8 test cases through the live agent and reports:

| Evaluator | Type | What it checks |
|-----------|------|----------------|
| `Contains` | Deterministic | Correct integer appears in response |
| `ToolCalled` | Deterministic | `count_char` tool was invoked |
| `OutputEvaluator` | LLM judge | Response is clear and accurate |

At the end a performance summary shows min / avg / p95 latency across all cases.

## Eval architecture

```
Eval cases (eval_cases.py)
    └── Experiment.run_evaluations()
          ├── _TimedTracedHandler  ← records latency + OTel spans per case
          ├── fresh Agent per case ← no conversation history leakage
          └── 3 evaluators run on each result
```

`TracedHandler` collects OpenTelemetry spans from each agent call, which is what enables `ToolCalled` to inspect whether the tool was invoked. A fresh `Agent` instance is returned from the task function for each case so that conversation history never leaks between cases.
