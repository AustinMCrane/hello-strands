import asyncio
import os
import time
import uuid
from collections.abc import AsyncGenerator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from strands.handlers.callback_handler import null_callback_handler

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

_MODEL_ID = os.environ.get("MODEL_ID", "gpt-5.4-mini")


def _extract_text(content: str | list) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for part in content:
        if isinstance(part, dict) and part.get("type") == "text":
            parts.append(part.get("text", ""))
        elif isinstance(part, str):
            parts.append(part)
    return "".join(parts)


def _build_strands_messages(request: ChatCompletionRequest) -> tuple[list, str | None]:
    system_prompt = None
    strands_messages = []

    for msg in request.messages:
        if msg.role == "system":
            system_prompt = _extract_text(msg.content)
        else:
            strands_messages.append(
                {"role": msg.role, "content": [{"text": _extract_text(msg.content)}]}
            )

    return strands_messages, system_prompt


async def _stream_chunks(
    request: ChatCompletionRequest, http_request: Request
) -> AsyncGenerator[str, None]:
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())
    model = request.model
    include_usage = request.stream_options and request.stream_options.include_usage

    messages, system_prompt = _build_strands_messages(request)
    agent = create_agent(
        model=http_request.app.state.model,
        system_prompt=system_prompt,
        callback_handler=null_callback_handler,
    )

    first = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[ChunkChoice(delta=Delta(role="assistant"))],
    )
    yield f"data: {first.model_dump_json()}\n\n"

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
        await asyncio.sleep(0)

    final = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[ChunkChoice(delta=Delta(), finish_reason="stop")],
        usage=Usage() if include_usage else None,
    )
    yield f"data: {final.model_dump_json()}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest, http_request: Request):
    if request.stream:
        return StreamingResponse(
            _stream_chunks(request, http_request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    messages, system_prompt = _build_strands_messages(request)
    agent = create_agent(
        model=http_request.app.state.model,
        system_prompt=system_prompt,
        callback_handler=null_callback_handler,
    )
    prompt: list | str = messages if messages else ""
    result = await asyncio.to_thread(agent, prompt)

    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:24]}",
        created=int(time.time()),
        model=request.model,
        choices=[Choice(message=ResponseMessage(content=str(result)))],
        usage=Usage(),
    )


def _model_object(model_id: str) -> dict:
    return {
        "id": model_id,
        "object": "model",
        "created": 0,
        "owned_by": "hello-strands",
    }


@router.get("/models")
async def list_models():
    return {"object": "list", "data": [_model_object(_MODEL_ID)]}


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    if model_id != _MODEL_ID:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")
    return _model_object(_MODEL_ID)
