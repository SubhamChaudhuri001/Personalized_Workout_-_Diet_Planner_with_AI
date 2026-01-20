def diet_plan(goal, calories, diet_type):
    if goal == "Weight Loss":
        calories -= 400
    elif goal == "Muscle Gain":
        calories += 300

    protein = (
        "Paneer, Dal, Tofu"
        if diet_type == "Vegetarian"
        else "Eggs, Chicken, Fish"
    )

    return {
        "Calories": int(calories),
        "Protein": protein,
        "Meals": [
            "Breakfast: Oats & fruits",
            "Lunch: Rice/Roti + protein",
            "Dinner: Salad + protein"
        ]
    }
