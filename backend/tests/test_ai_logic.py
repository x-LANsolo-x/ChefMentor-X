import pytest
from unittest.mock import AsyncMock, patch
from app.services.recipe_generator import RecipeGeneratorService
from app.services.ai_mentor import AIMentorService

@pytest.mark.asyncio
async def test_recipe_generation_logic(db_session):
    # Mock Gemini response
    mock_json = """
    {
        "name": "AI Tacos",
        "difficulty": "easy",
        "estimated_time_min": 20,
        "steps": [
            {"step_number": 1, "instruction": "Fry meat", "expected_state": "Browned"}
        ]
    }
    """
    
    with patch("google.generativeai.GenerativeModel.generate_content_async", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value.text = mock_json
        
        service = RecipeGeneratorService(db_session)
        recipe = await service.generate_from_name("Tacos")
        
        # Refresh to load relationships
        await db_session.refresh(recipe)
        
        # Verify it was saved to DB
        assert recipe.title == "AI Tacos" or recipe.name == "AI Tacos"
        assert recipe.ai_generated is True
        
        # Load steps explicitly
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from app.models.recipe import Recipe as RecipeModel
        result = await db_session.execute(
            select(RecipeModel).where(RecipeModel.id == recipe.id).options(selectinload(RecipeModel.steps))
        )
        recipe_with_steps = result.scalar_one()
        assert len(recipe_with_steps.steps) == 1
        assert recipe_with_steps.steps[0].instruction == "Fry meat"

@pytest.mark.asyncio
async def test_voice_intent_parsing():
    # Mock Gemini for Intent
    mock_json = '{"intent": "TIMER", "duration_seconds": 300}'
    
    # Note: The service runs synchronous code in a thread pool, so we mock generate_content
    with patch("google.generativeai.GenerativeModel.generate_content") as mock_gen:
        mock_gen.return_value.text = mock_json
        
        service = AIMentorService()
        result = await service.parse_voice_intent("Set timer for 5 mins")
        
        assert result["intent"] == "TIMER"
        assert result["duration_seconds"] == 300
