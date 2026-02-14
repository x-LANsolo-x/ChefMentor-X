import google.generativeai as genai
from app.core.config import settings
import requests
from PIL import Image
from io import BytesIO
import asyncio
from functools import partial
import json

class AIVisionService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-2.5-flash which supports vision
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_dish_failure(self, image_url: str) -> dict:
        """
        Analyzes an image of a failed dish to determine what went wrong.
        """
        try:
            # 1. Fetch image from URL
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, image_url)
            image_data = Image.open(BytesIO(response.content))
            
            prompt = """Look at this failed dish.
1. Diagnose the root cause of the failure (e.g., burnt, undercooked, broken sauce, curdled).
2. Explain WHY it happened in 1-2 sentences.
3. Provide 2 specific, actionable tips to fix it next time.

Format your response as valid JSON:
{
    "root_cause": "brief diagnosis",
    "explanation": "why it happened",
    "tips": ["tip 1", "tip 2"]
}"""
            
            # Run AI analysis in thread pool
            ai_response = await loop.run_in_executor(
                None,
                partial(self.model.generate_content, [prompt, image_data])
            )
            
            # Parse JSON from response
            response_text = ai_response.text.strip()
            
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}, Response: {response_text if 'response_text' in locals() else 'N/A'}")
            return {
                "root_cause": "Analysis Complete",
                "explanation": ai_response.text if 'ai_response' in locals() else "Could not parse response",
                "tips": ["Review the full analysis above", "Try again with a clearer image"]
            }
        except Exception as e:
            print(f"Vision AI Error: {e}")
            return {
                "root_cause": "Analysis Failed",
                "explanation": f"Could not analyze the image: {str(e)}",
                "tips": ["Ensure image is clear and well-lit", "Try uploading a different angle"]
            }
