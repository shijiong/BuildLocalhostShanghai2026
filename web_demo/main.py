import os

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from copilot_service import CopilotService


app = FastAPI(title="GitHub Copilot SDK Web Demo")
service = CopilotService(
    default_model="gpt-5.4",
    ollama_model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
    ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://192.168.0.117:11434/v1"),
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat/stream")
async def chat_stream(
    question: str = Form(...),
    model_choice: str = Form("gpt-5.4"),
    image: UploadFile | None = File(default=None),
):
    image_bytes = await image.read() if image else None
    image_name = image.filename if image else None
    image_mime = image.content_type if image else None

    async def body_iter():
        async for chunk in service.stream_answer(
            question=question,
            image_bytes=image_bytes,
            image_name=image_name,
            image_mime=image_mime,
            model_choice=model_choice,
        ):
            yield chunk

    return StreamingResponse(body_iter(), media_type="text/plain; charset=utf-8")


@app.get("/health")
async def health():
    return {"ok": True}
