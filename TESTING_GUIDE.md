# 🧪 ChefMentor X - Testing Guide

## Table of Contents
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Integration Testing](#integration-testing)
- [Manual Testing](#manual-testing)
- [Performance Testing](#performance-testing)

---

## Backend Testing

### Setup

```bash
cd backend

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Structure

```
backend/tests/
├── conftest.py              # Pytest fixtures
├── test_auth.py            # Authentication tests
├── test_recipes.py         # Recipe API tests
├── test_cooking.py         # Cooking session tests
├── test_voice.py           # Voice service tests
├── test_failure_analysis.py # AI failure analysis tests
├── test_recipedb.py        # External API tests
└── test_integration.py     # End-to-end tests
```

### Running Specific Tests

```bash
# Test specific file
pytest tests/test_auth.py -v

# Test specific function
pytest tests/test_auth.py::test_login -v

# Test with markers
pytest -m "not slow" -v

# Run only integration tests
pytest tests/test_integration.py -v
```

### Writing Tests

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_recipe():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/recipes",
            json={"name": "Test Recipe", "difficulty": "BEGINNER"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Recipe"
```

---

## Frontend Testing

### Setup

```bash
cd frontend-v1

# Install test dependencies
npm install

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Test Structure (if implemented)

```
frontend-v1/src/
├── components/__tests__/
│   ├── Button.test.tsx
│   └── Card.test.tsx
├── screens/__tests__/
│   ├── LoginScreen.test.tsx
│   └── RecipeListScreen.test.tsx
└── services/__tests__/
    └── apiClient.test.ts
```

### Component Testing Example

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import Button from '../components/Button';

describe('Button', () => {
  it('renders correctly', () => {
    const { getByText } = render(<Button title="Click me" />);
    expect(getByText('Click me')).toBeTruthy();
  });

  it('handles press event', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button title="Click me" onPress={onPress} />
    );
    
    fireEvent.press(getByText('Click me'));
    expect(onPress).toHaveBeenCalled();
  });
});
```

---

## Integration Testing

### Full User Flow Tests

```bash
# Start backend server
cd backend
uvicorn app.main:app --reload

# In another terminal, run integration tests
pytest tests/test_integration.py -v
```

### Test Scenarios

1. **Complete Cooking Session**
   - Login
   - Browse recipes
   - Start cooking session
   - Navigate through steps
   - Complete session

2. **Failure Analysis Flow**
   - Upload dish photo
   - Answer context questions
   - Receive AI diagnosis
   - View recommendations

3. **Voice Command Flow**
   - Start cooking
   - Send voice commands
   - Verify step navigation
   - Test timer commands

---

## Manual Testing

### Backend API Testing (Postman/Thunder Client)

#### 1. Import Collection
- Import `FlavorDB API - Complete Collection.postman_collection.json`
- Set environment variables:
  - `BASE_URL`: http://localhost:8000
  - `TOKEN`: (from login response)

#### 2. Test Endpoints

**Authentication:**
```bash
# Register
POST /api/v1/auth/register
{
  "email": "test@example.com",
  "password": "testpass123",
  "full_name": "Test User"
}

# Login
POST /api/v1/auth/login
{
  "email": "test@example.com",
  "password": "testpass123"
}
```

**Recipes:**
```bash
# List recipes (local)
GET /api/v1/recipes?source=local&limit=10

# List recipes (RecipeDB)
GET /api/v1/recipes?source=recipedb&query=pasta&limit=5

# Generate recipe (AI)
GET /api/v1/recipes?source=ai&query=vegan burger
```

**Cooking Sessions:**
```bash
# Start session
POST /api/v1/cooking/sessions/start
{
  "recipe_id": "uuid-here"
}

# Update progress
POST /api/v1/cooking/sessions/{session_id}/progress
{
  "current_step": 2,
  "notes": "Going well"
}
```

**Voice Commands:**
```bash
# Parse command
POST /api/v1/voice/command
{
  "text": "next step"
}
```

### Mobile App Testing

#### 1. Run on iOS Simulator
```bash
cd frontend-v1
npm run ios
```

#### 2. Run on Android Emulator
```bash
cd frontend-v1
npm run android
```

#### 3. Test on Physical Device
```bash
cd frontend-v1
npx expo start

# Scan QR code with Expo Go app
```

### Manual Test Checklist

**Authentication:**
- [ ] Register new user
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Logout
- [ ] Token refresh

**Recipe Browsing:**
- [ ] Load recipe list (local)
- [ ] Load recipe list (RecipeDB)
- [ ] Search recipes
- [ ] View recipe details
- [ ] Generate AI recipe

**Cooking Session:**
- [ ] Start cooking session
- [ ] Navigate through steps
- [ ] Use voice commands
- [ ] Set timers
- [ ] Pause/resume session
- [ ] Complete session

**Failure Analysis:**
- [ ] Take photo with camera
- [ ] Upload photo from gallery
- [ ] Answer context questions
- [ ] View AI diagnosis
- [ ] Save analysis results

**Voice Interaction:**
- [ ] Enable microphone
- [ ] Record voice command
- [ ] Process "next step"
- [ ] Process "set timer"
- [ ] Process "repeat"

**Settings:**
- [ ] Update voice speed
- [ ] Toggle beginner mode
- [ ] Enable/disable notifications
- [ ] View profile
- [ ] Logout

---

## Performance Testing

### Load Testing with Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class ChefMentorUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def list_recipes(self):
        self.client.get("/api/v1/recipes?source=local&limit=10", 
                       headers=self.headers)
    
    @task(2)
    def get_recipe(self):
        self.client.get("/api/v1/recipes/some-id", 
                       headers=self.headers)
    
    @task(1)
    def voice_command(self):
        self.client.post("/api/v1/voice/command",
                        json={"text": "next step"},
                        headers=self.headers)
```

Run load test:
```bash
# Install locust
pip install locust

# Run test
locust -f locustfile.py --host=http://localhost:8000

# Open browser
open http://localhost:8089
```

### Performance Benchmarks

**Target Metrics:**
- API response time: < 200ms (95th percentile)
- Database queries: < 100ms
- AI generation: < 5s
- Voice transcription: < 2s
- Image upload: < 3s

---

## Continuous Testing

### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/, --tb=short]
```

### CI Pipeline

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Test Coverage Goals

- **Backend**: 80%+ coverage
- **Critical paths**: 95%+ coverage
- **API endpoints**: 100% coverage
- **Authentication**: 100% coverage
- **Database models**: 90%+ coverage

---

## Debugging Tests

```bash
# Run with debug output
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Drop into debugger on failure
pytest tests/ --pdb
```

---

## Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **React Native Testing**: https://reactnative.dev/docs/testing-overview
- **Expo Testing**: https://docs.expo.dev/develop/unit-testing/
- **API Testing**: https://www.postman.com/
