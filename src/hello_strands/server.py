import os

import uvicorn


def main() -> None:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    reload = os.environ.get("RELOAD", "false").lower() == "true"

    uvicorn.run(
        "hello_strands.api.app:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
