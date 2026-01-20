# # backend/calculations.py
# def calculate_bmi(weight, height):
#     """
#     Safe BMI calculation
#     weight: kg
#     height: cm
#     """
#     if height is None or height <= 0:
#         return None
#     if weight is None or weight <= 0:
#         return None
#     return weight / ((height / 100) ** 2)


# def calculate_bmr(gender, weight, height, age):
#     """
#     Mifflin-St Jeor Formula
#     """
#     if gender == "Male":
#         return 10 * weight + 6.25 * height - 5 * age + 5
#     else:
#         return 10 * weight + 6.25 * height - 5 * age - 161

# backend/calculations.py

def calculate_bmi(weight, height):
    if height is None or height <= 0:
        return None
    if weight is None or weight <= 0:
        return None
    return round(weight / ((height / 100) ** 2), 2)


def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_daily_calories(bmr, activity):
    activity_factor = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }

    return int(bmr * activity_factor.get(activity, 1.2))
