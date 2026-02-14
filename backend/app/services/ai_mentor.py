import google.generativeai as genai
from app.core.config import settings
import asyncio
from functools import partial

class AIMentorService:
    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def get_step_guidance(self, step_instruction: str) -> str:
        """
        Generates a short, helpful mentoring tip for the current cooking step.
        """
        try:
            prompt = f"""You are a professional chef mentor. 
The user is on this step: "{step_instruction}".

Give one short, encouraging tip (max 20 words) to help them succeed at this specific step. 
Focus on technique or sensory cues (smell, look).
Do not repeat the instruction."""
            
            # Run synchronous API call in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                partial(self.model.generate_content, prompt)
            )
            return response.text.strip()
        except Exception as e:
            print(f"AI Error: {e}")
            return "Keep going, you're doing great!"
