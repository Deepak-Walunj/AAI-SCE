from enum import Enum

class CollectionName(str, Enum):
    AUTH_USERS = "users" 
    CANDIDATES = "candidates"
    ADMIN = "admin"


    @classmethod
    def get_all(cls):
        return [v.value for v in cls.__members__.values()]

    @classmethod
    def get_by_entity_type(cls, entity_type: str) -> str:
        if entity_type == "candidate":
            return cls.CANDIDATES.value
        elif entity_type == "admin":
            return cls.ADMIN.value
        raise ValueError(f"Unknown entity type: {entity_type}")