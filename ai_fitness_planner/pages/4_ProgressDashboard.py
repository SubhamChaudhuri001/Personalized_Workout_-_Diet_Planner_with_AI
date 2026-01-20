import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_progress

# Sidebar
st.sidebar.title("💪 YOUTHFIT AI")
st.sidebar.caption("AI-Based Workout & Diet Planner")

st.title("📊 Progress Dashboard")

# ✅ PAGE PROTECTION (SAME AS OTHER PAGES)
if "user" not in st.session_state:
    st.warning("⚠️ Please enter your details on the User Details page first.")
    st.stop()

# ✅ GET USER DATA
user = st.session_state.user

# ✅ SESSION SCHEMA GUARD
bmi = user.get("bmi")
if bmi is None:
    st.warning("⚠️ Please submit your details again.")
    st.stop()

# ---------------------------------------
# FETCH DATA FROM DATABASE
data = get_progress()

# ✅ SECOND SAFETY CHECK (DB DATA)
if not data:
    st.info("📌 No progress data recorded yet. Submit your details to start tracking.")
    st.stop()

# ---------------------------------------

# DATAFRAME
df = pd.DataFrame(data, columns=["Date", "Weight"])

# Convert Date & Weight properly
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")

# Drop invalid rows
df.dropna(inplace=True)

# Sort by date (VERY IMPORTANT)
df = df.sort_values("Date")

# Handle multiple entries on same day (keep latest)
df = df.groupby("Date", as_index=False).last()

# ---------------------------------------
# METRICS
latest_weight = df["Weight"].iloc[-1]
start_weight = df["Weight"].iloc[0]
weight_change = round(latest_weight - start_weight, 2)

# -----------------------------------
# HEALTH SUMMARY CARD
st.subheader("📌 Health Summary")

bmi = user["bmi"]
calories = user["calories"]
goal = user["goal"]

# BMI Category
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

col1, col2 = st.columns(2)

with col1:
    st.metric("⚖️ Weight", f"{latest_weight:.1f} kg")
    st.metric("🔥 Daily Calories", f"{calories} kcal")

with col2:
    st.metric("📏 BMI", f"{bmi:.2f}")
    st.metric("🎯 Goal", goal)

st.caption(f"🧠 BMI Category: **{category}**")
st.divider()


# WEIGHT PROGRESS CHART
st.subheader("📉 Weight Progress Over Time")

st.line_chart(
    df.set_index("Date")["Weight"],
    height=350
)

st.caption("📌 Progress is tracked from user submission")

st.success("🎯 Consistency is the key to success!")

if weight_change < 0:
    st.success(f"⬇️ You have lost {abs(weight_change)} kg. Great progress!")
elif weight_change > 0:
    st.warning(f"⬆️ You have gained {weight_change} kg. Review diet & workouts.")
else:
    st.info("⚖️ Your weight is stable. Consistency matters.")

st.metric("📆 Days Tracked", df["Date"].nunique())
