import asyncio
import base64
import os
from typing import AsyncGenerator

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import SessionEventType
from copilot.tools import define_tool
from pydantic import BaseModel, Field


class LookupKnowledgeParams(BaseModel):
    topic: str = Field(description="Knowledge topic, e.g. pricing, api, deployment")


@define_tool(description="Lookup fixed product knowledge for the assistant")
async def lookup_knowledge(params: LookupKnowledgeParams) -> dict:
    db = {
        "pricing": "Starter supports up to 1,000 requests/day in this demo policy.",
        "api": "Primary API uses HTTPS JSON and supports text+image analysis.",
        "deployment": "Recommended deployment path is containerized FastAPI behind a reverse proxy.",
    }
    topic = params.topic.strip().lower()
    return {"topic": topic, "result": db.get(topic, "No fixed knowledge found.")}


class CopilotService:
    def __init__(
        self,
        default_model: str = "gpt-5.4",
        ollama_model: str = "qwen3:8b",
        ollama_base_url: str | None = None,
    ) -> None:
        self.default_model = default_model
        self.ollama_model = ollama_model
        self.ollama_base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://192.168.0.117:11434/v1")

    async def stream_answer(
        self,
        question: str,
        image_bytes: bytes | None,
        image_name: str | None,
        image_mime: str | None,
        model_choice: str,
    ) -> AsyncGenerator[str, None]:
        client = CopilotClient()
        await client.start()

        queue: asyncio.Queue[str] = asyncio.Queue()
        done = asyncio.Event()

        choice = (model_choice or "gpt-5.4").strip().lower()
        session_kwargs = {
            "on_permission_request": PermissionHandler.approve_all,
            "streaming": True,
            "tools": [lookup_knowledge],
        }

        if choice == "ollama":
            session_kwargs["model"] = self.ollama_model
            session_kwargs["provider"] = {
                "type": "openai",
                "base_url": self.ollama_base_url,
            }
        else:
            session_kwargs["model"] = self.default_model

        session = await client.create_session(**session_kwargs)

        def on_event(event):
            if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                queue.put_nowait(event.data.delta_content)
            elif event.type == SessionEventType.SESSION_IDLE:
                done.set()

        session.on(on_event)

        attachments = None
        prompt = (
            "You are an analysis assistant in a web app. "
            "Answer in Chinese, structure the answer with short sections, "
            "and if image is attached, analyze the image first then answer the question.\n\n"
            f"Selected model source: {choice}\n"
            f"User question: {question}"
        )

        if image_bytes:
            attachments = [
                {
                    "type": "blob",
                    "data": base64.b64encode(image_bytes).decode("utf-8"),
                    "mimeType": image_mime or "application/octet-stream",
                    "displayName": image_name or "upload_image",
                }
            ]

        async def run_request() -> None:
            try:
                await session.send_and_wait(prompt, attachments=attachments)
            except Exception as exc:
                queue.put_nowait(f"\n[Copilot SDK Error] {exc}\n")
            finally:
                done.set()

        task = asyncio.create_task(run_request())

        try:
            while True:
                if done.is_set() and queue.empty():
                    break
                try:
                    chunk = await asyncio.wait_for(queue.get(), timeout=0.1)
                    yield chunk
                except asyncio.TimeoutError:
                    continue
        finally:
            await task
            await client.stop()
