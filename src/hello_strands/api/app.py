import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hello_strands.agent import create_model
from hello_strands.api.routes import router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = create_model()
    yield


app = FastAPI(title="hello-strands", lifespan=lifespan)

cors_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/v1")
