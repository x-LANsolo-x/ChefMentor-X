# 🔌 ChefMentor X - API Reference

Complete API documentation for all endpoints.

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.yourdomain.com/api/v1
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-02-15T10:00:00Z"
}
```

### Login

**POST** `/auth/login`

Authenticate and receive access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

### Get Current User

**GET** `/auth/me`

Get currently authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "skill_level": "INTERMEDIATE",
  "created_at": "2026-02-15T10:00:00Z"
}
```

---

## Recipe Endpoints

### List Recipes

**GET** `/recipes`

Get list of recipes from various sources.

**Query Parameters:**
- `source` (string): `local`, `recipedb`, or `ai` (default: `local`)
- `query` (string): Search term (required for `ai` source)
- `page` (int): Page number (default: 1)
- `limit` (int): Results per page (default: 10)

**Examples:**
```bash
# Local recipes
GET /recipes?source=local&limit=20

# Search RecipeDB
GET /recipes?source=recipedb&query=pasta&limit=10

# Generate AI recipe
GET /recipes?source=ai&query=vegan burger
```

**Response (200):**
```json
{
  "source": "local",
  "data": [
    {
      "id": "uuid-here",
      "name": "Perfect Scrambled Eggs",
      "description": "Creamy, fluffy scrambled eggs",
      "difficulty": "BEGINNER",
      "prep_time_minutes": 5,
      "cook_time_minutes": 10,
      "servings": 2,
      "image_url": "https://...",
      "ingredients": ["4 eggs", "1 tbsp butter", "salt", "pepper"],
      "steps": [
        {
          "step_number": 1,
          "title": "Whisk Eggs",
          "instruction": "Crack eggs and whisk...",
          "duration_minutes": 1,
          "ai_tips": "Whisk until frothy for fluffier eggs"
        }
      ],
      "tags": ["breakfast", "quick", "easy"]
    }
  ],
  "total": 50
}
```

### Get Recipe by ID

**GET** `/recipes/{recipe_id}`

Get detailed information for a specific recipe.

**Response (200):**
```json
{
  "id": "uuid-here",
  "name": "Perfect Scrambled Eggs",
  "description": "Creamy, fluffy scrambled eggs",
  "difficulty": "BEGINNER",
  "prep_time_minutes": 5,
  "cook_time_minutes": 10,
  "servings": 2,
  "ingredients": [...],
  "steps": [...],
  "nutritional_info": {
    "calories": 280,
    "protein": "14g",
    "carbs": "2g",
    "fat": "22g"
  }
}
```

---

## Cooking Session Endpoints

### Start Cooking Session

**POST** `/cooking/sessions/start`

Start a new cooking session.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "recipe_id": "uuid-here"
}
```

**Response (201):**
```json
{
  "id": "session-uuid",
  "recipe_id": "uuid-here",
  "user_id": "user-uuid",
  "status": "IN_PROGRESS",
  "current_step": 0,
  "started_at": "2026-02-15T10:30:00Z"
}
```

### Update Session Progress

**POST** `/cooking/sessions/{session_id}/progress`

Update progress for an active session.

**Request Body:**
```json
{
  "current_step": 2,
  "notes": "Looking good so far",
  "timer_used": true
}
```

**Response (200):**
```json
{
  "id": "session-uuid",
  "current_step": 2,
  "updated_at": "2026-02-15T10:35:00Z"
}
```

### Complete Session

**POST** `/cooking/sessions/{session_id}/complete`

Mark session as complete.

**Request Body:**
```json
{
  "success": true,
  "notes": "Turned out delicious!",
  "rating": 5
}
```

**Response (200):**
```json
{
  "id": "session-uuid",
  "status": "COMPLETED",
  "completed_at": "2026-02-15T11:00:00Z",
  "total_duration_minutes": 30
}
```

### Get Session History

**GET** `/cooking/sessions/history`

Get user's past cooking sessions.

**Query Parameters:**
- `limit` (int): Number of sessions (default: 10)
- `offset` (int): Pagination offset (default: 0)

**Response (200):**
```json
{
  "sessions": [
    {
      "id": "uuid",
      "recipe_name": "Scrambled Eggs",
      "started_at": "2026-02-15T10:00:00Z",
      "completed_at": "2026-02-15T10:30:00Z",
      "status": "COMPLETED",
      "success": true
    }
  ],
  "total": 25
}
```

---

## Voice Endpoints

### Speech to Text

**POST** `/voice/stt`

Upload audio file for transcription.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (audio file: .wav, .mp3, .m4a)

**Response (200):**
```json
{
  "text": "next step please"
}
```

### Parse Voice Command

**POST** `/voice/command`

Parse text into voice intent.

**Request Body:**
```json
{
  "text": "set a timer for 5 minutes"
}
```

**Response (200):**
```json
{
  "intent": "TIMER",
  "duration_seconds": 300,
  "confidence": 0.95
}
```

**Supported Intents:**
- `NEXT` - Go to next step
- `PREV` - Go to previous step
- `REPEAT` - Repeat current instruction
- `TIMER` - Set/start timer
- `PAUSE` - Pause session
- `RESUME` - Resume session
- `HELP` - Get help
- `INGREDIENT` - Get ingredient info
- `UNKNOWN` - Unrecognized command

### Text to Speech

**POST** `/voice/tts`

Convert text to speech audio.

**Request Body:**
```json
{
  "text": "Your eggs are ready"
}
```

**Response (200):**
- Content-Type: `audio/mp3`
- Binary audio data

---

## Failure Analysis Endpoints

### Analyze Failed Dish

**POST** `/failure/analyze`

Analyze a failed dish photo with AI.

**Request Body:**
```json
{
  "image_url": "https://example.com/burnt_eggs.jpg",
  "context": {
    "dish_name": "Scrambled Eggs",
    "heat_level": "high",
    "cooking_time": 10,
    "modifications": "Added extra butter"
  }
}
```

**Response (200):**
```json
{
  "root_cause": "Overcooked & Dried Out",
  "severity": "moderate",
  "confidence": 0.88,
  "explanation": "Your eggs were likely cooked at too high temperature...",
  "tips": [
    "Use medium-low heat instead of high",
    "Cook for 3-5 minutes maximum",
    "Remove from heat while slightly wet"
  ],
  "ai_provider": "gemini",
  "analysis_id": "uuid-here"
}
```

### Upload Image for Analysis

**POST** `/failure/upload`

Upload dish image directly.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file: .jpg, .png, .webp)
- Field: `context` (JSON string)

**Response (200):**
```json
{
  "image_url": "https://storage.../uploaded_image.jpg",
  "analysis_id": "uuid-here"
}
```

---

## Profile Endpoints

### Get User Profile

**GET** `/profile`

Get current user's profile.

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "skill_level": "INTERMEDIATE",
  "dietary_preferences": ["vegetarian"],
  "total_sessions": 45,
  "successful_sessions": 42,
  "favorite_recipes": [...]
}
```

### Update Profile

**PUT** `/profile`

Update user profile.

**Request Body:**
```json
{
  "full_name": "John Doe Jr.",
  "skill_level": "ADVANCED",
  "dietary_preferences": ["vegetarian", "gluten-free"]
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "full_name": "John Doe Jr.",
  "skill_level": "ADVANCED",
  "updated_at": "2026-02-15T12:00:00Z"
}
```

---

## Flavor Pairing Endpoints

### Get Ingredient Pairings

**GET** `/flavors/pairings/{ingredient}`

Get flavor pairing suggestions from FlavorDB.

**Example:**
```bash
GET /flavors/pairings/chicken
```

**Response (200):**
```json
{
  "ingredient": "chicken",
  "pairings": [
    {
      "ingredient": "garlic",
      "affinity_score": 0.95
    },
    {
      "ingredient": "lemon",
      "affinity_score": 0.92
    },
    {
      "ingredient": "rosemary",
      "affinity_score": 0.88
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid email format"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Recipe not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Default rate limits:
- **Authentication endpoints**: 5 requests/minute
- **General endpoints**: 100 requests/minute
- **AI endpoints**: 10 requests/minute

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1707998400
```

---

## Webhooks (Future)

Coming soon: Webhook support for real-time notifications.

---

## SDKs & Libraries

### Python
```python
from chefmentorx import ChefMentorClient

client = ChefMentorClient(api_key="your_api_key")
recipes = client.recipes.list(source="local", limit=10)
```

### JavaScript/TypeScript
```typescript
import { ChefMentorAPI } from '@chefmentorx/api';

const api = new ChefMentorAPI({ apiKey: 'your_api_key' });
const recipes = await api.recipes.list({ source: 'local', limit: 10 });
```

---

## Interactive API Documentation

Visit the interactive Swagger UI documentation:

**Development**: http://localhost:8000/docs  
**Production**: https://api.yourdomain.com/docs

---

## Support

For API support:
- **Email**: api-support@chefmentorx.com
- **Slack**: #api-support
- **GitHub**: https://github.com/yourusername/chefmentorx/issues
