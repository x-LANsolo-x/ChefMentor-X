"""
Database seeding script - Populate with initial recipes
Step 3.4: Seed Initial Data
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import AsyncSessionLocal
from app.models import Recipe, RecipeIngredient, RecipeStep, DifficultyLevel
from datetime import datetime

async def clear_existing_data(session: AsyncSession):
    """Clear existing recipe data (for development)"""
    from sqlalchemy import text
    
    print("🗑️  Clearing existing recipe data...")
    
    # Delete in correct order due to foreign keys
    await session.execute(text("DELETE FROM recipe_steps"))
    await session.execute(text("DELETE FROM recipe_ingredients"))
    await session.execute(text("DELETE FROM recipes"))
    await session.commit()
    
    print("✅ Existing data cleared")


async def seed_maggi_noodles(session: AsyncSession):
    """Seed Maggi Noodles recipe"""
    print("\n📝 Creating: Maggi Noodles...")
    
    recipe = Recipe(
        title="Maggi Noodles",
        description="Quick and easy 2-minute noodles - perfect for beginners and a college favorite!",
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=2,
        cook_time_minutes=5,
        total_time_minutes=7,
        servings=1,
        cuisine_type="Indian",
        meal_type="snack",
        tags=["quick", "easy", "vegetarian", "student-friendly"],
        is_active=True,
        is_featured=True,
    )
    session.add(recipe)
    await session.flush()  # Get recipe.id
    
    # Ingredients
    ingredients = [
        RecipeIngredient(recipe_id=recipe.id, name="Maggi noodles", quantity=1, unit="packet", order=1),
        RecipeIngredient(recipe_id=recipe.id, name="Water", quantity=1.5, unit="cups", order=2),
        RecipeIngredient(recipe_id=recipe.id, name="Maggi masala", quantity=1, unit="packet", order=3, notes="included in packet"),
        RecipeIngredient(recipe_id=recipe.id, name="Vegetables", quantity=0.5, unit="cup", order=4, notes="chopped, optional"),
    ]
    session.add_all(ingredients)
    
    # Steps
    steps = [
        RecipeStep(
            recipe_id=recipe.id,
            step_number=1,
            instruction="Boil 1.5 cups of water in a pan on high heat",
            duration_minutes=2,
            timer_required=True
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=2,
            instruction="Add the noodles and optional vegetables. Break the noodle cake into smaller pieces if desired",
            duration_minutes=1
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=3,
            instruction="Cook for 2 minutes, stirring occasionally",
            duration_minutes=2,
            timer_required=True,
            ai_tips="Stir gently to prevent noodles from sticking to the pan"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=4,
            instruction="Add the Maggi masala and mix well",
            duration_minutes=1
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=5,
            instruction="Serve hot and enjoy!",
            duration_minutes=0
        ),
    ]
    session.add_all(steps)
    
    print("✅ Maggi Noodles created")


async def seed_scrambled_eggs(session: AsyncSession):
    """Seed Scrambled Eggs recipe"""
    print("\n📝 Creating: Scrambled Eggs...")
    
    recipe = Recipe(
        title="Scrambled Eggs",
        description="Fluffy, creamy scrambled eggs - a breakfast classic that's simple to master",
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=3,
        cook_time_minutes=5,
        total_time_minutes=8,
        servings=2,
        cuisine_type="International",
        meal_type="breakfast",
        tags=["quick", "protein", "breakfast", "gluten-free"],
        calories=200,
        protein_grams=12,
        is_active=True,
        is_featured=True,
    )
    session.add(recipe)
    await session.flush()
    
    # Ingredients
    ingredients = [
        RecipeIngredient(recipe_id=recipe.id, name="Eggs", quantity=3, unit="pieces", order=1),
        RecipeIngredient(recipe_id=recipe.id, name="Milk", quantity=2, unit="tablespoons", order=2),
        RecipeIngredient(recipe_id=recipe.id, name="Butter", quantity=1, unit="tablespoon", order=3),
        RecipeIngredient(recipe_id=recipe.id, name="Salt", quantity=0.25, unit="teaspoon", order=4, notes="to taste"),
        RecipeIngredient(recipe_id=recipe.id, name="Black pepper", quantity=0.125, unit="teaspoon", order=5, notes="to taste, optional"),
    ]
    session.add_all(ingredients)
    
    # Steps
    steps = [
        RecipeStep(
            recipe_id=recipe.id,
            step_number=1,
            instruction="Crack eggs into a bowl, add milk, salt, and pepper. Whisk until well combined",
            duration_minutes=2,
            ai_tips="Whisk vigorously for 30 seconds to incorporate air for fluffier eggs"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=2,
            instruction="Heat butter in a non-stick pan over medium-low heat until melted and foamy",
            duration_minutes=1,
            common_mistakes=["Using high heat (eggs will become rubbery)", "Not waiting for butter to melt completely"]
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=3,
            instruction="Pour in the egg mixture and let it sit for 20 seconds without stirring",
            duration_minutes=1,
            timer_required=True
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=4,
            instruction="Gently push the eggs from the edges to the center with a spatula. Repeat this process slowly",
            duration_minutes=2,
            ai_tips="Slow and gentle movements create soft, creamy curds. Avoid over-stirring"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=5,
            instruction="Remove from heat when eggs are still slightly wet (they will continue cooking). Serve immediately",
            duration_minutes=0,
            ai_tips="Eggs should be creamy, not dry. Remove them just before they look fully cooked"
        ),
    ]
    session.add_all(steps)
    
    print("✅ Scrambled Eggs created")


async def seed_simple_dal(session: AsyncSession):
    """Seed Simple Dal recipe"""
    print("\n📝 Creating: Simple Dal...")
    
    recipe = Recipe(
        title="Simple Dal (Lentil Curry)",
        description="Comforting Indian lentil soup - nutritious, flavorful, and easy to make",
        difficulty=DifficultyLevel.INTERMEDIATE,
        prep_time_minutes=10,
        cook_time_minutes=25,
        total_time_minutes=35,
        servings=4,
        cuisine_type="Indian",
        meal_type="dinner",
        tags=["vegetarian", "vegan", "healthy", "protein-rich", "gluten-free"],
        calories=180,
        protein_grams=9,
        is_active=True,
        is_featured=True,
    )
    session.add(recipe)
    await session.flush()
    
    # Ingredients
    ingredients = [
        RecipeIngredient(recipe_id=recipe.id, name="Yellow lentils (toor dal)", quantity=1, unit="cup", order=1),
        RecipeIngredient(recipe_id=recipe.id, name="Water", quantity=3, unit="cups", order=2),
        RecipeIngredient(recipe_id=recipe.id, name="Turmeric powder", quantity=0.5, unit="teaspoon", order=3),
        RecipeIngredient(recipe_id=recipe.id, name="Salt", quantity=1, unit="teaspoon", order=4, notes="to taste"),
        RecipeIngredient(recipe_id=recipe.id, name="Oil or ghee", quantity=2, unit="tablespoons", order=5),
        RecipeIngredient(recipe_id=recipe.id, name="Cumin seeds", quantity=1, unit="teaspoon", order=6),
        RecipeIngredient(recipe_id=recipe.id, name="Garlic", quantity=3, unit="cloves", order=7, notes="minced"),
        RecipeIngredient(recipe_id=recipe.id, name="Onion", quantity=1, unit="medium", order=8, notes="chopped"),
        RecipeIngredient(recipe_id=recipe.id, name="Tomato", quantity=1, unit="medium", order=9, notes="chopped"),
        RecipeIngredient(recipe_id=recipe.id, name="Green chili", quantity=1, unit="piece", order=10, notes="slit, optional"),
        RecipeIngredient(recipe_id=recipe.id, name="Cilantro", quantity=2, unit="tablespoons", order=11, notes="chopped, for garnish"),
    ]
    session.add_all(ingredients)
    
    # Steps
    steps = [
        RecipeStep(
            recipe_id=recipe.id,
            step_number=1,
            instruction="Rinse lentils thoroughly in water 2-3 times until water runs clear",
            duration_minutes=2
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=2,
            instruction="In a pot, add lentils, 3 cups water, turmeric, and salt. Bring to a boil",
            duration_minutes=5
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=3,
            instruction="Reduce heat to low, cover partially, and simmer for 20 minutes until lentils are soft and mushy",
            duration_minutes=20,
            timer_required=True,
            ai_tips="Stir occasionally to prevent sticking. Add more water if it gets too thick"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=4,
            instruction="While dal cooks, heat oil in a small pan. Add cumin seeds and let them sizzle for 30 seconds",
            duration_minutes=1
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=5,
            instruction="Add garlic, onion, and green chili. Sauté until onions turn golden brown",
            duration_minutes=5,
            ai_tips="Cook on medium heat for even browning"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=6,
            instruction="Add tomatoes and cook until soft and mushy",
            duration_minutes=3
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=7,
            instruction="Pour this tempering (tadka) over the cooked dal. Mix well",
            duration_minutes=1
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=8,
            instruction="Garnish with cilantro and serve hot with rice or roti",
            duration_minutes=0
        ),
    ]
    session.add_all(steps)
    
    print("✅ Simple Dal created")


async def seed_grilled_cheese(session: AsyncSession):
    """Seed Grilled Cheese recipe"""
    print("\n📝 Creating: Grilled Cheese Sandwich...")
    
    recipe = Recipe(
        title="Perfect Grilled Cheese Sandwich",
        description="Crispy, golden bread with melted cheese - a comfort food classic",
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=5,
        cook_time_minutes=6,
        total_time_minutes=11,
        servings=1,
        cuisine_type="American",
        meal_type="lunch",
        tags=["quick", "comfort-food", "vegetarian", "kid-friendly"],
        calories=400,
        is_active=True,
        is_featured=True,
    )
    session.add(recipe)
    await session.flush()
    
    # Ingredients
    ingredients = [
        RecipeIngredient(recipe_id=recipe.id, name="Bread slices", quantity=2, unit="pieces", order=1, notes="white or whole wheat"),
        RecipeIngredient(recipe_id=recipe.id, name="Cheese slices", quantity=2, unit="pieces", order=2, notes="cheddar or American"),
        RecipeIngredient(recipe_id=recipe.id, name="Butter", quantity=1, unit="tablespoon", order=3, notes="softened"),
    ]
    session.add_all(ingredients)
    
    # Steps
    steps = [
        RecipeStep(
            recipe_id=recipe.id,
            step_number=1,
            instruction="Butter one side of each bread slice generously",
            duration_minutes=1,
            ai_tips="Spread butter all the way to the edges for even browning"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=2,
            instruction="Place cheese slices on the unbuttered side of one bread slice. Top with the second slice, buttered side up",
            duration_minutes=1
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=3,
            instruction="Heat a non-stick pan over medium-low heat",
            duration_minutes=1,
            common_mistakes=["Using high heat (bread burns before cheese melts)"]
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=4,
            instruction="Place sandwich in the pan. Cook for 3 minutes until bottom is golden brown",
            duration_minutes=3,
            timer_required=True,
            ai_tips="Don't press down too hard - you want a crispy exterior but fluffy interior"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=5,
            instruction="Carefully flip the sandwich and cook for another 3 minutes until second side is golden and cheese is fully melted",
            duration_minutes=3,
            timer_required=True
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=6,
            instruction="Remove from pan, let cool for 1 minute, cut diagonally, and serve",
            duration_minutes=1
        ),
    ]
    session.add_all(steps)
    
    print("✅ Grilled Cheese Sandwich created")


async def seed_simple_pasta(session: AsyncSession):
    """Seed Simple Pasta recipe"""
    print("\n📝 Creating: Simple Pasta...")
    
    recipe = Recipe(
        title="Simple Pasta with Tomato Sauce",
        description="Classic pasta with homemade tomato sauce - simple ingredients, delicious results",
        difficulty=DifficultyLevel.BEGINNER,
        prep_time_minutes=10,
        cook_time_minutes=20,
        total_time_minutes=30,
        servings=2,
        cuisine_type="Italian",
        meal_type="dinner",
        tags=["vegetarian", "pasta", "italian", "easy"],
        calories=450,
        carbs_grams=75,
        is_active=True,
        is_featured=True,
    )
    session.add(recipe)
    await session.flush()
    
    # Ingredients
    ingredients = [
        RecipeIngredient(recipe_id=recipe.id, name="Pasta", quantity=200, unit="grams", order=1, notes="any shape"),
        RecipeIngredient(recipe_id=recipe.id, name="Salt", quantity=1, unit="tablespoon", order=2, notes="for pasta water"),
        RecipeIngredient(recipe_id=recipe.id, name="Olive oil", quantity=2, unit="tablespoons", order=3),
        RecipeIngredient(recipe_id=recipe.id, name="Garlic", quantity=4, unit="cloves", order=4, notes="minced"),
        RecipeIngredient(recipe_id=recipe.id, name="Canned tomatoes", quantity=400, unit="grams", order=5, notes="crushed or diced"),
        RecipeIngredient(recipe_id=recipe.id, name="Dried basil", quantity=1, unit="teaspoon", order=6, notes="or 5-6 fresh leaves"),
        RecipeIngredient(recipe_id=recipe.id, name="Sugar", quantity=0.5, unit="teaspoon", order=7, notes="optional, to balance acidity"),
        RecipeIngredient(recipe_id=recipe.id, name="Salt and pepper", quantity=1, unit="to taste", order=8),
        RecipeIngredient(recipe_id=recipe.id, name="Parmesan cheese", quantity=2, unit="tablespoons", order=9, notes="grated, for serving"),
    ]
    session.add_all(ingredients)
    
    # Steps
    steps = [
        RecipeStep(
            recipe_id=recipe.id,
            step_number=1,
            instruction="Bring a large pot of salted water to a boil",
            duration_minutes=5,
            ai_tips="Use plenty of water - at least 4 cups per 100g of pasta. Salt the water generously"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=2,
            instruction="Add pasta and cook according to package directions (usually 8-10 minutes) until al dente",
            duration_minutes=10,
            timer_required=True,
            ai_tips="Stir occasionally to prevent sticking. Taste 1-2 minutes before suggested time"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=3,
            instruction="While pasta cooks, heat olive oil in a large pan over medium heat. Add minced garlic",
            duration_minutes=2
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=4,
            instruction="Sauté garlic for 1 minute until fragrant (don't let it burn)",
            duration_minutes=1,
            common_mistakes=["Burning garlic (it becomes bitter)", "Using too high heat"]
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=5,
            instruction="Add canned tomatoes, basil, sugar, salt, and pepper. Bring to a simmer",
            duration_minutes=2
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=6,
            instruction="Simmer sauce for 10 minutes, stirring occasionally, until slightly thickened",
            duration_minutes=10,
            timer_required=True,
            ai_tips="Break up large tomato chunks with your spoon as it cooks"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=7,
            instruction="Reserve 1 cup of pasta water, then drain the pasta",
            duration_minutes=1,
            ai_tips="Pasta water helps adjust sauce consistency and helps sauce stick to pasta"
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=8,
            instruction="Add drained pasta to the sauce. Toss to coat. Add pasta water if needed to loosen the sauce",
            duration_minutes=2
        ),
        RecipeStep(
            recipe_id=recipe.id,
            step_number=9,
            instruction="Serve hot, topped with grated Parmesan cheese",
            duration_minutes=0
        ),
    ]
    session.add_all(steps)
    
    print("✅ Simple Pasta created")


async def verify_seeded_data(session: AsyncSession):
    """Verify that data was seeded correctly"""
    print("\n" + "=" * 70)
    print("🔍 Verifying Seeded Data...")
    print("=" * 70)
    
    from sqlalchemy import select, func
    
    # Count recipes
    result = await session.execute(select(func.count()).select_from(Recipe))
    recipe_count = result.scalar()
    print(f"\n📊 Total Recipes: {recipe_count}")
    
    # Count ingredients
    result = await session.execute(select(func.count()).select_from(RecipeIngredient))
    ingredient_count = result.scalar()
    print(f"📊 Total Ingredients: {ingredient_count}")
    
    # Count steps
    result = await session.execute(select(func.count()).select_from(RecipeStep))
    step_count = result.scalar()
    print(f"📊 Total Steps: {step_count}")
    
    # List all recipes with details
    print("\n📋 Seeded Recipes:")
    result = await session.execute(
        select(Recipe).order_by(Recipe.id)
    )
    recipes = result.scalars().all()
    
    for recipe in recipes:
        print(f"\n  ✅ {recipe.title}")
        print(f"     Difficulty: {recipe.difficulty.value}")
        print(f"     Time: {recipe.total_time_minutes} minutes")
        print(f"     Servings: {recipe.servings}")
        
        # Count ingredients and steps for this recipe
        result = await session.execute(
            select(func.count()).select_from(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe.id)
        )
        ing_count = result.scalar()
        
        result = await session.execute(
            select(func.count()).select_from(RecipeStep).where(RecipeStep.recipe_id == recipe.id)
        )
        step_count = result.scalar()
        
        print(f"     Ingredients: {ing_count}, Steps: {step_count}")


async def main():
    """Main seeding function"""
    print("=" * 70)
    print("🌱 ChefMentor X - Database Seeding")
    print("=" * 70)
    print("\nThis will populate the database with 5 starter recipes:")
    print("  1. Maggi Noodles")
    print("  2. Scrambled Eggs")
    print("  3. Simple Dal")
    print("  4. Grilled Cheese Sandwich")
    print("  5. Simple Pasta with Tomato Sauce")
    print("=" * 70)
    
    try:
        async with AsyncSessionLocal() as session:
            # Clear existing data (optional - comment out if you want to keep existing data)
            await clear_existing_data(session)
            
            # Seed all recipes
            await seed_maggi_noodles(session)
            await seed_scrambled_eggs(session)
            await seed_simple_dal(session)
            await seed_grilled_cheese(session)
            await seed_simple_pasta(session)
            
            # Commit all changes
            await session.commit()
            
            # Verify
            await verify_seeded_data(session)
        
        print("\n" + "=" * 70)
        print("🎉 DATABASE SEEDING COMPLETE!")
        print("=" * 70)
        print("\n✅ 5 recipes added successfully")
        print("✅ All ingredients and steps created")
        print("✅ Database is ready for use!")
        print("\n" + "=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Seeding failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
