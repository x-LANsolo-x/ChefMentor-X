import pytest
from app.core.security import create_access_token, verify_token
from app.services.auth import AuthService
from app.models.user import User
from unittest.mock import patch, MagicMock
from sqlalchemy import select

# ============================================================================
# UNIT TESTS: Security Functions (JWT)
# ============================================================================

@pytest.mark.asyncio
async def test_jwt_generation_and_verification():
    """Test JWT token creation and verification"""
    data = {"sub": "testuser", "email": "test@example.com"}
    token = create_access_token(data)
    assert token is not None
    
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "testuser"
    assert payload["email"] == "test@example.com"

def test_verify_invalid_token():
    """Test JWT verification with invalid token"""
    payload = verify_token("invalid.token.here")
    assert payload is None

# ============================================================================
# UNIT TESTS: AuthService
# ============================================================================

@pytest.mark.asyncio
async def test_auth_service_creates_new_user(db_session):
    """Test that AuthService creates a new user on first login"""
    auth_service = AuthService(db_session)
    
    # Mock Google's token verification
    mock_idinfo = {
        "email": "newuser@gmail.com",
        "name": "New User",
        "sub": "google123456"
    }
    
    with patch('app.services.auth.id_token.verify_oauth2_token', return_value=mock_idinfo):
        result = await auth_service.google_login("mock_google_token")
    
    # Verify response structure
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["email"] == "newuser@gmail.com"
    assert result["name"] == "New User"
    
    # Verify user was created in database
    db_result = await db_session.execute(select(User).where(User.email == "newuser@gmail.com"))
    user = db_result.scalar_one_or_none()
    assert user is not None
    assert user.name == "New User"

@pytest.mark.asyncio
async def test_auth_service_returns_existing_user(db_session):
    """Test that AuthService returns existing user on subsequent logins"""
    # Create existing user
    existing_user = User(email="existing@gmail.com", name="Existing User")
    db_session.add(existing_user)
    await db_session.commit()
    await db_session.refresh(existing_user)
    
    auth_service = AuthService(db_session)
    
    # Mock Google's token verification
    mock_idinfo = {
        "email": "existing@gmail.com",
        "name": "Existing User",
        "sub": "google123456"
    }
    
    with patch('app.services.auth.id_token.verify_oauth2_token', return_value=mock_idinfo):
        result = await auth_service.google_login("mock_google_token")
    
    # Verify response
    assert result["email"] == "existing@gmail.com"
    assert result["user_id"] == str(existing_user.id)
    
    # Verify no duplicate user was created
    db_result = await db_session.execute(select(User).where(User.email == "existing@gmail.com"))
    users = db_result.scalars().all()
    assert len(users) == 1  # Only one user should exist

# ============================================================================
# INTEGRATION TESTS: Auth Endpoints
# ============================================================================

@pytest.mark.asyncio
async def test_google_login_endpoint(client):
    """Test /auth/google endpoint with mocked Google verification"""
    # Mock the Google ID token verification
    with patch("app.services.auth.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = {
            "email": "newuser@example.com",
            "name": "New User",
            "sub": "google_123",
            "aud": "MY_CLIENT_ID",
            "iss": "accounts.google.com"
        }
        
        # We also need to mock settings.GOOGLE_CLIENT_ID to match
        with patch("app.core.config.settings.GOOGLE_CLIENT_ID", "MY_CLIENT_ID"):
            response = await client.post("/api/v1/auth/google", json={"id_token": "fake_token"})
            
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["email"] == "newuser@example.com"
            assert data["name"] == "New User"

@pytest.mark.asyncio
async def test_google_login_endpoint_existing_user(client, db_session):
    """Test login with existing user doesn't create duplicates"""
    # Create existing user
    existing_user = User(email="repeat@example.com", name="Repeat User")
    db_session.add(existing_user)
    await db_session.commit()
    
    with patch("app.services.auth.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = {
            "email": "repeat@example.com",
            "name": "Repeat User",
            "sub": "google_456"
        }
        
        response = await client.post("/api/v1/auth/google", json={"id_token": "fake_token"})
        assert response.status_code == 200
        
        # Verify no duplicate created
        db_result = await db_session.execute(select(User).where(User.email == "repeat@example.com"))
        users = db_result.scalars().all()
        assert len(users) == 1
