"""
Simple recipe seeder - uses direct SQL to avoid model import issues
"""
import asyncio
import asyncpg
import json

DATABASE_URL = "postgresql://postgres:PUwHtSNmtylcCIxoWGBzUgohrAEeyAsD@yamanote.proxy.rlwy.net:18960/railway"

recipes = [
    {
        "title": "Perfect Scrambled Eggs",
        "description": "Creamy French-style scrambled eggs",
        "difficulty": "BEGINNER",
        "prep_time": 2, "cook_time": 5, "total_time": 7, "servings": 2,
        "image_url": "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=400",
        "tags": ["breakfast", "quick"],
        "steps": [
            "Crack eggs into bowl. Add cream, salt, pepper. Whisk until combined.",
            "Heat butter in non-stick pan over medium-low until foaming.",
            "Pour eggs. Wait 20 seconds, then gently push from edges to center.",
            "Remove from heat when still slightly wet. Residual heat finishes cooking.",
            "Plate immediately. Garnish with chives and black pepper."
        ]
    },
    {
        "title": "Classic Pasta Carbonara",
        "description": "Authentic Roman carbonara with guanciale and pecorino",
        "difficulty": "INTERMEDIATE",
        "prep_time": 10, "cook_time": 15, "total_time": 25, "servings": 4,
        "image_url": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400",
        "tags": ["pasta", "italian", "dinner"],
        "steps": [
            "Boil salted water. Cook spaghetti until al dente (10 min).",
            "Cut guanciale into strips. Cook in pan over medium until crispy.",
            "Whisk egg yolks, whole egg, pecorino, and black pepper in bowl.",
            "Reserve 1 cup pasta water. Drain pasta, add to pan off heat.",
            "Quickly toss pasta with egg mixture. Add pasta water for creamy sauce.",
            "Serve immediately with extra pecorino and pepper."
        ]
    },
    {
        "title": "Easy Chicken Stir Fry",
        "description": "Quick stir fry with tender chicken and crisp vegetables",
        "difficulty": "BEGINNER",
        "prep_time": 15, "cook_time": 10, "total_time": 25, "servings": 4,
        "image_url": "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=400",
        "tags": ["dinner", "asian", "quick"],
        "steps": [
            "Slice chicken thin. Toss with soy sauce and cornstarch.",
            "Heat wok until smoking. Add oil.",
            "Add chicken in single layer. Sear 1 min, then stir fry until cooked.",
            "Remove chicken. Add oil, garlic, ginger. Stir fry 30 seconds.",
            "Add vegetables. Stir fry 3 minutes until crisp-tender.",
            "Return chicken. Add soy sauce and sesame oil. Toss.",
            "Serve over rice immediately."
        ]
    },
    {
        "title": "French Omelette",
        "description": "Classic French omelette with custardy center",
        "difficulty": "INTERMEDIATE",
        "prep_time": 3, "cook_time": 3, "total_time": 6, "servings": 1,
        "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=400",
        "tags": ["breakfast", "french"],
        "steps": [
            "Whisk eggs vigorously for 30 seconds with salt and pepper.",
            "Heat 8-inch pan over medium-high. Add butter and swirl.",
            "Pour eggs. Immediately stir in circles while shaking pan.",
            "When mostly set but still runny, stop stirring. Wait 10 seconds.",
            "Tilt pan and fold omelette in half or roll.",
            "Slide onto plate. Should be pale yellow with no browning."
        ]
    },
    {
        "title": "Perfect Grilled Cheese",
        "description": "Crispy golden grilled cheese sandwich",
        "difficulty": "BEGINNER",
        "prep_time": 5, "cook_time": 8, "total_time": 13, "servings": 1,
        "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400",
        "tags": ["lunch", "comfort"],
        "steps": [
            "Butter one side of each bread slice generously.",
            "Place one slice butter-down in cold pan. Add cheese.",
            "Top with second slice butter-up. Turn heat to medium-low.",
            "Cook until bottom is golden (3-4 min). Don't peek early!",
            "Flip carefully. Cook until golden and cheese melts (3 min).",
            "Remove from heat. Rest 1 minute before cutting."
        ]
    }
]

async def seed():
    conn = await asyncpg.connect(DATABASE_URL)
    
    print("🌱 Seeding 5 recipes...")
    print("")
    
    for i, recipe in enumerate(recipes, 1):
        print(f"[{i}/5] {recipe['title']}")
        
        # Insert recipe with all required fields
        recipe_id = await conn.fetchval('''
            INSERT INTO recipes (id, title, name, description, difficulty, 
                               prep_time_minutes, cook_time_minutes, total_time_minutes,
                               servings, image_url, tags, is_active, is_featured, ai_generated)
            VALUES (gen_random_uuid(), $1, $2, $3, CAST($4 AS difficultylevel), $5, $6, $7, $8, $9, CAST($10 AS jsonb), true, false, false)
            RETURNING id
        ''', recipe['title'], recipe['title'], recipe['description'], 
            recipe['difficulty'], recipe['prep_time'], recipe['cook_time'],
            recipe['total_time'], recipe['servings'], recipe['image_url'],
            json.dumps(recipe['tags']))
        
        # Insert steps with UUID
        for step_num, instruction in enumerate(recipe['steps'], 1):
            await conn.execute('''
                INSERT INTO recipe_steps (id, recipe_id, step_number, instruction, timer_required)
                VALUES (gen_random_uuid(), $1, $2, $3, $4)
            ''', recipe_id, step_num, instruction, False)
        
        print(f"    ✅ {len(recipe['steps'])} steps")
    
    await conn.close()
    print("")
    print("✅ Seeding complete!")
    print("   - 5 recipes created")
    print("   - 30+ steps created")

if __name__ == "__main__":
    asyncio.run(seed())
