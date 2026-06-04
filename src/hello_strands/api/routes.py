import asyncio
import time
import uuid
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from hello_strands.agent import create_agent
from hello_strands.api.schemas import (
    ChatCompletionChunk,
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    ChunkChoice,
    Delta,
    ResponseMessage,
    Usage,
)

router = APIRouter()


def _build_strands_messages(request: ChatCompletionRequest) -> tuple[list, str | None]:
    """Split OpenAI messages into a Strands-compatible message list and system prompt."""
    system_prompt = None
    strands_messages = []

    for msg in request.messages:
        if msg.role == "system":
            system_prompt = msg.content
        else:
            strands_messages.append(
                {"role": msg.role, "content": [{"text": msg.content}]}
            )

    return strands_messages, system_prompt


async def _stream_chunks(
    request: ChatCompletionRequest,
) -> AsyncGenerator[str, None]:
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())
    model = request.model

    messages, system_prompt = _build_strands_messages(request)
    agent = create_agent(system_prompt=system_prompt)

    # First chunk announces the assistant role
    first = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[ChunkChoice(delta=Delta(role="assistant"))],
    )
    yield f"data: {first.model_dump_json()}\n\n"

    # Pass the full conversation; stream_async accepts list[Message]
    prompt: list | str = messages if messages else ""
    async for event in agent.stream_async(prompt):
        text: str = event.get("data", "")
        if not text:
            continue
        chunk = ChatCompletionChunk(
            id=completion_id,
            created=created,
            model=model,
            choices=[ChunkChoice(delta=Delta(content=text))],
        )
        yield f"data: {chunk.model_dump_json()}\n\n"
        await asyncio.sleep(0)  # yield control so the event loop can flush

    # Final chunk signals end of stream
    final = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[ChunkChoice(delta=Delta(), finish_reason="stop")],
    )
    yield f"data: {final.model_dump_json()}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.stream:
        return StreamingResponse(
            _stream_chunks(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    # Non-streaming: run the agent and collect the full response
    messages, system_prompt = _build_strands_messages(request)
    agent = create_agent(system_prompt=system_prompt)
    prompt: list | str = messages if messages else ""
    result = agent(prompt)

    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:24]}",
        created=int(time.time()),
        model=request.model,
        choices=[Choice(message=ResponseMessage(content=str(result)))],
        usage=Usage(),
    )


@router.get("/models")
async def list_models():
    """Minimal /v1/models endpoint so OpenAI-compatible clients don't error."""
    import os

    model_id = os.environ.get("MODEL_ID", "gpt-4o")
    return {
        "object": "list",
        "data": [
            {
                "id": model_id,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "hello-strands",
            }
        ],
    }
