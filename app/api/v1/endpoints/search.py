from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional

from app.services.kkphim_service import kkphim_service
from app.api.deps import get_optional_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def search_movies(
    keyword: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    user: Optional[User] = Depends(get_optional_user),
):
    """Search for movies and series"""
    if not keyword or len(keyword.strip()) == 0:
        raise HTTPException(status_code=400, detail="Search keyword is required")

    result = await kkphim_service.search(keyword=keyword.strip(), limit=limit)

    if not result:
        raise HTTPException(status_code=404, detail="No results found")

    return {
        "success": True,
        "keyword": keyword,
        "data": result.get("items", []),
        "total": len(result.get("items", [])),
    }
