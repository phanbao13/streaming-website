from pydantic import BaseModel
from typing import Optional, List


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20


class PaginatedResponse(BaseModel):
    data: List
    total: int
    page: int
    limit: int
    total_pages: int
