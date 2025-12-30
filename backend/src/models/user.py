from beanie import Document, init_beanie
from pydantic import Field, EmailStr, BaseModel
from pydantic import Field, EmailStr, BaseModel
from beanie import PydanticObjectId
from typing import List, Optional


class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    created_bots: List[PydanticObjectId] = Field(default_factory=list)
    credit_id: Optional[PydanticObjectId] = None

    class Settings:
        name = "users"
        indexes = [
            "username",  # For username lookups
            "email",  # For email lookups
        ]
