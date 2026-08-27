from pydantic import BaseModel
from typing import List

class PaginatedMeta(BaseModel):
    total: int
    page: int
    size: int
