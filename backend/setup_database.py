#!/usr/bin/env python3
"""
Database setup script for ChefMentor X
Handles database creation, migration, and initial seeding
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def print_step(step, message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print('='*60)

def get_db_params(database_url):
    """Parse database URL and extract connection parameters"""
    # Remove asyncpg driver if present
    database_url = database_url.replace('+asyncpg', '')
    parsed = urlparse(database_url)
    
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'user': parsed.username or 'postgres',
        'password': parsed.password or '',
        'database': parsed.path.lstrip('/') if parsed.path else 'chefmentor_dev'
    }

def test_postgres_connection(params):
    """Test if we can connect to PostgreSQL server"""
    print_step(1, "Testing PostgreSQL Connection")
    
    try:
        # Try connecting to default 'postgres' database
        conn = psycopg2.connect(
            host=params['host'],
            port=params['port'],
            user=params['user'],
            password=params['password'],
            database='postgres'
        )
        conn.close()
        print("✅ Successfully connected to PostgreSQL server")
        return True
    except psycopg2.OperationalError as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        print("\nPlease check:")
        print("  1. PostgreSQL is running")
        print("  2. Username and password are correct")
        print("  3. Host and port are accessible")
        return False

def create_database_if_not_exists(params):
    """Create the database if it doesn't exist"""
    print_step(2, f"Creating Database: {params['database']}")
    
    try:
        # Connect to postgres database to create our database
        conn = psycopg2.connect(
            host=params['host'],
            port=params['port'],
            user=params['user'],
            password=params['password'],
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (params['database'],)
        )
        
        if cursor.fetchone():
            print(f"✅ Database '{params['database']}' already exists")
        else:
            cursor.execute(f'CREATE DATABASE {params["database"]}')
            print(f"✅ Created database '{params['database']}'")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def run_migrations():
    """Run Alembic migrations"""
    print_step(3, "Running Database Migrations")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Migration failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False

def seed_database():
    """Seed the database with initial data"""
    print_step(4, "Seeding Database with Initial Data")
    
    seed_file = Path(__file__).parent / "seed_recipes.py"
    if not seed_file.exists():
        print("⚠️  Seed file not found, skipping...")
        return True
    
    try:
        result = subprocess.run(
            [sys.executable, str(seed_file)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Database seeded successfully")
            print(result.stdout)
            return True
        else:
            print("⚠️  Seeding encountered issues (may be normal if already seeded):")
            print(result.stderr)
            return True  # Don't fail setup if seeding fails
            
    except Exception as e:
        print(f"⚠️  Failed to seed database: {e}")
        return True  # Don't fail setup if seeding fails

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🍳 ChefMentor X - Database Setup")
    print("="*60)
    
    # Check for DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("\n❌ ERROR: DATABASE_URL not found in environment variables")
        print("\nPlease:")
        print("  1. Copy backend/.env.example to backend/.env")
        print("  2. Update DATABASE_URL with your PostgreSQL credentials")
        print("  3. Run this script again")
        sys.exit(1)
    
    # Parse database parameters
    params = get_db_params(database_url)
    print(f"\nDatabase Configuration:")
    print(f"  Host: {params['host']}")
    print(f"  Port: {params['port']}")
    print(f"  User: {params['user']}")
    print(f"  Database: {params['database']}")
    
    # Run setup steps
    if not test_postgres_connection(params):
        print("\n" + "="*60)
        print("❌ Setup failed: Cannot connect to PostgreSQL")
        print("="*60)
        sys.exit(1)
    
    if not create_database_if_not_exists(params):
        print("\n" + "="*60)
        print("❌ Setup failed: Cannot create database")
        print("="*60)
        sys.exit(1)
    
    if not run_migrations():
        print("\n" + "="*60)
        print("❌ Setup failed: Migrations failed")
        print("="*60)
        sys.exit(1)
    
    seed_database()  # Optional, don't fail if this doesn't work
    
    # Success!
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print("\nYour database is ready to use.")
    print("You can now start the backend server with:")
    print("  uvicorn app.main:app --reload")
    print("\n")

if __name__ == "__main__":
    main()
