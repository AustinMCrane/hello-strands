import sys

from dotenv import load_dotenv

from hello_strands.agent import create_agent


def main() -> None:
    load_dotenv()

    agent = create_agent()

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Hello! Tell me what you can do."

    print(agent(prompt))


if __name__ == "__main__":
    main()
