from .base import DBModelBase
from uuid import uuid4
from pydantic import EmailStr, Field
from ..core.enums import EntityType, Gender
from typing import Optional
from enum import Enum

class AuthUserFields(str, Enum):
    userId = "userId"
    email = "email"
    hashed_password = "hashed_password"
    entity_type = "entity_type"

class AuthUser(DBModelBase):
    userId: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    hashed_password: str
    entity_type: EntityType

class CandidateProfileFields(str, Enum):
    userId = "userId"
    email = "email"
    full_name = "full_name"
    gender = "gender"
    
class AdminProfileFields(str, Enum):
    userId = "userId"
    email = "email"
    full_name = "full_name"

class CandidateProfile(DBModelBase):
    userId: str = Field(..., description="Reference to AuthUser.userId")
    email: EmailStr
    full_name: str
    gender: Optional[Gender] = None
    
class AuthProfile(DBModelBase):
    userId: str = Field(..., description="Reference to AuthUser.userId")
    email: EmailStr
    hashed_password: Optional[str] = None
    entity_type: Optional[str] = None

class AdminProfile(DBModelBase):
    userId: str = Field(..., description="Reference to AuthUser.userId")
    email: EmailStr
    full_name: str
    