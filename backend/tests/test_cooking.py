import pytest
import pytest_asyncio
from app.models.recipe import Recipe, RecipeStep, DifficultyLevel
from app.models.session import CookingSession
from app.models.user import User
from app.services.cooking import CookingService
import uuid
from unittest.mock import AsyncMock, patch
from sqlalchemy import select

# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def seeded_recipe(db_session):
    """Create a recipe with steps for testing"""
    recipe = Recipe(
        id=uuid.uuid4(),
        title="Test Recipe",
        name="Test Recipe",
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=10,
        cook_time_minutes=20,
        total_time_minutes=30,
        servings=4
    )
    db_session.add(recipe)
    await db_session.flush()
    
    step1 = RecipeStep(id=uuid.uuid4(), recipe_id=recipe.id, step_number=1, instruction="Boil water", expected_state="Boiling")
    step2 = RecipeStep(id=uuid.uuid4(), recipe_id=recipe.id, step_number=2, instruction="Add noodles", expected_state="Soft")
    db_session.add_all([step1, step2])
    await db_session.commit()
    await db_session.refresh(recipe)
    return recipe

@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(email="testuser@example.com", name="Test User")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

# ============================================================================
# UNIT TESTS: CookingService
# ============================================================================

@pytest.mark.asyncio
async def test_cooking_service_starts_session(db_session, seeded_recipe, test_user):
    """Test that CookingService creates a new cooking session"""
    cooking_service = CookingService(db_session)
    session = await cooking_service.start_session(str(seeded_recipe.id), user_id=str(test_user.id))
    
    assert session is not None
    assert str(session.recipe_id) == str(seeded_recipe.id)
    assert str(session.user_id) == str(test_user.id)
    assert session.status == "in_progress"
    assert session.current_step_index == "0"

@pytest.mark.asyncio
async def test_cooking_service_get_current_step(db_session, seeded_recipe, test_user):
    """Test getting current step with AI guidance"""
    cooking_service = CookingService(db_session)
    
    # Create session
    session = await cooking_service.start_session(str(seeded_recipe.id), user_id=str(test_user.id))
    
    # Mock AI Mentor
    with patch("app.services.ai_mentor.AIMentorService.get_step_guidance", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "Great technique!"
        result = await cooking_service.get_current_step(str(session.id))
    
    assert result["step_number"] == 1
    assert result["instruction"] == "Boil water"
    assert result["expected_state"] == "Boiling"
    assert result["is_last_step"] is False
    assert result["guidance"] == "Great technique!"

@pytest.mark.asyncio
async def test_cooking_service_advance_step(db_session, seeded_recipe, test_user):
    """Test advancing to next step"""
    cooking_service = CookingService(db_session)
    
    # Create session
    session = await cooking_service.start_session(str(seeded_recipe.id), user_id=str(test_user.id))
    
    # Mock AI for both calls
    with patch("app.services.ai_mentor.AIMentorService.get_step_guidance", new_callable=AsyncMock) as mock_ai:
        mock_ai.return_value = "Good job!"
        result = await cooking_service.advance_step(str(session.id))
    
    assert result["step_number"] == 2
    assert result["instruction"] == "Add noodles"
    
    # Verify session was updated
    db_result = await db_session.execute(select(CookingSession).where(CookingSession.id == session.id))
    updated_session = db_result.scalar_one()
    assert updated_session.current_step_index == "1"

@pytest.mark.asyncio
async def test_cooking_service_handles_completion(db_session, seeded_recipe, test_user):
    """Test behavior when all steps are completed"""
    cooking_service = CookingService(db_session)
    
    # Create session at last step
    session = CookingSession(
        id=uuid.uuid4(),
        recipe_id=seeded_recipe.id,
        user_id=test_user.id,
        status="in_progress",
        current_step_index="2"  # Past last step (0-indexed, 2 steps total)
    )
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)
    
    result = await cooking_service.get_current_step(str(session.id))
    
    assert result["is_last_step"] is True
    assert "complete" in result["message"].lower()

# ============================================================================
# INTEGRATION TESTS: Cooking Endpoints (End-to-End Flow)
# ============================================================================

@pytest.mark.asyncio
async def test_cooking_flow_e2e(client, seeded_recipe):
    """Test complete cooking flow: Start -> Get Step -> Advance -> Complete"""
    # Mock the background prefetch to avoid hitting real database
    with patch("app.services.cooking.CookingService._prefetch_guidance", new_callable=AsyncMock):
        # 1. Start Session
        response = await client.post("/api/v1/cooking/start", json={"recipe_id": str(seeded_recipe.id)})
        assert response.status_code == 200
        session_data = response.json()
        session_id = session_data["id"]
        assert session_data["status"] == "in_progress"
    
        # 2. Get Current Step (Step 1)
        with patch("app.services.ai_mentor.AIMentorService.get_step_guidance", new_callable=AsyncMock) as mock_ai:
            mock_ai.return_value = "Careful with the hot water!"
            
            response = await client.get(f"/api/v1/cooking/{session_id}/current")
            assert response.status_code == 200
            step_data = response.json()
            assert step_data["step_number"] == 1
            assert step_data["instruction"] == "Boil water"
            assert step_data["is_last_step"] is False

        # 3. Next Step (Step 2)
        with patch("app.services.ai_mentor.AIMentorService.get_step_guidance", new_callable=AsyncMock) as mock_ai:
            mock_ai.return_value = "Stir well."
            
            response = await client.post(f"/api/v1/cooking/{session_id}/next")
            assert response.status_code == 200
            step_data = response.json()
            assert step_data["step_number"] == 2
            assert step_data["is_last_step"] is True

        # 4. Next Step (Complete)
        response = await client.post(f"/api/v1/cooking/{session_id}/next")
        assert response.status_code == 200
        result = response.json()
        assert "complete" in result["message"].lower() or result.get("is_last_step") is True
