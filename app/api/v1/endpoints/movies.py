from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.services.kkphim_service import kkphim_service
from app.api.deps import get_db, get_optional_user
from app.models.user import User

router = APIRouter()


@router.get("/new")
async def get_new_movies(
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get newly updated movies"""
    result = await kkphim_service.get_new_movies(page=page)

    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No movies found")

    return {
        "success": True,
        "data": result.get("items", []),
        "pagination": result.get("pagination", {}),
    }


@router.get("/movies")
async def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get all movies (phim-le)"""
    result = await kkphim_service.get_movies(page=page)

    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No movies found")

    return {
        "success": True,
        "data": result.get("data", []).get("items", []),
        "pagination": result.get("data", []).get("params", {}).get("pagination", {}),
    }


@router.get("/series")
async def get_series(
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get all TV series (phim-bo)"""
    result = await kkphim_service.get_series(page=page)

    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No series found")

    return {
        "success": True,
        "data": result.get("data", []).get("items", []),
        "pagination": result.get("data", []).get("params", {}).get("pagination", {}),
    }

@router.get("/tv-shows")
async def get_tv_shows(
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get all TV shows (phim-tap)"""
    result = await kkphim_service.get_tv_shows(page=page)

    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No TV shows found")

    return {
        "success": True,
        "data": result.get("data", []).get("items", []),
        "pagination": result.get("data", []).get("params", {}).get("pagination", {}),
    }

@router.get("/anime")
async def get_anime(    
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get all anime (phim-hoat-hinh)"""
    result = await kkphim_service.get_anime(page=page)

    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No anime found")

    return {
        "success": True,
        "data": result.get("data", []).get("items", []),
        "pagination": result.get("data", []).get("params", {}).get("pagination", {}),
    }

@router.get("/countries")
async def get_nation(user: Optional[User] = Depends(get_optional_user)):
    """Get all countries"""
    result = await kkphim_service.get_countries()

    if not result:
        raise HTTPException(status_code=404, detail="No countries found")
    
    return {"success": True, "data": result}

@router.get("/{slug}")
async def get_movie_detail(
    slug: str, user: Optional[User] = Depends(get_optional_user)
):
    """Get movie details by slug"""
    result = await kkphim_service.get_movie_detail(slug=slug)

    if not result or not result.get("movie"):
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"success": True, "data": result.get("movie"), "episodes": result.get("episodes", [])}


@router.get("/category/{category_slug}")
async def get_movies_by_category(
    category_slug: str,
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get movies by category"""
    result = await kkphim_service.get_by_category(
        category_slug=category_slug, page=page
    )
    if not result or result.get("status") != True:
        raise HTTPException(status_code=404, detail="No movies found in this category")

    return {
        "success": True,
        "data": result.get("data", []).get("items", []),
        "pagination": result.get("data", []).get("pagination", {}),
    }

@router.get("/convert-img")
async def convert_image_url(
    img_url: str,
    user: Optional[User] = Depends(get_optional_user)
):
    """Convert image URL using external API"""
    converted_url = kkphim_service.convert_image_to_webp(img_url)
    return {"success": True, "converted_url": converted_url}
