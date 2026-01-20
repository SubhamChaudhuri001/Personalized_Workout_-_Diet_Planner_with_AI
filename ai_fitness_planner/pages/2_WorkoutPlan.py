import streamlit as st
import sys
import os
import io
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.workout_logic import workout_plan
from backend.llm_service import generate_response

from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ---------------------------------------
# PDF GENERATOR (SAFE FOR AI TEXT)
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
    max_chars = 115  # safe wrap for A4

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

st.title("🏋️ Personalized Workout Plan")

# PAGE PROTECTION
if "user" not in st.session_state:
    st.warning("⚠️ Please enter your details on the User Details page first.")
    st.stop()

user = st.session_state.user

# SAFETY CHECK
bmi = user.get("bmi")
if bmi is None:
    st.warning("⚠️ Please submit your details again.")
    st.stop()

# ---------------------------------------
# BMI INFO (ALWAYS SHOWN)
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

category = bmi_category(bmi)

st.subheader("📏 BMI Analysis")
st.metric("BMI Value", f"{bmi:.2f}")
st.info(f"🧠 BMI Category: **{category}**")

st.progress(min(bmi / 40, 1.0))
st.caption("BMI scale (0–40), Visual indicator only, not a medical assessment.")

st.divider()

# ---------------------------------------
# AI TOGGLE
use_ai_plan = st.toggle("Generate workout plan using AI", value=True)

# ✅ CLEAR RULE-BASED PLAN WHEN SWITCHING TO AI
if use_ai_plan and st.session_state.get("plan_source") == "rule":
    st.session_state.pop("active_workout_plan", None)
    st.session_state.pop("plan_source", None)

# ---------------------------------------
prompt = f"""
You are a certified fitness trainer.

Create a structured 7-day workout plan using these details:
- Age: {user['age']}
- Gender: {user['gender']}
- Height: {user['height']} cm
- Weight: {user['weight']} kg
- BMI: {bmi:.2f}
- Fitness Goal: {user['goal']}

Rules:
- Day-wise plan (Monday–Sunday)
- Include rest days
- Beginner friendly
- Use bullet points
- End the response with the word END
"""
# AI MODE
if use_ai_plan:
    st.subheader("🚀 AI-Generated Workout Plan")

    if "active_workout_plan" not in st.session_state:
        st.info("Click the button below to generate your AI workout plan.")

    if st.button("💪🏻 Generate AI Workout Plan"):
        with st.spinner("AI is creating your workout plan..."):
            ai_plan_text = generate_response(prompt)

        if not ai_plan_text.strip().endswith("END"):
            ai_plan_text += "\n\n[Note: Response ended early by the model]"

        st.session_state.active_workout_plan = ai_plan_text
        st.session_state.plan_source = "ai"


    # ✅ DISPLAY STORED PLAN (NO REGENERATION)
    if (
        "active_workout_plan" in st.session_state
        and st.session_state.get("plan_source") == "ai"
    ):
        st.write(st.session_state.active_workout_plan)


# ---------------------------------------
# FALLBACK MODE (RULE-BASED)
else:
    st.subheader("🔹 Recommended Workout Plan (Rule-Based)")

    plan = workout_plan(user["goal"], bmi)
    st.session_state.active_workout_plan = "\n".join(plan)
    st.session_state.plan_source = "rule"

    for exercise in plan:
        st.write("✅", exercise)

    st.expander("📅 Weekly Schedule").write("""
Monday – Cardio  
Tuesday – Upper Body  
Wednesday – Rest  
Thursday – Lower Body  
Friday – Core  
Saturday – Optional Cardio  
Sunday – Rest
""")

# ---------------------------------------
# PDF DOWNLOAD (ACTIVE PLAN ONLY)
if (
    "active_workout_plan" in st.session_state
    and (
        (use_ai_plan and st.session_state.get("plan_source") == "ai")
        or (not use_ai_plan)
    )
):

    pdf = generate_ai_explanation_pdf(
        "YOUTHFIT AI – Workout Plan",
        st.session_state.active_workout_plan
    )

    st.download_button(
        "📄 Download Workout Plan (PDF)",
        pdf,
        "YOUTHFIT_AI_Workout_Plan.pdf",
        "application/pdf"
    )

if "plan_source" in st.session_state:
    if st.session_state.plan_source == "ai":
        st.caption("🤖 This is an AI-generated personalized plan")
    elif st.session_state.plan_source == "rule":
        st.caption("📋 This is a rule-based (normal) plan")

