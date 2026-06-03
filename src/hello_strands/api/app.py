from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from hello_strands.api.routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    load_dotenv()
    yield


app = FastAPI(title="hello-strands", lifespan=lifespan)
app.include_router(router, prefix="/v1")
