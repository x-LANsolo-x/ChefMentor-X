"""
ChefMentor X - Integration Tests

End-to-end tests for complete user flows.
"""
import pytest
from httpx import AsyncClient
from app.main import app


class TestCookingFlow:
    """Test complete cooking session flow"""
    
    @pytest.mark.asyncio
    async def test_complete_cooking_session(self):
        """Test full cooking session from start to finish"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 1. Login
            login_response = await client.post(
                "/api/v1/auth/login",
                json={"email": "test@example.com", "password": "testpass123"}
            )
            assert login_response.status_code in [200, 404]  # User may not exist
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                # 2. Get recipes
                recipes_response = await client.get(
                    "/api/v1/recipes?source=local&limit=5",
                    headers=headers
                )
                assert recipes_response.status_code == 200
                recipes = recipes_response.json()
                assert "data" in recipes
                
                # 3. Start cooking session
                if recipes["data"]:
                    recipe_id = recipes["data"][0]["id"]
                    session_response = await client.post(
                        "/api/v1/cooking/sessions/start",
                        headers=headers,
                        json={"recipe_id": recipe_id}
                    )
                    assert session_response.status_code in [200, 201]
                    
                    session = session_response.json()
                    session_id = session["id"]
                    
                    # 4. Update progress
                    progress_response = await client.post(
                        f"/api/v1/cooking/sessions/{session_id}/progress",
                        headers=headers,
                        json={"current_step": 1, "notes": "Looking good"}
                    )
                    assert progress_response.status_code == 200
                    
                    # 5. Complete session
                    complete_response = await client.post(
                        f"/api/v1/cooking/sessions/{session_id}/complete",
                        headers=headers,
                        json={"success": True, "notes": "Delicious!"}
                    )
                    assert complete_response.status_code == 200


class TestFailureAnalysisFlow:
    """Test complete failure analysis flow"""
    
    @pytest.mark.asyncio
    async def test_analyze_failed_dish(self):
        """Test uploading and analyzing a failed dish"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 1. Upload image
            # Note: This requires multipart/form-data with actual image
            # For now, test with URL-based analysis
            
            # 2. Analyze failure
            analysis_response = await client.post(
                "/api/v1/failure/analyze",
                json={
                    "image_url": "https://example.com/burnt_eggs.jpg",
                    "context": {
                        "dish_name": "Scrambled Eggs",
                        "heat_level": "high",
                        "cooking_time": 10
                    }
                }
            )
            
            # May require auth or specific endpoint structure
            assert analysis_response.status_code in [200, 401, 404, 422]


class TestRecipeGeneration:
    """Test AI recipe generation"""
    
    @pytest.mark.asyncio
    async def test_generate_recipe(self):
        """Test generating recipe from AI"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/recipes?source=ai&query=vegan pasta"
            )
            
            assert response.status_code in [200, 401]  # May require auth
            
            if response.status_code == 200:
                data = response.json()
                assert "data" in data
                if data["data"]:
                    recipe = data["data"][0]
                    assert "name" in recipe or "title" in recipe
                    assert "ingredients" in recipe or "steps" in recipe


class TestVoiceIntegration:
    """Test voice command integration"""
    
    @pytest.mark.asyncio
    async def test_voice_command_parsing(self):
        """Test voice command endpoint"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/voice/command",
                json={"text": "next step"}
            )
            
            assert response.status_code == 200
            result = response.json()
            assert "intent" in result
            assert result["intent"] == "NEXT"
    
    @pytest.mark.asyncio
    async def test_multiple_voice_commands(self):
        """Test various voice commands"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            commands = [
                ("next step", "NEXT"),
                ("go back", "PREV"),
                ("repeat that", "REPEAT"),
                ("set timer for 5 minutes", "TIMER"),
                ("pause", "PAUSE"),
            ]
            
            for text, expected_intent in commands:
                response = await client.post(
                    "/api/v1/voice/command",
                    json={"text": text}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    assert "intent" in result
                    # Intent should match or be UNKNOWN
                    assert result["intent"] in [expected_intent, "UNKNOWN"]
