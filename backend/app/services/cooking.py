from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models.session import CookingSession
from app.models.recipe import Recipe
from app.services.ai_mentor import AIMentorService
from datetime import datetime

class CookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIMentorService()
    
    async def start_session(self, recipe_id: int, user_id: int = None, is_demo: bool = False):
        # 1. Verify Recipe Exists
        recipe = await self.db.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        # 2. If demo mode and no user_id, use demo user (ID: 3)
        if is_demo and user_id is None:
            user_id = 3  # Demo user created in seed
            
        if user_id is None:
            raise HTTPException(status_code=400, detail="user_id is required for authenticated sessions")
            
        # 3. Create Session
        session = CookingSession(
            recipe_id=recipe_id,
            user_id=user_id,
            is_demo=is_demo,
            status="IN_PROGRESS",
            current_step=0
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        return session

    async def get_current_step(self, session_id: int):
        # Fetch session with recipe and steps
        result = await self.db.execute(
            select(CookingSession)
            .options(selectinload(CookingSession.recipe).selectinload(Recipe.steps))
            .where(CookingSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        current_index = session.current_step
        steps = session.recipe.steps
        
        # Sort steps to be safe
        steps.sort(key=lambda x: x.step_number)
        
        if current_index >= len(steps):
            return {"message": "Recipe complete!", "is_last_step": True, "step_number": current_index, "instruction": "All done!", "guidance": "Congratulations! You've completed the recipe!"}
            
        step = steps[current_index]
        
        # Get AI Guidance (with error handling)
        guidance = "Keep going, you're doing great!"
        try:
            guidance = await self.ai.get_step_guidance(step.instruction)
        except Exception as e:
            print(f"AI Service Skipped: {e}")
        
        return {
            "step_number": step.step_number,
            "instruction": step.instruction,
            "expected_state": getattr(step, 'expected_state', None),
            "is_last_step": (current_index == len(steps) - 1),
            "guidance": guidance
        }

    async def advance_step(self, session_id: int):
        session = await self.db.get(CookingSession, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        session.current_step = session.current_step + 1
        await self.db.commit()
        await self.db.refresh(session)  # Refresh to get updated value
        
        # Expire all cached instances to ensure fresh data
        self.db.expire_all()
        
        return await self.get_current_step(session_id)
