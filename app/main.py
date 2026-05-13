from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .services.analysis import ConflictForecastService


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="US-Israel-Iran Conflict Forecast Platform",
    description="Full-stack research prototype implementing the Word document specification.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
service = ConflictForecastService()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    payload = service.dashboard()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "dashboard": payload},
    )


@app.get("/api/dashboard")
async def get_dashboard() -> dict:
    return service.dashboard()


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}
