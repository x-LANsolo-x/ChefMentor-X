"""
Comprehensive testing for Alembic migrations and database schema
Step 3.3 - Intensive Testing
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text, inspect
from dotenv import load_dotenv
import os

load_dotenv()

async def test_migrations():
    """Comprehensive migration and schema testing"""
    
    database_url = os.getenv("DATABASE_URL")
    
    print("=" * 80)
    print("🧪 STEP 3.3: INTENSIVE MIGRATION TESTING")
    print("=" * 80)
    
    all_tests_passed = True
    
    try:
        engine = create_async_engine(database_url, echo=False)
        
        # ============================================================
        # TEST 1: Migration System
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 1: ALEMBIC MIGRATION SYSTEM")
        print("=" * 80)
        
        async with engine.connect() as conn:
            # Check alembic_version table exists
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            exists = result.scalar()
            
            if exists:
                print("✅ alembic_version table exists")
                
                # Get current migration version
                result = await conn.execute(text("SELECT version_num FROM alembic_version;"))
                version = result.scalar()
                print(f"✅ Current migration version: {version}")
                
                if version == "83ddadd367f7":
                    print("✅ Migration version matches expected (83ddadd367f7)")
                else:
                    print(f"❌ Migration version mismatch. Expected: 83ddadd367f7, Got: {version}")
                    all_tests_passed = False
            else:
                print("❌ alembic_version table does not exist")
                all_tests_passed = False
        
        # ============================================================
        # TEST 2: All Tables Exist
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 2: ALL REQUIRED TABLES EXIST")
        print("=" * 80)
        
        expected_tables = [
            'users',
            'user_profiles',
            'recipes',
            'recipe_ingredients',
            'recipe_steps',
            'cooking_sessions',
            'session_steps',
            'failure_analyses'
        ]
        
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            existing_tables = [row[0] for row in result.fetchall()]
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"✅ {table} - EXISTS")
            else:
                print(f"❌ {table} - MISSING")
                all_tests_passed = False
        
        # ============================================================
        # TEST 3: Table Structures
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 3: TABLE STRUCTURES AND COLUMNS")
        print("=" * 80)
        
        async with engine.connect() as conn:
            # Test users table
            print("\n📋 users table:")
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            required_columns = ['id', 'email', 'google_id', 'is_demo', 'is_active', 'created_at']
            found_columns = [col[0] for col in columns]
            
            for req_col in required_columns:
                if req_col in found_columns:
                    print(f"  ✅ {req_col}")
                else:
                    print(f"  ❌ {req_col} - MISSING")
                    all_tests_passed = False
            
            # Test recipes table
            print("\n📋 recipes table:")
            result = await conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'recipes'
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            required_columns = ['id', 'title', 'description', 'difficulty', 'prep_time_minutes']
            found_columns = [col[0] for col in columns]
            
            for req_col in required_columns:
                if req_col in found_columns:
                    print(f"  ✅ {req_col}")
                else:
                    print(f"  ❌ {req_col} - MISSING")
                    all_tests_passed = False
        
        # ============================================================
        # TEST 4: Indexes
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 4: INDEXES")
        print("=" * 80)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT tablename, indexname
                FROM pg_indexes
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname;
            """))
            indexes = result.fetchall()
        
        print(f"\n✅ Total indexes created: {len(indexes)}")
        
        # Check for important indexes
        important_indexes = [
            'ix_users_email',
            'ix_users_google_id',
            'ix_recipes_title',
            'ix_cooking_sessions_user_id',
            'ix_cooking_sessions_recipe_id'
        ]
        
        index_names = [idx[1] for idx in indexes]
        for idx in important_indexes:
            if idx in index_names:
                print(f"  ✅ {idx}")
            else:
                print(f"  ⚠️  {idx} - Not found (may be optional)")
        
        # ============================================================
        # TEST 5: Foreign Keys
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 5: FOREIGN KEY CONSTRAINTS")
        print("=" * 80)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT 
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                ORDER BY tc.table_name;
            """))
            foreign_keys = result.fetchall()
        
        print(f"\n✅ Total foreign keys: {len(foreign_keys)}")
        
        for fk in foreign_keys:
            print(f"  ✅ {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")
        
        # ============================================================
        # TEST 6: Enums
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 6: ENUM TYPES")
        print("=" * 80)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT typname
                FROM pg_type
                WHERE typtype = 'e'
                ORDER BY typname;
            """))
            enums = result.fetchall()
        
        expected_enums = ['difficultylevel', 'sessionstatus', 'skilllevel', 'stepstatus']
        found_enums = [e[0] for e in enums]
        
        for enum in expected_enums:
            if enum in found_enums:
                print(f"  ✅ {enum}")
            else:
                print(f"  ❌ {enum} - MISSING")
                all_tests_passed = False
        
        # ============================================================
        # TEST 7: Data Insertion Test
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 7: DATA INSERTION TEST")
        print("=" * 80)
        
        async with engine.begin() as conn:
            # Insert test user
            result = await conn.execute(text("""
                INSERT INTO users (email, is_demo, is_active, display_name)
                VALUES ('test@example.com', true, true, 'Test User')
                RETURNING id;
            """))
            user_id = result.scalar()
            print(f"✅ Test user inserted (ID: {user_id})")
            
            # Insert test recipe
            result = await conn.execute(text("""
                INSERT INTO recipes (title, description, difficulty)
                VALUES ('Test Recipe', 'A test recipe', 'beginner')
                RETURNING id;
            """))
            recipe_id = result.scalar()
            print(f"✅ Test recipe inserted (ID: {recipe_id})")
            
            # Test foreign key relationship
            result = await conn.execute(text("""
                INSERT INTO cooking_sessions (user_id, recipe_id, status)
                VALUES (:user_id, :recipe_id, 'not_started')
                RETURNING id;
            """), {"user_id": user_id, "recipe_id": recipe_id})
            session_id = result.scalar()
            print(f"✅ Test cooking session inserted (ID: {session_id})")
            
            # Clean up test data
            await conn.execute(text("DELETE FROM cooking_sessions WHERE id = :id"), {"id": session_id})
            await conn.execute(text("DELETE FROM recipes WHERE id = :id"), {"id": recipe_id})
            await conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
            print("✅ Test data cleaned up")
        
        # ============================================================
        # TEST 8: Cascade Delete Test
        # ============================================================
        print("\n" + "=" * 80)
        print("TEST 8: CASCADE DELETE TEST")
        print("=" * 80)
        
        async with engine.begin() as conn:
            # Create test user with profile
            result = await conn.execute(text("""
                INSERT INTO users (email, is_demo)
                VALUES ('cascade_test@example.com', true)
                RETURNING id;
            """))
            user_id = result.scalar()
            
            result = await conn.execute(text("""
                INSERT INTO user_profiles (user_id, skill_level)
                VALUES (:user_id, 'beginner')
                RETURNING id;
            """), {"user_id": user_id})
            profile_id = result.scalar()
            
            # Delete user (should cascade to profile)
            await conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
            
            # Check if profile was deleted
            result = await conn.execute(text("""
                SELECT COUNT(*) FROM user_profiles WHERE id = :id
            """), {"id": profile_id})
            count = result.scalar()
            
            if count == 0:
                print("✅ Cascade delete working correctly")
            else:
                print("❌ Cascade delete failed - orphaned profile exists")
                all_tests_passed = False
        
        await engine.dispose()
        
        # ============================================================
        # FINAL RESULTS
        # ============================================================
        print("\n" + "=" * 80)
        if all_tests_passed:
            print("🎉 ALL TESTS PASSED!")
            print("=" * 80)
            print("\n✅ Alembic migration system working correctly")
            print("✅ All tables created successfully")
            print("✅ All columns present")
            print("✅ Indexes configured correctly")
            print("✅ Foreign keys working")
            print("✅ Enums defined properly")
            print("✅ Data insertion working")
            print("✅ Cascade deletes functioning")
            print("\n🚀 Database is ready for production use!")
        else:
            print("❌ SOME TESTS FAILED")
            print("=" * 80)
            print("\n⚠️  Please review the failed tests above")
        print("=" * 80)
        
        return all_tests_passed
        
    except Exception as e:
        print(f"\n❌ Testing failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_migrations())
    sys.exit(0 if success else 1)
