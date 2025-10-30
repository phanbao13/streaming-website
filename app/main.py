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


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/watch-history", response_class=HTMLResponse)
async def watch_history_page(request: Request):
    return templates.TemplateResponse("watch_history.html", {"request": request})


@app.get("/favorites", response_class=HTMLResponse)
async def favorites_page(request: Request):
    return templates.TemplateResponse("favorites.html", {"request": request})


@app.get("/my-list", response_class=HTMLResponse)
async def my_list_page(request: Request):
    return templates.TemplateResponse("favorites.html", {"request": request})


@app.get("/browse/movies", response_class=HTMLResponse)
async def browse_movies_page(request: Request):
    return templates.TemplateResponse("browse_movies.html", {"request": request})


@app.get("/browse/series", response_class=HTMLResponse)
async def browse_series_page(request: Request):
    return templates.TemplateResponse("browse_series.html", {"request": request})

@app.get("/browse/tv-shows", response_class=HTMLResponse)
async def browse_tv_shows_page(request: Request):
    return templates.TemplateResponse("browse_tv-shows.html", {"request": request})

@app.get("/browse/anime", response_class=HTMLResponse)
async def browse_anime_page(request: Request):
    return templates.TemplateResponse("browse_anime.html", {"request": request})

@app.get("/browse/countries/{slug}", response_class=HTMLResponse)
async def browse_countries_page(request: Request, slug: str):
    return templates.TemplateResponse("browse_countries.html", {"request": request, "slug": slug})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
