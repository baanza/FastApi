from uuid import UUID
from pydantic import BaseModel, Field

class tokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class tokenPayLoad(BaseModel):
    sub: str = None
    exp: int = None

class UserAuth(BaseModel):
    email : str = Field(..., description="user-email")
    password: str = Field(..., min_length=5, max_length=24, description="password")

class userOut(BaseModel):
    id: UUID
    email: str

class systemUser(userOut):
    password: str