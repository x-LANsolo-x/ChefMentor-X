from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.models.recipe import Recipe
from app.services.recipedb import RecipeDBService

router = APIRouter()

@router.get("")
async def list_recipes(
    page: int = 1, 
    limit: int = 10,
    source: str = Query("local", enum=["local", "recipedb"]),
    db: AsyncSession = Depends(get_db)
):
    """
    List recipes.
    - source='local': Returns curated/seeded recipes from our DB.
    - source='recipedb': Proxies request to external RecipeDB API.
    """
    if source == "local":
        result = await db.execute(select(Recipe).limit(limit).offset((page-1)*limit))
        recipes = result.scalars().all()
        return {"source": "local", "data": recipes}
    
    else:
        # Call External API
        service = RecipeDBService()
        data = await service.search_recipes(page=page, limit=limit)
        return {"source": "recipedb", "data": data}

from app.services.flavordb import FlavorDBService

@router.get("/test-flavor/{ingredient}")
async def test_flavor(ingredient: str):
    """Temporary endpoint to test FlavorDB connection"""
    service = FlavorDBService()
    return await service.get_pairings(ingredient)

@router.get("/{recipe_id}")
async def get_recipe(recipe_id: str, db: AsyncSession = Depends(get_db)):
    """Get single recipe details from Local DB"""
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if recipe:
        return recipe
    return {"error": "Not found in local DB"}
