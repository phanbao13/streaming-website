"""
Updated KKPhim Service based on official API documentation
File: app/services/kkphim_service.py
"""

import httpx
from typing import Optional, Dict, Any, List
from app.config import settings
from app.core.cache import cache


class KKPhimService:
    def __init__(self):
        self.base_url = settings.KKPHIM_API_BASE_URL
        self.timeout = settings.KKPHIM_API_TIMEOUT

    async def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Make async request to KKPhim API"""
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def get_new_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get newly updated movies
        Endpoint: /danh-sach/phim-moi-cap-nhat
        """
        cache_key = f"new_movies:page:{page}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/danh-sach/phim-moi-cap-nhat", {"page": page})
        if data:
            cache.set(cache_key, data, ttl=300)
        return data

    async def get_movies(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """
        Get movies (phim-le)
        Endpoint: /v1/api/danh-sach/phim-le
        """
        cache_key = f"movies:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/danh-sach/phim-le", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_series(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """
        Get TV series (phim-bo)
        Endpoint: /v1/api/danh-sach/phim-bo
        """
        cache_key = f"series:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/danh-sach/phim-bo", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_tv_shows(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """
        Get TV shows (phim-tap)
        Endpoint: /v1/api/danh-sach/tv-shows
        """
        cache_key = f"tv_shows:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/danh-sach/tv-shows", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_anime(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """
        Get anime (phim-hoat-hinh)
        Endpoint: /v1/api/danh-sach/hoat-hinh
        """
        cache_key = f"anime:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/danh-sach/hoat-hinh", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_movie_detail(self, slug: str) -> Optional[Dict]:
        """
        Get movie details by slug
        Endpoint: /phim/{slug}
        """
        cache_key = f"movie_detail:{slug}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/phim/{slug}")
        if data:
            cache.set(cache_key, data, ttl=1800)
        return data

    async def search(
        self, keyword: str, page: int = 1, limit: int = 20
    ) -> Optional[Dict]:
        """
        Search movies/series
        Endpoint: /v1/api/tim-kiem
        """
        cache_key = f"search:{keyword}:{page}:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"keyword": keyword, "page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/tim-kiem", params)
        if data:
            cache.set(cache_key, data, ttl=300)
        return data

    async def get_by_category(
        self, category_slug: str, page: int = 1, limit: int = 20
    ) -> Optional[Dict]:
        """Get movies by category"""
        cache_key = f"category:{category_slug}:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/the-loai/{category_slug}", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_by_country(
        self, country_slug: str, page: int = 1, limit: int = 20
    ) -> Optional[Dict]:
        """Get movies by country"""
        cache_key = f"country:{country_slug}:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/quoc-gia/{country_slug}", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_by_year(
        self, year: int, page: int = 1, limit: int = 20
    ) -> Optional[Dict]:
        """Get movies by year"""
        cache_key = f"year:{year}:page:{page}:limit:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {"page": page, "limit": limit}
        data = await self._make_request(f"/v1/api/nam/{year}", params)
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_categories(self) -> Optional[Dict]:
        """Get all categories"""
        cache_key = "categories"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request("/the-loai")
        if data:
            cache.set(cache_key, data, ttl=86400)
        return data

    async def get_countries(self) -> Optional[Dict]:
        """Get all countries"""
        cache_key = "countries"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request("/quoc-gia")
        if data:
            cache.set(cache_key, data, ttl=86400)
        return data

    async def convert_image_to_webp(self, image_url: str) -> str:
        """Convert image to WebP format"""
        if not image_url:
            return ""
        return f"{self.base_url}/image.php?url={image_url}"

    
# Create singleton instance
kkphim_service = KKPhimService()
