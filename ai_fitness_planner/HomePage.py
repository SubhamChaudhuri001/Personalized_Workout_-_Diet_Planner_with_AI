import streamlit as st
import os
from PIL import Image
from backend.database import create_table

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="YOUTHFIT AI",
    page_icon="💪",
    layout="centered"
)

create_table()

# ✅ Load Logo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
logo = Image.open(LOGO_PATH)

st.image(logo, width=180)

# Sidebar
st.sidebar.title("💪 YOUTHFIT AI")
st.sidebar.caption("AI-Based Workout & Diet Planner")

# Main Content
st.title("💪 AI-Based Personalized Workout & Diet Planner")

st.markdown("""
### Train Smarter. Eat Better. Live Healthier.

This AI-powered web application generates **personalized workout and diet plans**
based on your body metrics, fitness goals, and lifestyle.
""")

st.info("👈 Use the sidebar to navigate through the app")

st.markdown("---")

st.subheader("✨ Key Features")
st.write("""
- Personalized workout recommendations  
- AI-based diet planning  
- BMI & calorie calculation  
- Progress tracking dashboard  
""")

st.success("🚀 Internship-Ready AI Project")