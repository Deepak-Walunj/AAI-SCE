from typing import BinaryIO, Optional, Tuple, List
from app.repositories.candidate import CandidateRepository
from app.services.auth import AuthService
from app.models.user import CandidateProfile
from app.schemas.candidate import (
    CandidateProfileUpdate,
    CandidateProfileRegisterRequest,
    CandidateProfileSchema,
    FailedRegistration
)
from app.schemas.auth import UserRegisterRequest
from app.core.enums import EntityType
from app.core.logging import get_logger

logger = get_logger(__name__)

class CandidateService:
    def __init__(self, candidate_repository: CandidateRepository, auth_service: AuthService,):
        self.candidate_repository = candidate_repository
        self.auth_service = auth_service
        
    async def get_profile(self, user_id: str) -> Optional[CandidateProfile]:
        return await self.candidate_repository.find_by_user_id(user_id)
    
    async def register_candidate(self, data: CandidateProfileRegisterRequest) -> CandidateProfileSchema:
        candidate_auth_data = UserRegisterRequest(
            email = data.email,
            password = data.password,
            entity_type = EntityType.CANDIDATE,
        )
        user = await self.auth_service.register(candidate_auth_data)
        candidate = CandidateProfile(
            userId = user.userId,
            email = data.email,
            full_name = data.name,
            gender = data.gender,
        )
        profile = await self.create_profile(candidate)
        logger.info("Candidate registered successfully.", candidate_id=profile.userId, email=data.email)
        return CandidateProfileSchema(**profile.model_dump())
    
    async def create_profile(self, candidate: CandidateProfile) -> CandidateProfile:
        return await self.candidate_repository.create(candidate)
    
    async def _safe_register_candidate(self, candidate: CandidateProfileRegisterRequest) -> Tuple[Optional[CandidateProfileSchema], Optional[FailedRegistration]]:
        """Safely register a candidate and return either a success or failure result."""
        try:
            registered = await self.register_candidate(candidate)
            return registered, None
        except Exception as e:
            logger.error(f"Failed to register candidate", email=candidate.email, error=str(e))
            return None, FailedRegistration(
                email=candidate.email,
                error=str(e)
            )
    
    async def update_profile(self, user_id: str, data: CandidateProfileUpdate) -> CandidateProfile:
        return await self.candidate_repository.update(user_id, data)
    
    async def delete_profile(self, user_id: str) -> None:
        profile = await self.candidate_repository.find_by_user_id(user_id)
        if profile:
            await self.candidate_repository.delete(profile.userId)