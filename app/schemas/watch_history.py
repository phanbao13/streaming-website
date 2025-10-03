from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WatchHistoryBase(BaseModel):
    movie_slug: str
    movie_name: str
    episode_slug: Optional[str] = None
    episode_name: Optional[str] = None
    progress: float = 0.0


class WatchHistoryCreate(WatchHistoryBase):
    pass


class WatchHistoryUpdate(BaseModel):
    progress: float


class WatchHistoryResponse(WatchHistoryBase):
    id: int
    user_id: int
    last_watched: datetime

    class Config:
        from_attributes = True


class FavoriteCreate(BaseModel):
    movie_slug: str
    movie_name: str
    poster_url: Optional[str] = None


class FavoriteResponse(FavoriteCreate):
    id: int
    user_id: int
    added_at: datetime

    class Config:
        from_attributes = True
