from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional


class UserSignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserSigninRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)

    @model_validator(mode="before")
    @classmethod
    def validate_username_or_email(cls, data):
        if not data.get("username") and not data.get("email"):
            raise ValueError("Either username or email must be provided")
        return data


class UserAuthResponse(BaseModel):
    message: str
    userId: str


class ErrorResponse(BaseModel):
    message: str
