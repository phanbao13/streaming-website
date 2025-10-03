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
        """Get newly updated movies"""
        cache_key = f"new_movies:page:{page}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/danh-sach/phim-moi-cap-nhat", {"page": page})
        if data:
            cache.set(cache_key, data, ttl=300)  # Cache for 5 minutes
        return data

    async def get_movies(self, page: int = 1) -> Optional[Dict]:
        """Get movies (phim-le)"""
        cache_key = f"movies:page:{page}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/v1/api/danh-sach/phim-le", {"page": page})
        if data:
            cache.set(cache_key, data, ttl=600)  # Cache for 10 minutes
        return data

    async def get_series(self, page: int = 1) -> Optional[Dict]:
        """Get TV series (phim-bo)"""
        cache_key = f"series:page:{page}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/v1/api/danh-sach/phim-bo", {"page": page})
        if data:
            cache.set(cache_key, data, ttl=600)
        return data

    async def get_movie_detail(self, slug: str) -> Optional[Dict]:
        """Get movie details by slug"""
        cache_key = f"movie_detail:{slug}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(f"/phim/{slug}")
        if data:
            cache.set(cache_key, data, ttl=1800)  # Cache for 30 minutes
        return data

    async def search(self, keyword: str, limit: int = 10) -> Optional[Dict]:
        """Search movies/series"""
        cache_key = f"search:{keyword}:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(
            f"/v1/api/tim-kiem", {"keyword": keyword, "limit": limit}
        )
        if data:
            cache.set(cache_key, data, ttl=300)
        return data

    async def get_by_category(
        self, category_slug: str, page: int = 1
    ) -> Optional[Dict]:
        """Get movies by category"""
        cache_key = f"category:{category_slug}:page:{page}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        data = await self._make_request(
            f"/v1/api/the-loai/{category_slug}", {"page": page}
        )
        if data:
            cache.set(cache_key, data, ttl=600)
        return data


kkphim_service = KKPhimService()
