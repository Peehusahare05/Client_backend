from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    disabled: bool = False
