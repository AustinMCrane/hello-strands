import sys

from dotenv import load_dotenv

from hello_strands.agent import create_agent


def main() -> None:
    load_dotenv()

    agent = create_agent()

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(agent(prompt))
    else:
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
            print(f"Agent: {agent(prompt)}\n")


if __name__ == "__main__":
    main()
