import asyncio
from .gpt import Gpt
from .config import Settings
from functools import lru_cache
from urllib.parse import quote
from fastapi import FastAPI
from typing import AsyncIterable, Awaitable
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

# Ensure settings object is created once and return the same object each time this func is called
@lru_cache
def get_settings():
    return Settings()

async def wrap_chain(message: str) -> AsyncIterable[str]:
    # Initialize gpt instance and pass Settings in
    gpt = Gpt(get_settings())
    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with a event to signal when it's done or an exception is raised"""
        try:
            return await fn
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop
            event.set()

    # Begin a task that runs in the background thread
    task = asyncio.create_task(wrap_done(gpt.query(message), gpt.callback.done))

    async for token in gpt.callback.aiter():
        # Use SSE to stream the response
        print(f"{token}", file=open('output.txt', 'a'))
        yield f"data: {token}\n\n"

    # await task
    res = await task
    source_docs_set = set([doc.metadata["source"] for doc in res["source_documents"]])

    yield "data: Sources:\n\n"
    for src in source_docs_set:
        yield f"data: {src}\n\n"

async def generate_sample_data():
    for i in range(10):
        yield f"data: {i} \n\n"
        await asyncio.sleep(1)

# Simple root url for simple PING (healthcheck)
@app.get("/")
async def root():
    return "Welcome to bookworm"

class QueryReq(BaseModel):
    """Request body for query (streaming response).""" 
    message: str

# Response returned by chromadb and ollama model
@app.post("/query")
async def query(body: QueryReq):
    return StreamingResponse(wrap_chain(body.message), media_type="text/event-stream")

# Test endpoint which stream string via SSE
@app.post("/test")
async def test():
    return StreamingResponse(generate_sample_data(), media_type="text/event-stream")