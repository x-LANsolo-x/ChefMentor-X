"""
ChefMentor X - RecipeDB Integration Tests

Tests for external RecipeDB API integration.
"""
import pytest
from app.services.recipedb import RecipeDBService


class TestRecipeDBService:
    """Test RecipeDB API integration"""
    
    @pytest.fixture
    def recipedb_service(self):
        return RecipeDBService()
    
    @pytest.mark.asyncio
    async def test_search_recipes(self, recipedb_service):
        """Test recipe search"""
        result = await recipedb_service.search_recipes(page=1, limit=5)
        
        assert "recipes" in result
        assert isinstance(result["recipes"], list)
        assert "total" in result
        assert "page" in result
        assert result["page"] == 1
    
    @pytest.mark.asyncio
    async def test_search_with_query(self, recipedb_service):
        """Test recipe search with query term"""
        result = await recipedb_service.search_recipes(
            query="chicken",
            page=1,
            limit=5
        )
        
        assert "recipes" in result
        # Results should be related to chicken (if API works correctly)
    
    @pytest.mark.asyncio
    async def test_search_with_region_filter(self, recipedb_service):
        """Test recipe search with region filter"""
        result = await recipedb_service.search_recipes(
            region="Indian",
            page=1,
            limit=5
        )
        
        assert "recipes" in result
        assert isinstance(result["recipes"], list)
    
    @pytest.mark.asyncio
    async def test_get_recipe_by_name(self, recipedb_service):
        """Test getting recipe by name"""
        result = await recipedb_service.get_recipe_by_name("Butter Chicken")
        
        # May return None if not found, but should not error
        assert result is None or isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_error_handling(self, recipedb_service):
        """Test that errors are handled gracefully"""
        # Test with invalid parameters
        result = await recipedb_service.search_recipes(page=-1, limit=0)
        
        # Should return error structure, not crash
        assert "recipes" in result or "error" in result
