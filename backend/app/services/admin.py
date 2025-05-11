from typing import Optional
from app.repositories.admin import AdminRepository
from app.services.auth import AuthService
from app.models.user import AdminProfile
from app.schemas.admin import (
    AdminProfileRegisterRequest,
    AdminProfileSchema,
)
from app.schemas.auth import UserRegisterRequest
from app.core.enums import EntityType
from app.core.logging import get_logger
from app.core.exceptions import NotFoundException

logger = get_logger(__name__)

class AdminService:
    def __init__(self, admin_repository: AdminRepository, auth_service: AuthService):
        self.admin_repository = admin_repository
        self.auth_service = auth_service

    async def get_profile(self, user_id: str) -> Optional[AdminProfile]:
        return await self.admin_repository.find_by_user_id(user_id)

    async def register_admin(self, data: AdminProfileRegisterRequest) -> AdminProfileSchema:
        admin_auth_data = UserRegisterRequest(
            email=data.email,
            password=data.password,
            entity_type=EntityType.ADMIN,
        )
        user = await self.auth_service.register(admin_auth_data)
        admin = AdminProfile(
            userId=user.userId,
            email=data.email,
            full_name=data.name,
        )
        profile = await self.create_profile(admin)
        logger.info("Admin registered successfully.", admin_id=profile.userId, email=data.email)
        return AdminProfileSchema(**profile.model_dump())

    async def create_profile(self, admin: AdminProfile) -> AdminProfile:
        return await self.admin_repository.create(admin)

    async def delete_profile(self, user_id: str) -> None:
        profile = await self.admin_repository.find_by_user_id(user_id)
        if profile:
            await self.admin_repository.delete(profile.userId)
            await self.auth_service.delete_user_by_userId(user_id)
        else:
            raise NotFoundException(message="Profile not found", details={"user_id": user_id})
