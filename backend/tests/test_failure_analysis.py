"""
Tests for failure analysis endpoints and service.
"""
import pytest
from httpx import AsyncClient
from app.main import app
from io import BytesIO
from PIL import Image

@pytest.mark.asyncio
async def test_analyze_failure_without_auth():
    """Test that failure analysis requires authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        response = await client.post(
            "/api/v1/failure/analyze",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")},
            data={
                "dish_name": "Scrambled Eggs",
                "heat_level": "medium",
                "timing_issue": "overcooked"
            }
        )
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_analyze_failure_with_auth(authenticated_client):
    """Test failure analysis with authentication"""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    response = await authenticated_client.post(
        "/api/v1/failure/analyze",
        files={"file": ("test.jpg", img_bytes, "image/jpeg")},
        data={
            "dish_name": "Scrambled Eggs",
            "heat_level": "medium",
            "timing_issue": "overcooked",
            "modifications": "Added extra butter"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "root_cause" in data
    assert "severity" in data
    assert "explanation" in data
    assert "tips" in data
    assert data["severity"] in ["minor", "moderate", "major"]

@pytest.mark.asyncio
async def test_analyze_failure_invalid_image(authenticated_client):
    """Test failure analysis with invalid image"""
    response = await authenticated_client.post(
        "/api/v1/failure/analyze",
        files={"file": ("test.txt", BytesIO(b"not an image"), "text/plain")},
        data={
            "dish_name": "Scrambled Eggs",
            "heat_level": "medium"
        }
    )
    
    assert response.status_code in [400, 422]

@pytest.mark.asyncio
async def test_get_failure_history(authenticated_client):
    """Test retrieving failure analysis history"""
    response = await authenticated_client.get("/api/v1/failure/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
