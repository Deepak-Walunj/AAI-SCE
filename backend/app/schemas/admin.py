from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.enums import Gender


class AdminProfileRequest(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Full name of the admin",
        error_messages={
            "min_length": "Name must be at least 1 characters long"
        }
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )

class AdminProfileRegisterRequest(AdminProfileRequest):
    password: str = Field(
        ..., 
        min_length=6,
        description="Password for authentication",
        error_messages={
            "min_length": "Password must be at least 6 characters long"
        }
    )

class AdminProfileSchema(BaseModel):
    userId: str
    email: EmailStr
    full_name: str

class AdminProfileResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    
class FailedRegistration(BaseModel):
    email: EmailStr
    error: str
