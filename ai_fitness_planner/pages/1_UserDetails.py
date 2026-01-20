import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import connect_db
from datetime import date

from backend.calculations import calculate_bmi, calculate_bmr

activity_factor = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725
}

# Sidebar
st.sidebar.title("💪 YOUTHFIT AI")
st.sidebar.caption("AI-Based Workout & Diet Planner")

st.title("📝 Enter Your Details")

# -------------------------------------------------
# 1️⃣ INITIALIZE SESSION STATE ONLY ONCE
if "user" not in st.session_state:
    st.session_state.user = {
        "age": 35,
        "gender": "Male",
        "height": 150,
        "weight": 50,
        "activity": "Moderately Active",
        "goal": "Stay Fit",
        "diet": "Vegetarian"
    }

user = st.session_state.user

# 🔐 SESSION STATE SAFETY (schema guard)
required_keys = ["bmi", "bmr", "calories"]

for key in required_keys:
    if key not in st.session_state.user:
        st.session_state.user[key] = None


# -------------------------------------------------
# 2️⃣ SESSION-BOUND FORM
with st.form("user_form"):

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=70,
        value=user["age"],
        key="age"
    )

    gender = st.radio(
        "Gender",
        ["Male", "Female"],
        index=0 if user["gender"] == "Male" else 1,
        key="gender"
    )

    height = st.number_input(
        "Height (cm)",
        min_value=50,
        max_value=250,
        value=user["height"],
        key="height"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20,
        max_value=300,
        value=user["weight"],
        key="weight"
    )

    activity_options = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
    activity = st.selectbox(
        "Activity Level",
        activity_options,
        index=activity_options.index(user["activity"]),
        key="activity"
    )

    goal_options = ["Weight Loss", "Muscle Gain", "Stay Fit"]
    goal = st.selectbox(
        "Fitness Goal",
        goal_options,
        index=goal_options.index(user["goal"]),
        key="goal"
    )

    diet = st.selectbox(
        "Diet Preference",
        ["Vegetarian", "Non-Vegetarian"],
        index=0 if user["diet"] == "Vegetarian" else 1,
        key="diet"
    )

    submit = st.form_submit_button("Generate My Plan")

if submit:
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(gender, weight, height, age)
    calories = int(bmr * activity_factor[activity])

    st.session_state.user = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity": activity,
        "goal": goal,
        "diet": diet,
        "bmi": bmi,
        "bmr": bmr,
        "calories": calories
    }

    today = date.today().isoformat()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO progress (age, gender, height, weight, goal, calories, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (age, gender, height, weight, goal, calories, today))
    conn.commit()
    conn.close()

    st.success("✅ Details saved successfully!")
    st.info(f"📊 BMI: {bmi:.2f} | 🔥 Daily Calories: {calories}")
