"""
ChefMentor X - Production Configuration

Additional production-specific settings and security measures.
"""
from pydantic_settings import BaseSettings
from typing import List


class ProductionSettings(BaseSettings):
    """Production-specific settings"""
    
    # Security
    SECURE_COOKIES: bool = True
    HTTPS_ONLY: bool = True
    CORS_CREDENTIALS: bool = True
    
    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = True
    GLOBAL_RATE_LIMIT: str = "100/minute"
    AUTH_RATE_LIMIT: str = "5/minute"
    
    # Monitoring
    SENTRY_DSN: str | None = None
    ENABLE_METRICS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Database
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    DB_POOL_TIMEOUT: int = 30
    
    # Caching
    ENABLE_CACHE: bool = True
    CACHE_BACKEND: str = "redis"  # redis or memory
    
    # File Storage
    STORAGE_BACKEND: str = "s3"  # s3 or local
    S3_BUCKET: str | None = None
    S3_REGION: str = "us-east-1"
    
    # AI Services
    AI_TIMEOUT_SECONDS: int = 30
    AI_MAX_RETRIES: int = 3
    
    # Performance
    ENABLE_COMPRESSION: bool = True
    ENABLE_CACHING: bool = True
    
    class Config:
        env_file = ".env.production"


# Production middleware and security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}


# CORS configuration for production
def get_cors_config(allowed_origins: List[str]) -> dict:
    """Get CORS configuration for production"""
    return {
        "allow_origins": allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["*"],
        "max_age": 3600,
    }
