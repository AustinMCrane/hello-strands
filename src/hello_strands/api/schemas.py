from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None


# --- Non-streaming response ---


class ResponseMessage(BaseModel):
    role: str = "assistant"
    content: str


class Choice(BaseModel):
    index: int = 0
    message: ResponseMessage
    finish_reason: str = "stop"
    logprobs: None = None


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Choice]
    usage: Usage


# --- Streaming response (SSE chunks) ---


class Delta(BaseModel):
    role: str | None = None
    content: str | None = None


class ChunkChoice(BaseModel):
    index: int = 0
    delta: Delta
    finish_reason: str | None = None
    logprobs: None = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: list[ChunkChoice]
