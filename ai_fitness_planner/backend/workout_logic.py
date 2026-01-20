def workout_plan(goal, bmi):
    if goal == "Weight Loss":
        return [
            "30–40 min Cardio",
            "Jump rope",
            "Bodyweight squats",
            "Plank & core exercises"
        ]
    elif goal == "Muscle Gain":
        return [
            "Strength training",
            "Chest & Back workouts",
            "Leg day & shoulder training",
            "Progressive overload"
        ]
    else:
        return [
            "Mixed cardio + strength",
            "Yoga & stretching",
            "Light resistance training"
        ]
