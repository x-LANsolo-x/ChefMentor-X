"""
ChefMentor X - FastAPI Application
Main application entry point with health check endpoints
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="ChefMentor X API",
    version="1.0.0",
    description="AI-Powered Voice-First Cooking Assistant - Backend API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to ChefMentor X API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify backend is running
    
    Returns service status and basic configuration info
    """
    from app.db.base import DATABASE_URL
    
    return {
        "status": "healthy",
        "service": "ChefMentor X API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": {
            "status": "configured",
            "type": "PostgreSQL (Railway)",
            "driver": "asyncpg"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 ChefMentor X API Starting...")
    print("📚 Documentation available at /docs")
    print("❤️  Health check at /health")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    from app.db.base import close_db
    await close_db()
    print("👋 ChefMentor X API Shutting down...")


# Future: Include routers here
# from app.api.v1 import api_router
# app.include_router(api_router, prefix="/api/v1")
