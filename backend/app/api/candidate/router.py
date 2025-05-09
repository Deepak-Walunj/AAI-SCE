from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from app.core.logging import get_logger
from app.schemas.candidate import CandidateProfileUpdate, CandidateProfileResponse,CandidateProfileRegisterRequest
from app.core.enums import EntityType, Gender
from app.services.candidate import CandidateService
from app.api.deps import get_candidate_service
from app.core.decorators import allowed_entities

router = APIRouter(prefix="/candidate", tags=["candidate"])

logger = get_logger(__name__)

@router.post("/register", response_model=CandidateProfileResponse)
async def register_candidate(
    request: Request,
    name: str = Form(..., message = "Full name of the user"),
    email: str = Form(..., message = "Valid email address"),
    gender: Gender = Form(..., message = "Gender (male, female, or other)"),
    password: str = Form(..., message = "Password must be at least 6 characters long", min_length = 6),
    candidate_service: CandidateService = Depends(get_candidate_service)
) -> CandidateProfileResponse:
    profile = await candidate_service.register_candidate(
        CandidateProfileRegisterRequest(
            name = name,
            email = email,
            gender = gender,
            password = password
        )
    )
    return CandidateProfileResponse(
        success=True,
        message="Profile created successfully",
        data=profile.model_dump()
    )
    
@router.get("/me", response_model=CandidateProfileResponse)
@allowed_entities([EntityType.CANDIDATE])
async def get_my_profile(
    request: Request,
    candidate_service: CandidateService = Depends(get_candidate_service)
) -> CandidateProfileResponse:
    profile = await candidate_service.get_profile(request.state.user.userId)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return CandidateProfileResponse(
        success=True,
        message="Profile retrieved successfully",
        data=profile.model_dump()
    )
    
@router.put("/me", response_model=CandidateProfileResponse)
@allowed_entities([EntityType.CANDIDATE])
async def update_my_profile(
    request: Request,
    data: CandidateProfileUpdate,
    candidate_service: CandidateService = Depends(get_candidate_service)
) -> CandidateProfileResponse:
    profile = await candidate_service.update_profile(request.state.user.userId, data)
    return CandidateProfileResponse(
        success=True,
        message="Profile updated successfully",
        data=profile.model_dump()
    )
    

@router.delete("/me", response_model=None)
@allowed_entities([EntityType.CANDIDATE])
async def delete_my_profile(
    request: Request,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    await candidate_service.delete_profile(request.state.user.userId)
    return None