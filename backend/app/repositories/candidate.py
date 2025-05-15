from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.user import CandidateProfile
from app.core.logging import get_logger
from typing import Optional, BinaryIO, List
from app.schemas.candidate import CandidateProfileSchema, CandidateProfileUpdate, CandidateProcessData
from app.models.user import CandidateProfileFields
from app.core.exceptions import NotFoundException
from datetime import datetime

logger = get_logger(__name__)

class CandidateRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create(self, profile: CandidateProfile) -> CandidateProfile:
        try:
            existing_candidate = await self.find_by_email_ids([profile.email])
            if existing_candidate:
                raise ValueError("Candidate with this email already exists")
            profile_dict = profile.model_dump()
            await self.collection.insert_one(profile_dict)
            return profile
            
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")
            raise
        
    async def find_by_email_ids(self, email_ids: List[str]) -> Optional[List[CandidateProfileSchema]]:
        profile_dict = await self.collection.find({CandidateProfileFields.email.value: {"$in": email_ids}}).to_list()
        return [CandidateProfileSchema(**p) for p in profile_dict] if profile_dict else None
    
    async def find_by_user_id(self, user_id: str) -> Optional[CandidateProfile]:
        profile_dict = await self.collection.find_one({CandidateProfileFields.userId.value: user_id})
        return CandidateProfile(**profile_dict) if profile_dict else None

    async def update(self, user_id: str, data: CandidateProfileUpdate) -> CandidateProfile:
        update_data = data.dict_not_none()
        result = await self.collection.find_one_and_update(
            {"userId": user_id},
            {"$set": update_data},
            return_document=True
        )
        if not result:
            raise NotFoundException(f"Candidate profile with userId {user_id} not found")
            
        return CandidateProfile(**result)
    
    async def delete(self, user_id: str) -> None:
        await self.collection.delete_one({"userId": user_id})
        
    async def add_process(self, user_id: str, data: CandidateProcessData) -> str:
        candidate = await self.find_by_user_id(user_id)
        if not candidate:
            raise NotFoundException(f"Candidate profile with userId {user_id} not found")
        result="Work in progress"
        new_entry = {
            "text": data.text,
            "text_type": data.text_type,
            "tone": data.tone,
            "output_type": data.output_type,
            "output_language": data.output_language,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        process_data=candidate.process or {}
        idx=str(len(process_data)+1)
        process_data[idx] = new_entry
        await self.collection.update_one(
            {"userId": user_id},
            {
                "$set": {
                    "process": process_data,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result