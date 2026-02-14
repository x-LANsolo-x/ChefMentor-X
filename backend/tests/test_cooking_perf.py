import pytest
import pytest_asyncio
from app.services.cooking import CookingService
from app.models.recipe import Recipe, RecipeStep
from fastapi import BackgroundTasks
import uuid
from unittest.mock import AsyncMock, patch

@pytest_asyncio.fixture
async def fast_recipe(db_session):
    from app.models.recipe import DifficultyLevel
    recipe = Recipe(
        id=uuid.uuid4(), 
        title="Fast Food",
        name="Fast Food", 
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=5,
        total_time_minutes=5,
        servings=1
    )
    db_session.add(recipe)
    await db_session.flush()
    
    # 3 Steps to test flow: 1 -> 2 -> 3
    s1 = RecipeStep(id=uuid.uuid4(), recipe_id=recipe.id, step_number=1, instruction="Step 1")
    s2 = RecipeStep(id=uuid.uuid4(), recipe_id=recipe.id, step_number=2, instruction="Step 2")
    s3 = RecipeStep(id=uuid.uuid4(), recipe_id=recipe.id, step_number=3, instruction="Step 3")
    db_session.add_all([s1, s2, s3])
    await db_session.commit()
    return recipe

@pytest.mark.asyncio  
async def test_speculative_caching(db_session, fast_recipe):
    """
    Test that speculative caching works: 
    - Starting session prefetches Step 1 guidance
    - Advancing to Step 2 prefetches Step 3 guidance
    - Cached guidance is used instead of calling AI again
    """
    
    # Mock BOTH the AI service AND the background task's DB session
    with patch("app.services.ai_mentor.AIMentorService.get_step_guidance", new_callable=AsyncMock) as mock_ai, \
         patch("app.db.base.AsyncSessionLocal") as mock_session_factory:
        
        # Configure the mock to return our test db_session
        mock_session_factory.return_value.__aenter__.return_value = db_session
        
        mock_ai.return_value = "AI_TIP_FOR_STEP_1"
        
        service = CookingService(db_session)
        bg_tasks = BackgroundTasks()
        
        # 1. Start Session
        session = await service.start_session(str(fast_recipe.id), background_tasks=bg_tasks)
        
        # Manually execute the background task (in real FastAPI, happens after response)
        for task in bg_tasks.tasks:
            await task()
            
        # 2. Refresh Session from DB to check if cache was updated
        await db_session.refresh(session)
        assert session.next_step_guidance == "AI_TIP_FOR_STEP_1", "Step 1 guidance should be cached"
        
        # 3. Get Current Step (Should use cache without calling AI)
        step_data = await service.get_current_step(str(session.id))
        assert step_data["guidance"] == "AI_TIP_FOR_STEP_1", "Should return cached guidance"
        assert step_data["step_number"] == 1
        
        # 4. Advance Step - Should clear cache and prefetch next
        mock_ai.return_value = "AI_TIP_FOR_STEP_3"  # Mock for Step 3 (current+2)
        bg_tasks_next = BackgroundTasks()
        
        new_step_data = await service.advance_step(str(session.id), background_tasks=bg_tasks_next)
        
        # Verify we moved to Step 2
        assert new_step_data["step_number"] == 2
        
        # Cache should be cleared after advancing
        await db_session.refresh(session)
        assert session.next_step_guidance is None, "Cache should be cleared after use"
        
        # Execute background task (prefetching Step 3)
        for task in bg_tasks_next.tasks:
            await task()
            
        # Verify Step 3 guidance is now cached
        await db_session.refresh(session)
        assert session.next_step_guidance == "AI_TIP_FOR_STEP_3", "Step 3 guidance should be prefetched"
