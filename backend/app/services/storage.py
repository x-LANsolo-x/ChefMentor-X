import cloudinary
import cloudinary.uploader
from app.core.config import settings
import asyncio
from functools import partial

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

class StorageService:
    @staticmethod
    async def upload_image(file_data) -> str:
        """Uploads image bytes to Cloudinary and returns the secure URL"""
        try:
            # Upload to Cloudinary (run in thread pool as it's synchronous)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(cloudinary.uploader.upload, file_data, folder="chefmentor_failures")
            )
            return response["secure_url"]
        except Exception as e:
            print(f"Cloudinary Upload Error: {e}")
            raise e
