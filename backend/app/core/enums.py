from enum import Enum

class EntityType(str, Enum):
    CANDIDATE = "candidate"
    ADMIN = "company_admin"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"