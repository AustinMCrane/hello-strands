import asyncio
import sys

from dotenv import load_dotenv
from strands.handlers.callback_handler import null_callback_handler

from hello_strands.agent import create_agent


async def _stream_to_stdout(agent, prompt: str) -> None:
    print("Assistant: ", end="", flush=True)
    async for event in agent.stream_async(prompt):
        text: str = event.get("data", "")
        if text:
            print(text, end="", flush=True)
    print()


async def run_streaming(prompt: str) -> None:
    agent = create_agent(callback_handler=null_callback_handler)
    await _stream_to_stdout(agent, prompt)


async def interactive() -> None:
    agent = create_agent(callback_handler=null_callback_handler)
    print("hello-strands interactive mode. Type 'exit' to quit.\n")
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {"exit", "quit"}:
            break
        if not prompt:
            continue
        await _stream_to_stdout(agent, prompt)


def main() -> None:
    load_dotenv()

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        asyncio.run(run_streaming(prompt))
    else:
        asyncio.run(interactive())


if __name__ == "__main__":
    main()
