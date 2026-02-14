import httpx
from app.core.config import settings

class FlavorDBService:
    BASE_URL = "http://cosylab.iiitd.edu.in:6969/flavordb"
    
    def __init__(self):
        # Assuming we have a token, if not we might scrape or skip auth if public
        self.auth_token = settings.FLAVOR_DB_API_KEY 
        
    async def get_pairings(self, ingredient: str) -> list:
        """Find flavor pairings for an ingredient"""
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/food/by-alias",
                    params={"food_pair": ingredient},
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"FlavorDB Error: {str(e)}")
                return []
