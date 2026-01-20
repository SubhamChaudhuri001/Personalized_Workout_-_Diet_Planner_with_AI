import streamlit as st
import sys
import os
import io
import textwrap
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ml_model import predict_calories
from backend.diet_logic import diet_plan
from backend.llm_service import generate_response

from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# -------------------------------------------------
# SESSION STATE INITIALIZATION (CRITICAL)
if "diet_active_plan" not in st.session_state:
    st.session_state["diet_active_plan"] = None

if "diet_plan_source" not in st.session_state:
    st.session_state["diet_plan_source"] = None

# -------------------------------------------------
# PDF GENERATOR (SAFE FOR ANY AI TEXT)
def generate_ai_explanation_pdf(title, explanation):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Preformatted(title, styles["Title"]))
    story.append(Spacer(1, 20))

    wrapped_text = []
    max_chars = 115

    for line in explanation.split("\n"):
        wrapped_lines = textwrap.wrap(line, max_chars) or [""]
        wrapped_text.extend(wrapped_lines)

    story.append(Preformatted("\n".join(wrapped_text), styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Sidebar
st.sidebar.title("💪 YOUTHFIT AI")
st.sidebar.caption("AI-Based Workout & Diet Planner")

st.title("🍱 Personalized Diet Plan")

# PAGE PROTECTION
if "user" not in st.session_state:
    st.warning("⚠️ Please enter your details on the User Details page first.")
    st.stop()

user = st.session_state.user

# SAFETY CHECK
daily_cal = user.get("calories")
if daily_cal is None:
    st.warning("⚠️ Please submit your details again.")
    st.stop()

# -------------------------------------------------
# CORE CALCULATION (SAFE)
diet_core = diet_plan(user["goal"], daily_cal, user["diet"])

activity_factor = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725
}

ml_calories = predict_calories(
    user["age"],
    user["weight"],
    user["height"],
    activity_factor[user["activity"]]
)

# -------------------------------------------------
# CALORIE INFO
st.subheader("🔥 Daily Calorie Target")
st.success(f"Formula-Based: {diet_core['Calories']} kcal/day")
st.info(f"AI (ML) Estimated: {ml_calories} kcal/day")

st.divider()

# -------------------------------------------------
# MACRO GRAPH
st.subheader("📊 Macronutrient Distribution")

macro_df = pd.DataFrame({
    "Macronutrient": ["Protein", "Carbs", "Fats"],
    "Calories": [
        diet_core["Calories"] * 0.30,
        diet_core["Calories"] * 0.45,
        diet_core["Calories"] * 0.25
    ]
})

st.bar_chart(macro_df.set_index("Macronutrient"))
st.caption("📌 Macronutrient split is formula-based")

st.divider()

# -------------------------------------------------
# MODE TOGGLE
st.subheader("🍱 Diet Plan Generation Mode")
use_ai_plan = st.toggle("Generate diet plan using AI", value=True)

# RESET RULE PLAN WHEN SWITCHING TO AI
if use_ai_plan and st.session_state["diet_plan_source"] == "rule":
    st.session_state["diet_active_plan"] = None
    st.session_state["diet_plan_source"] = None

# -------------------------------------------------
# AI PROMPT
prompt = f"""
You are a certified nutritionist.

Create a daily diet plan using:
- Age: {user['age']}
- Gender: {user['gender']}
- Height: {user['height']} cm
- Weight: {user['weight']} kg
- Goal: {user['goal']}
- Diet Preference: {user['diet']}
- Activity Level: {user['activity']}
- Daily Calories: {diet_core['Calories']} kcal

Rules:
- Include breakfast, lunch, snacks, dinner
- Simple & affordable foods
- Beginner friendly
- Brief explanation
- End with the word END
"""

# -------------------------------------------------
# AI MODE
if use_ai_plan:
    st.subheader("🤖 AI-Generated Diet Plan")

    if st.session_state["diet_active_plan"] is None:
        st.info("Click below to generate your AI diet plan.")

    if st.button("🚀 Generate AI Diet Plan"):
        with st.spinner("AI is creating your diet plan..."):
            ai_text = generate_response(prompt)

        if ai_text is None:#
            st.error("⚠️ AI service is temporarily busy. Please try again later.")#
            st.info("💡 Tip: Free AI APIs have usage limits.")#
            st.stop()#

        if not ai_text.strip().endswith("END"):
            ai_text += "\n\n[Note: Response ended early by the model]"

        st.session_state["diet_active_plan"] = ai_text
        st.session_state["diet_plan_source"] = "ai"


    if (
        st.session_state["diet_active_plan"]
        and st.session_state["diet_plan_source"] == "ai"
):
        st.write(st.session_state["diet_active_plan"])

# RULE-BASED MODE
else:
    st.subheader("🔹 Recommended Diet Plan (Rule-Based)")

    st.write("🍗 **Protein Sources:**", diet_core["Protein"])
    for meal in diet_core["Meals"]:
        st.write("•", meal)

    st.session_state["diet_active_plan"] = "\n".join(diet_core["Meals"])
    st.session_state["diet_plan_source"] = "rule"

    st.expander("💡 Nutrition Tips").write("""
- Drink at least 3L water daily  
- Avoid processed sugar  
- Eat every 3–4 hours  
- Maintain sufficient protein intake  
""")

# -------------------------------------------------
# PDF DOWNLOAD (STRICT)
if (
    st.session_state["diet_active_plan"]
    and (
        (use_ai_plan and st.session_state["diet_plan_source"] == "ai")
        or (not use_ai_plan and st.session_state["diet_plan_source"] == "rule")
    )
):

    pdf = generate_ai_explanation_pdf(
        "YOUTHFIT AI – Diet Plan",
        st.session_state["diet_active_plan"]
    )

    st.download_button(
        "📄 Download Diet Plan (PDF)",
        pdf,
        "YOUTHFIT_AI_Diet_Plan.pdf",
        "application/pdf"
    )

# -------------------------------------------------
# MODE LABEL
if st.session_state["diet_plan_source"] == "ai":
    st.caption("🤖 AI-generated personalized diet plan")
elif st.session_state["diet_plan_source"] == "rule":
    st.caption("📋 Rule-based diet plan")
