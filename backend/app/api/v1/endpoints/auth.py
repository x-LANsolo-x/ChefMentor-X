from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas.auth import GoogleAuthRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter()

@router.post("/google", response_model=TokenResponse)
async def google_login(
    auth_data: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Exchange Google ID Token for App JWT Token.
    Creates user if they don't exist.
    """
    auth_service = AuthService(db)
    return await auth_service.google_login(auth_data.id_token)
