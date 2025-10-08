from pydantic import BaseModel
from typing import List

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

class FileIn(BaseModel):
    title: str
    description: str = ""
    min_role_weight: int = 10
    tags: List[str] = []

class FileOut(BaseModel):
    id: int
    title: str
    size_bytes: int
    min_role_weight: int
    info_hash: str
    tags: List[str] = []

class SearchQuery(BaseModel):
    q: str