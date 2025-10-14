from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging

from app.config import settings
from app.api.v1.api import api_router
from app.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
    description="Movie Streaming Website API",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Homepage"""
    return templates.TemplateResponse("home.html", {"request": request})


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}


# Movie detail page
@app.get("/movie/{slug}", response_class=HTMLResponse)
async def movie_page(request: Request, slug: str):
    """Movie detail page"""
    return templates.TemplateResponse(
        "movie_detail.html", {"request": request, "slug": slug}
    )


# Watch page
@app.get("/watch/{slug}", response_class=HTMLResponse)
async def watch_page(request: Request, slug: str):
    """Watch/player page"""
    return templates.TemplateResponse("player.html", {"request": request, "slug": slug})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
