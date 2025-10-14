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

    if not result or result.get("status") != "success":
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

    if not result or result.get("status") != "success":
        raise HTTPException(status_code=404, detail="No movies found")

    return {
        "success": True,
        "data": result.get("items", []),
        "pagination": result.get("pagination", {}),
    }


@router.get("/series")
async def get_series(
    page: int = Query(1, ge=1, description="Page number"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Get all TV series (phim-bo)"""
    result = await kkphim_service.get_series(page=page)

    if not result or result.get("status") != "success":
        raise HTTPException(status_code=404, detail="No series found")

    return {
        "success": True,
        "data": result.get("items", []),
        "pagination": result.get("pagination", {}),
    }


@router.get("/{slug}")
async def get_movie_detail(
    slug: str, user: Optional[User] = Depends(get_optional_user)
):
    """Get movie details by slug"""
    result = await kkphim_service.get_movie_detail(slug=slug)

    if not result or not result.get("movie"):
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"success": True, "data": result.get("movie")}


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

    if not result or result.get("status") != "success":
        raise HTTPException(status_code=404, detail="No movies found in this category")

    return {
        "success": True,
        "data": result.get("items", []),
        "pagination": result.get("pagination", {}),
    }
