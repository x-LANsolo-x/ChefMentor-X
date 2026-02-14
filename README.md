# BugOff

BugOff is a voice-first, AI-assisted cooking companion that helps home cooks follow recipes, ask questions hands-free, and learn from mistakes. It combines step-by-step guidance with real-time assistance so users can cook confidently without constantly touching their phones.

## Features

- Voice-first cooking flow with hands-free controls
- Context-aware coaching during each step
- Photo-based failure analysis to diagnose what went wrong
- Clear, accessible UI designed for use while cooking
- Demo mode for trying the app without an account

## Tech Stack

**Backend**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic

**Frontend**
- React Native
- Expo
- TypeScript
- Zustand
- React Navigation

**AI/ML Services**
- Google Gemini
- Groq Whisper
- Google Text-to-Speech

**Infrastructure**
- Cloudinary
- Railway (recommended)
- Upstash (recommended)

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Clone the Repository

```bash
git clone https://github.com/x-LANsolo-x/BugOff.git
cd BugOff
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd ../frontend
npm install
```

### Environment Configuration

```bash
cp backend/.env.example backend/.env
```

Update `backend/.env` with the required keys and values:

- Database URL
- Redis URL
- Cloudinary credentials
- Google Gemini API key
- Groq Whisper API key
- Google TTS credentials

### Database Setup

1. Ensure PostgreSQL is running.
2. Create a database (for example, `bugoff`).
3. Update the `DATABASE_URL` in `backend/.env`.
4. Apply migrations:

```bash
cd backend
alembic upgrade head
```

### Run the Application

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

```bash
# Terminal 2 - Frontend
cd frontend
npm start
```

### Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Project Structure

```
BugOff/
├── backend/                 # Python FastAPI backend
│   ├── app/                 # Application code
│   ├── tests/               # Backend tests
│   ├── alembic/             # Database migrations
│   ├── .env                 # Environment variables (not in git)
│   ├── .env.example         # Environment template
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React Native mobile app
│   ├── src/                 # Source code
│   │   ├── screens/         # Screen components
│   │   ├── components/      # Reusable components
│   │   ├── services/        # API and service layer
│   │   ├── hooks/           # Custom React hooks
│   │   ├── store/           # Zustand state management
│   │   └── utils/           # Utilities and helpers
│   ├── assets/              # Images, fonts
│   ├── App.tsx              # Root component
│   └── package.json         # Node dependencies
│
├── docs/                    # Planning and implementation docs
├── md/                      # Detailed technical specifications
├── stitch/                  # UI design prototypes (HTML/CSS)
├── SETUP.md                 # Setup instructions
└── README.md                # This file
```

## Documentation

Additional documentation is available in the `docs` and `md` directories:

- `SETUP.md` - Complete installation guide
- `docs/IMPLEMENTATION_PLAN.md` - Development roadmap
- `docs/PROJECT_TIMELINE_GANTT.md` - Timeline and milestones
- `md/chef_mentor_x_backend_structure_backend_structure.md` - Backend structure
- `md/chef_mentor_x_frontend_design_system_frontend_guidelines.md` - Frontend design system
- `md/chef_mentor_x_technology_stack_tech_stack.md` - Technology stack details
- `md/chef_mentor_x_testing_strategy.md` - Testing strategy
- `md/chef_mentor_x_ai_ml_strategy.md` - AI/ML strategy
- `md/chef_mentor_x_voice_interaction_spec.md` - Voice interaction specification
- `md/chef_mentor_x_recipe_integration_guide.md` - Recipe integration guide
- `md/chef_mentor_x_privacy_security_policy.md` - Privacy and security policy
- `md/chef_mentor_x_final_prd_v_2_two_tab_experience.md` - Product requirements
- `md/chef_mentor_x_application_flow_app_flow.md` - Application flow

## Troubleshooting

**Dependencies fail to install**

```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# Frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Database connection issues**

- Confirm PostgreSQL is running.
- Verify the `DATABASE_URL` in `backend/.env`.
- Check that port 5432 is available.

**Expo fails to start**

```bash
cd frontend
npx expo start -c
```

For more details, see `SETUP.md`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## Contact & Support

- Issues: https://github.com/x-LANsolo-x/BugOff/issues
- Email: shashwatvatsyayan@gmail.com
- GitHub: https://github.com/x-LANsolo-x

## Contributors

<a href="https://github.com/x-LANsolo-x" title="x-LANsolo-x">
  <img src="https://avatars.githubusercontent.com/x-LANsolo-x" alt="x-LANsolo-x" width="80" height="80" />
</a>

Made by Team BugOff
