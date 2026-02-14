from fastapi import APIRouter
from app.api.v1.endpoints import auth, recipes, cooking, failure, flavors, voice

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
api_router.include_router(cooking.router, prefix="/cooking", tags=["Cooking"])
api_router.include_router(failure.router, prefix="/failure", tags=["Failure Analysis"])
api_router.include_router(flavors.router, prefix="/flavors", tags=["Flavor Pairings"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice AI"])
