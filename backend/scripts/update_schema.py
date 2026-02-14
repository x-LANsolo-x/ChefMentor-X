import asyncio
import os
import sys

# Configure path to import from app
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(backend_dir)

from app.db.base import engine
from sqlalchemy import text

async def update_schema():
    print("🔄 Connecting to database...")
    try:
        async with engine.begin() as conn:
            print("📊 Updating 'failure_analyses' table...")
            
            # Columns to add: name, type
            columns = [
                ("tips", "TEXT"),
                ("severity", "VARCHAR(50)"),
                ("confidence", "FLOAT"),
                ("ai_provider", "VARCHAR(50)")
            ]
            
            for col_name, col_type in columns:
                try:
                    # Generic ALTER TABLE command (works for SQLite and Postgres mostly)
                    sql = text(f"ALTER TABLE failure_analyses ADD COLUMN {col_name} {col_type}")
                    await conn.execute(sql)
                    print(f"   ✅ Added column '{col_name}'")
                except Exception as e:
                    # If column exists, this will likely fail. We ignore it.
                    # Simplified error message for clarity
                    msg = str(e).split('\n')[0]
                    print(f"   ⚠️  Skipped '{col_name}' (exists or error): {msg}")
                    
        print("\n✅ Schema update process completed.")
        
    except Exception as e:
        print(f"\n❌ Database connection failed: {str(e)}")
        print("   Make sure your database server is running.")

if __name__ == "__main__":
    try:
        asyncio.run(update_schema())
    except KeyboardInterrupt:
        print("\n🛑 Update cancelled.")
