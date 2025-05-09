from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from app.core.logging import get_logger
from app.schemas.admin import AdminProfileRegisterRequest, AdminProfileResponse
from app.services.admin import AdminService
from app.api.deps import get_admin_service
from app.core.enums import EntityType
from app.core.decorators import allowed_entities

router = APIRouter(prefix="/admin", tags=["admin"])

logger = get_logger(__name__)

@router.post("/register", response_model=AdminProfileResponse)
async def register_admin(
    request: Request,
    name: str = Form(..., message="Full name of the admin"),
    email: str = Form(..., message="Valid email address"),
    password: str = Form(..., message="Password must be at least 6 characters long", min_length=6),
    admin_service: AdminService = Depends(get_admin_service)) -> AdminProfileResponse:
    profile = await admin_service.register_admin(
        AdminProfileRegisterRequest(
            name=name,
            email=email,
            password=password
        )
    )
    return AdminProfileResponse(
        success=True,
        message="Admin profile created successfully",
        data=profile.model_dump()
    )

@router.get("/me", response_model=AdminProfileResponse)
@allowed_entities([EntityType.ADMIN])
async def get_my_profile(
    request: Request,
    admin_service: AdminService = Depends(get_admin_service)
) -> AdminProfileResponse:
    profile = await admin_service.get_profile(request.state.user.userId)
    print("User ID from token:", request.state.user.userId)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return AdminProfileResponse(
        success=True,
        message="Profile retrieved successfully",
        data=profile.model_dump()
    )

@router.delete("/me", response_model=None)
@allowed_entities([EntityType.ADMIN])
async def delete_my_profile(
    request: Request,
    admin_service: AdminService = Depends(get_admin_service)
):
    await admin_service.delete_profile(request.state.user.userId)
    return AdminProfileResponse(
        success=True,
        message="Profile deleted successfully",
    )
