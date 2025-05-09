from typing import Optional
from app.models.user import AdminProfile
from app.core.logging import get_logger
from typing import Optional, BinaryIO, List
from app.schemas.admin import AdminProfileSchema
from app.models.user import AdminProfileFields
from motor.motor_asyncio import AsyncIOMotorCollection


logger = get_logger(__name__)

class AdminRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_by_user_id(self, user_id: str) -> Optional[AdminProfile]:
        profile_dict = await self.collection.find_one({AdminProfileFields.userId.value: user_id})
        print("Querying with:", {AdminProfileFields.userId.value: user_id})
        return AdminProfile(**profile_dict) if profile_dict else None

    async def create(self, profile: AdminProfile) -> AdminProfile:
        try:
            existing_admin = await self.find_by_email_ids([profile.email])
            if existing_admin:
                raise ValueError("Admin with this email already exists")
            profile_dict = profile.model_dump()
            await self.collection.insert_one(profile_dict)
            return profile
            
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")
            raise
    
    async def find_by_email_ids(self, email_ids: List[str]) -> Optional[List[AdminProfileSchema]]:
        profile_dict = await self.collection.find({AdminProfileFields.email.value: {"$in": email_ids}}).to_list()
        return [AdminProfileSchema(**p) for p in profile_dict] if profile_dict else None

    async def delete(self, user_id: str) -> None:
        await self.collection.delete_one({"userId": user_id})
        logger.info(f"Admin profile deleted with userId: {user_id}")
