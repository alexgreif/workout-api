from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain a letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain a number")

        return v
    


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
