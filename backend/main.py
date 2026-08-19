from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import get_settings
from .limiter import limiter
from .routers import ai, itinerary, locations, trips
from .utils.errors import AppError

settings = get_settings()
log = logging.getLogger("ai-travel-guide")
ROOT_DIR = Path(__file__).resolve().parent.parent
frontend_dist = ROOT_DIR / "dist"

app = FastAPI(
    title="AI Travel Guide",
    description="Premium AI-powered travel planning API",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router)
app.include_router(ai.router)
app.include_router(locations.router)
app.include_router(itinerary.router)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message, "code": exc.code})


@app.exception_handler(Exception)
async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    log.exception("Unhandled planning error")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Something went wrong while planning this trip. Please try again in a moment.",
            "code": "internal_error",
        },
    )


@app.get("/api/health")
async def health() -> dict:
    return {
        "ok": True,
        "ai": settings.ai_enabled,
        "google_maps": settings.google_enabled,
        "model": settings.openrouter_model,
        "provider": settings.openrouter_provider,
    }


if (frontend_dist / "index.html").exists():
    assets = frontend_dist / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")

    @app.get("/{full_path:path}")
    async def spa(full_path: str) -> FileResponse:
        candidate = frontend_dist / full_path
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(frontend_dist / "index.html")
else:

    @app.get("/")
    async def dev_frontend() -> RedirectResponse:
        return RedirectResponse("http://localhost:5173")
