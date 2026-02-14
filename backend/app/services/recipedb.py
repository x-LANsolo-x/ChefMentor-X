import httpx
from app.core.config import settings
from typing import List, Optional

class RecipeDBService:
    BASE_URL = "http://cosylab.iiitd.edu/recipe2-api"
    
    def __init__(self):
        self.api_key = settings.RECIPE_DB_API_KEY
        
    async def search_recipes(self, page: int = 1, limit: int = 10) -> dict:
        """Fetch recipes from RecipeDB"""
        # Note: RecipeDB auth is Bearer token in header
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # The endpoint playground suggests /recipe/recipesinfo
                response = await client.get(
                    f"{self.BASE_URL}/recipe/recipesinfo",
                    params={"page": page, "limit": limit},
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"RecipeDB Error: {str(e)}")
                return {"error": str(e), "data": []}

    async def get_recipe_by_id(self, recipe_id: str) -> dict:
        """Get single recipe details - Note: API doesn't seem to have direct ID endpoint in list, 
           we might need to filter or use title search if ID lookup isn't standard."""
        # For now, we return empty or implement title search fallback
        pass
