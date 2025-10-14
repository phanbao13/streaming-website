from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.watch_history import WatchHistory
from app.models.favorite import Favorite
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.watch_history import (
    WatchHistoryCreate,
    WatchHistoryResponse,
    WatchHistoryUpdate,
    FavoriteCreate,
    FavoriteResponse,
)

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update current user profile"""
    if user_update.email:
        # Check if email is taken by another user
        existing = (
            db.query(User)
            .filter(User.email == user_update.email, User.id != current_user.id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_update.email

    if user_update.username:
        # Check if username is taken by another user
        existing = (
            db.query(User)
            .filter(User.username == user_update.username, User.id != current_user.id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Username already in use")
        current_user.username = user_update.username

    if user_update.password:
        from app.core.security import get_password_hash

        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)

    return current_user


# Watch History Endpoints
@router.get("/watch-history", response_model=List[WatchHistoryResponse])
async def get_watch_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get user's watch history"""
    history = (
        db.query(WatchHistory)
        .filter(WatchHistory.user_id == current_user.id)
        .order_by(WatchHistory.last_watched.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return history


@router.post("/watch-history", response_model=WatchHistoryResponse)
async def add_or_update_watch_history(
    history_data: WatchHistoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Add or update watch history"""
    # Check if entry exists
    existing = (
        db.query(WatchHistory)
        .filter(
            WatchHistory.user_id == current_user.id,
            WatchHistory.movie_slug == history_data.movie_slug,
            WatchHistory.episode_slug == history_data.episode_slug,
        )
        .first()
    )

    if existing:
        # Update existing
        existing.progress = history_data.progress
        existing.movie_name = history_data.movie_name
        existing.episode_name = history_data.episode_name
        from datetime import datetime

        existing.last_watched = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        new_history = WatchHistory(user_id=current_user.id, **history_data.dict())
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
        return new_history


@router.delete("/watch-history/{history_id}")
async def delete_watch_history(
    history_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete watch history entry"""
    history = (
        db.query(WatchHistory)
        .filter(WatchHistory.id == history_id, WatchHistory.user_id == current_user.id)
        .first()
    )

    if not history:
        raise HTTPException(status_code=404, detail="Watch history not found")

    db.delete(history)
    db.commit()

    return {"success": True, "message": "Watch history deleted"}


# Favorites Endpoints
@router.get("/favorites", response_model=List[FavoriteResponse])
async def get_favorites(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get user's favorite movies"""
    favorites = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id)
        .order_by(Favorite.added_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return favorites


@router.post("/favorites", response_model=FavoriteResponse)
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Add movie to favorites"""
    # Check if already favorited
    existing = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.movie_slug == favorite_data.movie_slug,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Movie already in favorites")

    new_favorite = Favorite(user_id=current_user.id, **favorite_data.dict())
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite


@router.delete("/favorites/{movie_slug}")
async def remove_favorite(
    movie_slug: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Remove movie from favorites"""
    favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id, Favorite.movie_slug == movie_slug)
        .first()
    )

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()

    return {"success": True, "message": "Removed from favorites"}


@router.get("/favorites/check/{movie_slug}")
async def check_favorite(
    movie_slug: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Check if movie is in favorites"""
    favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == current_user.id, Favorite.movie_slug == movie_slug)
        .first()
    )

    return {"is_favorite": favorite is not None}
