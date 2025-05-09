from typing import BinaryIO, Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from app.core.enums import Gender

class CandidateProfileRequest(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Full name of the candidate",
        error_messages={
            "min_length": "Name must be at least 1 characters long"
        }
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )

    gender: Gender = Field(
        ..., 
        description=f"Gender of the candidate. Must be one of: {', '.join(g.value for g in Gender)}"
    )

class CandidateProfileRegisterRequest(CandidateProfileRequest):
    password: str = Field(
        ..., 
        min_length=6,
        description="Password for authentication",
        error_messages={
            "min_length": "Password must be at least 6 characters long"
        }
    )

class CandidateProfileSchema(BaseModel):
    userId: str
    email: EmailStr
    full_name: str
    gender: Optional[Gender] = None
    
class CandidateProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    gender: Optional[Gender] = None

    def dict_not_none(self):
        return {k: v for k, v in self.model_dump().items() if v is not None}

class CandidateProfileResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class FailedRegistration(BaseModel):
    email: EmailStr
    error: str

