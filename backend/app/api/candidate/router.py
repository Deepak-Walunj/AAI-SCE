from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from app.core.logging import get_logger
from app.schemas.candidate import (
    CandidateProfileUpdate, 
    CandidateProfileResponse,
    CandidateProfileRegisterRequest, 
    CandidateProcessResponse, 
    CandidateProcessData,
    )
from app.core.enums import EntityType, Gender
from app.services.candidate import CandidateService
from app.api.deps import get_candidate_service
from app.core.decorators import allowed_entities

router = APIRouter(prefix="/candidate", tags=["candidate"])

logger = get_logger(__name__)

@router.post("/register", response_model=CandidateProfileResponse)
async def register_candidate(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    gender: Gender = Form(...),
    password: str = Form(..., min_length=6),
    candidate_service: CandidateService = Depends(get_candidate_service)) -> CandidateProfileResponse:
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
    await candidate_service.update_profile(request.state.user.userId, data)
    return CandidateProfileResponse(
        success=True,
        message="Profile updated successfully",
    )
    

@router.delete("/me", response_model=None)
@allowed_entities([EntityType.CANDIDATE])
async def delete_my_profile(
    request: Request,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    await candidate_service.delete_profile(request.state.user.userId)
    return CandidateProfileResponse(
        success=True,
        message="Profile deleted successfully",
    )
    
@router.post("/process", response_model=CandidateProcessResponse)
@allowed_entities([EntityType.CANDIDATE])
async def process_text(
    request: Request,
    data: CandidateProcessData,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    result=await candidate_service.get_process_output(request.state.user.userId, data)
    return CandidateProcessResponse(
        success=True,
        message="Text processed successfully",
        result=result
    )