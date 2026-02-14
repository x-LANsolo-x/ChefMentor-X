import io
from gtts import gTTS
from groq import Groq
from app.core.config import settings

class VoiceService:
    def __init__(self):
        self.groq = Groq(api_key=settings.GROQ_API_KEY)

    async def speech_to_text(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """
        Transcribes audio using Groq (Whisper).
        """
        try:
            # Groq API expects a tuple (filename, file_content)
            transcription = self.groq.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model="whisper-large-v3",
                response_format="json",
                language="en",
                temperature=0.0
            )
            return transcription.text
        except Exception as e:
            print(f"STT Error: {e}")
            return ""

    async def text_to_speech(self, text: str) -> io.BytesIO:
        """
        Converts text to speech using Google TTS.
        Returns bytes buffer of MP3 audio.
        """
        try:
            import asyncio
            from functools import partial
            
            # Create a BytesIO buffer to hold the MP3 data in memory
            mp3_fp = io.BytesIO()
            
            # Generate speech (run in thread pool since gTTS is synchronous)
            loop = asyncio.get_event_loop()
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Write to buffer in thread pool
            await loop.run_in_executor(None, partial(tts.write_to_fp, mp3_fp))
            
            # Reset buffer position to the beginning
            mp3_fp.seek(0)
            return mp3_fp
        except Exception as e:
            print(f"TTS Error: {e}")
            import traceback
            traceback.print_exc()
            return None
