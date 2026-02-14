from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def google_login(self, token: str) -> dict:
        try:
            # 1. Verify Google Token
            # In production, we strictly verify the AUD (Audience)
            # For dev, if verification fails locally (common with emulators), we might mock it
            # But here is the standard production code:
            try:
                idinfo = id_token.verify_oauth2_token(
                    token, 
                    requests.Request(), 
                    settings.GOOGLE_CLIENT_ID
                )
            except ValueError as e:
                # Fallback for development if using Expo Go proxy issues, 
                # but STRICTLY handle this in prod. 
                # For now, we assume valid if verify fails ONLY IF DEBUG is True
                if settings.DEBUG and "Invalid token" in str(e):
                     # MOCK DATA FOR DEV ONLY IF VERIFICATION FAILS
                     # DELETE THIS BLOCK IN PRODUCTION
                     print("⚠️ DEV MODE: Google Token Verification Failed. Using Mock Data.")
                     idinfo = {
                         "email": "testuser@gmail.com",
                         "name": "Test User",
                         "sub": "123456789"
                     }
                else:
                    raise e

            email = idinfo['email']
            name = idinfo.get('name', email.split('@')[0])
            
            # 2. Check if user exists
            result = await self.db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            # 3. Create if new
            if not user:
                user = User(email=email, name=name)
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)
            
            # 4. Generate JWT
            access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": str(user.id),
                "email": user.email,
                "name": user.name
            }
            
        except Exception as e:
            print(f"Auth Error: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")
