from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, BackgroundTasks
from app.models.session import CookingSession
from app.models.recipe import Recipe
from app.services.ai_mentor import AIMentorService
from datetime import datetime
import asyncio

class CookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIMentorService()
    
    async def start_session(self, recipe_id: str, user_id: str = None, demo_session_id: str = None, background_tasks: BackgroundTasks = None):
        # 1. Verify Recipe Exists
        recipe = await self.db.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        # 2. Create Session
        session = CookingSession(
            recipe_id=recipe_id,
            user_id=user_id,
            demo_session_id=demo_session_id,
            status="in_progress",
            current_step_index="0"
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        # 3. Prefetch Step 1 Guidance immediately
        if background_tasks:
            background_tasks.add_task(self._prefetch_guidance, str(session.id), 0)
        
        return session

    async def get_current_step(self, session_id: str):
        # Fetch session with recipe and steps
        result = await self.db.execute(
            select(CookingSession)
            .options(selectinload(CookingSession.recipe).selectinload(Recipe.steps))
            .where(CookingSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        current_index = int(session.current_step_index)
        steps = session.recipe.steps
        steps.sort(key=lambda x: x.step_number)
        
        if current_index >= len(steps):
            return {"message": "Recipe complete!", "is_last_step": True, "step_number": 999, "instruction": "Done!"}
            
        step = steps[current_index]
        
        # Check Cache
        guidance = session.next_step_guidance
        
        if not guidance:
            # Cache Miss: Fetch synchronously (slow)
            try:
                guidance = await self.ai.get_step_guidance(step.instruction)
            except:
                guidance = "No tips available."
        
        return {
            "step_number": step.step_number,
            "instruction": step.instruction,
            "expected_state": step.expected_state,
            "is_last_step": (current_index == len(steps) - 1),
            "guidance": guidance
        }

    async def advance_step(self, session_id: str, background_tasks: BackgroundTasks = None):
        session = await self.db.get(CookingSession, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        current = int(session.current_step_index)
        
        # Clear used guidance
        session.next_step_guidance = None
        session.current_step_index = str(current + 1)
        
        await self.db.commit()
        
        # Prefetch NEXT step (current + 1 is the new current, so we want guidance for that)
        # Actually, we want guidance for the step user JUST landed on.
        # Wait, if user clicks "Next", they land on Step 2. We want Step 2 guidance ready.
        # But we can't prefetch Step 2 BEFORE they click Next unless we do it during Step 1.
        # Correct Logic: During Step 1, prefetch Step 2.
        
        if background_tasks:
            # Prefetch the step AFTER the one we just landed on? 
            # No, users want guidance for the CURRENT step they are viewing.
            # So when we enter Step 2, we should have ALREADY prefetched Step 2's guidance during Step 1.
            
            # Trigger prefetch for Step 3 (index + 2) so it's ready for next time
            background_tasks.add_task(self._prefetch_guidance, session_id, current + 2)
        
        return await self.get_current_step(session_id)

    async def _prefetch_guidance(self, session_id: str, step_index: int):
        """Background task to fetch AI guidance for a future step"""
        # Create new DB session for background task
        from app.db.base import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            db_session = await session.get(CookingSession, session_id) # Re-fetch
            if not db_session: return
            
            # Load steps
            result = await session.execute(
                select(Recipe).where(Recipe.id == db_session.recipe_id).options(selectinload(Recipe.steps))
            )
            recipe = result.scalar_one()
            steps = sorted(recipe.steps, key=lambda x: x.step_number)
            
            if step_index < len(steps):
                step = steps[step_index]
                guidance = await self.ai.get_step_guidance(step.instruction)
                
                # Update DB
                db_session.next_step_guidance = guidance
                await session.commit()
                print(f"✨ Prefetched guidance for Step {step_index + 1}")
