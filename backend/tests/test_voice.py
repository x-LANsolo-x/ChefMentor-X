"""
Tests for voice endpoints (STT, TTS, command parsing).
"""
import pytest
from httpx import AsyncClient
from app.main import app
from io import BytesIO

@pytest.mark.asyncio
async def test_speech_to_text():
    """Test STT endpoint with mock audio"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create mock audio file
        audio_data = BytesIO(b"mock audio data")
        
        response = await client.post(
            "/api/v1/voice/stt",
            files={"file": ("audio.wav", audio_data, "audio/wav")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "text" in data

@pytest.mark.asyncio
async def test_voice_command_parsing():
    """Test voice command intent parsing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        test_cases = [
            ("next step", "NEXT"),
            ("go back", "PREV"),
            ("repeat that", "REPEAT"),
            ("set timer for 5 minutes", "TIMER"),
            ("pause", "PAUSE"),
            ("resume", "RESUME"),
            ("help", "HELP"),
        ]
        
        for text, expected_intent in test_cases:
            response = await client.post(
                "/api/v1/voice/command",
                json={"text": text}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "intent" in data
            assert data["intent"] == expected_intent

@pytest.mark.asyncio
async def test_text_to_speech():
    """Test TTS endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/voice/tts",
            json={"text": "Hello, this is a test"}
        )
        
        assert response.status_code == 200
        # Should return audio data
        assert response.headers["content-type"] == "audio/mp3"
