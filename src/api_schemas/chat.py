# Request models
from pydantic import BaseModel

class SearchQuery(BaseModel):
    query: str

class ChatQuery(BaseModel):
    query: str