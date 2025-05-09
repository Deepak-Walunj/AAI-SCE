from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.logging import get_logger
from app.models.user import AuthUser
from app.core.exceptions import DuplicateRequestException

logger = get_logger(__name__)

class AuthRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
        logger.info("AuthRepository initialized", collection=str(collection.full_name))

    async def create(self, user: AuthUser) -> AuthUser:
        logger.info("Creating new user", email=user.email)
        try:
            # Convert user to dict and ensure all required fields are present
            user_dict = user.model_dump()  # Use model_dump to exclude None values
            
            # Ensure we have all required fields
            required_fields = ['email', 'hashed_password', 'entity_type']
            missing_fields = [f for f in required_fields if f not in user_dict]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
            await self.collection.insert_one(user_dict)
            logger.info("User created successfully", user_id=user.userId)
            return user
        except Exception as e:
            logger.error("Failed to create user", error=str(e))
            raise DuplicateRequestException(f"Failed to create user: {str(e)}")

    async def find_by_email(self, email: str) -> Optional[AuthUser]:
        logger.info("Finding user by email", email=email)
        user_dict = await self.collection.find_one({"email": email})
        if user_dict:
            logger.info("User found", user_id=user_dict["userId"])
            return AuthUser(**user_dict)
        logger.info("User not found", email=email)
        return None

    async def find_by_user_id(self, user_id: str) -> Optional[AuthUser]:
        logger.info("Finding user by ID", user_id=user_id)
        user_dict = await self.collection.find_one({"userId": user_id})
        if user_dict:
            logger.info("User found", user_id=user_dict["userId"])
            return AuthUser(**user_dict)
        logger.info("User not found", user_id=user_id)
        return None
