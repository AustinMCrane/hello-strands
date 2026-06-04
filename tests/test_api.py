import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from hello_strands.api.app import app

client = TestClient(app)

ENV = {
    "OPENAI_BASE_URL": "https://test.example.com/v1",
    "OPENAI_API_KEY": "test-key",
    "MODEL_ID": "test-model",
}


def _mock_agent(response_text: str = "Hello!") -> MagicMock:
    mock = MagicMock()
    mock.return_value = response_text
    return mock


@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)


def test_chat_completions_non_streaming():
    with patch("hello_strands.api.routes.create_agent", return_value=_mock_agent("Hi there!")):
        resp = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": [{"role": "user", "content": "Hello"}],
            },
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["object"] == "chat.completion"
    assert body["choices"][0]["message"]["content"] == "Hi there!"
    assert body["choices"][0]["finish_reason"] == "stop"


def test_chat_completions_with_system_message():
    mock_agent = _mock_agent("Sure!")

    with patch("hello_strands.api.routes.create_agent", return_value=mock_agent) as mock_factory:
        resp = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": [
                    {"role": "system", "content": "Be brief."},
                    {"role": "user", "content": "Hi"},
                ],
            },
        )

    assert resp.status_code == 200
    mock_factory.assert_called_once_with(system_prompt="Be brief.")


def test_chat_completions_streaming():
    async def fake_stream(prompt):
        yield {"data": "Hello"}
        yield {"data": " world"}
        yield {"current_tool_use": {}}  # non-text event, should be ignored

    mock_agent = MagicMock()
    mock_agent.stream_async = fake_stream

    with patch("hello_strands.api.routes.create_agent", return_value=mock_agent):
        resp = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": True,
            },
        )

    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")

    lines = [l for l in resp.text.splitlines() if l.startswith("data:")]
    assert lines[-1] == "data: [DONE]"

    chunks = [json.loads(l[len("data: "):]) for l in lines[:-1]]
    # First chunk has role
    assert chunks[0]["choices"][0]["delta"]["role"] == "assistant"
    # Content chunks
    content = "".join(
        c["choices"][0]["delta"].get("content") or "" for c in chunks
    )
    assert "Hello" in content
    assert "world" in content


def test_list_models():
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    body = resp.json()
    assert body["object"] == "list"
    assert body["data"][0]["id"] == "test-model"
