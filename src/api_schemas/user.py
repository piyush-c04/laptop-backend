# app/api_schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.api_schemas.review import ReviewResponse

# ======================
# USER SCHEMAS
# ======================

class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str  # raw password from frontend

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: Optional[str] = "true"
    date_created: Optional[str] = None

    model_config = {
        "from_attributes": True
    }



