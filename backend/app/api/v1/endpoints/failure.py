from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.failure import FailureService

router = APIRouter()

@router.post("/analyze")
async def analyze_failure(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload image of failed dish for AI analysis"""
    service = FailureService(db)
    result = await service.analyze_upload(file)
    return result
