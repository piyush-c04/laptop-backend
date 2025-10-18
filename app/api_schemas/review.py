from pydantic import BaseModel
from typing import Optional

# Review Schemas
class ReviewBase(BaseModel):
    username: str
    rating: float
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    laptop_id: int

    class Config:
        orm_mode = True