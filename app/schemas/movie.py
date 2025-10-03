from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class Episode(BaseModel):
    name: str
    slug: str
    filename: str
    link_embed: Optional[str] = None
    link_m3u8: Optional[str] = None


class Category(BaseModel):
    id: str
    name: str
    slug: str


class Country(BaseModel):
    id: str
    name: str
    slug: str


class MovieBase(BaseModel):
    name: str
    slug: str
    origin_name: str
    poster_url: Optional[str] = None
    thumb_url: Optional[str] = None
    year: Optional[int] = None
    type: str  # "single" or "series"


class MovieDetail(MovieBase):
    content: Optional[str] = None
    trailer_url: Optional[str] = None
    time: Optional[str] = None
    episode_current: Optional[str] = None
    episode_total: Optional[str] = None
    quality: Optional[str] = None
    lang: Optional[str] = None
    director: Optional[List[str]] = []
    actor: Optional[List[str]] = []
    category: Optional[List[Category]] = []
    country: Optional[List[Country]] = []
    episodes: Optional[List[dict]] = []  # Server data with episodes
    view: Optional[int] = 0

    class Config:
        from_attributes = True


class MovieList(BaseModel):
    movies: List[MovieBase]
    pagination: dict
