# 💪 YOUTHFIT AI – Personalized Fitness Planner

An **AI-powered fitness web application** that generates **personalized workout and diet plans** using both **rule-based logic** and **Large Language Models (LLMs)**. Built with **Streamlit**, this project demonstrates clean architecture, AI safety, session-state management, and real-world usability.

---

## 🚀 Project Overview

YOUTHFIT AI helps users:
- Understand their **BMI & calorie needs**
- Get **rule-based OR AI-generated** workout plans
- Get **rule-based OR AI-generated** diet plans
- Download plans as **well-formatted PDFs**
- Track progress via a **dashboard**

The app is designed to be:
- ✅ Beginner-friendly
- ✅ Internship / resume ready
- ✅ Safe from AI hallucination bugs
- ✅ Modular & scalable

---

## 🧠 Why Both Rule-Based + AI?

| Feature | Rule-Based | AI-Based |
|------|-----------|---------|
| Reliability | ✅ High | ⚠ Depends on prompt |
| Personalization | ❌ Limited | ✅ Very High |
| Explainability | ❌ No | ✅ Yes |
| Safety | ✅ Guaranteed | ✅ Controlled |

👉 **Rule-based logic ensures correctness**, while **AI adds personalization & explanations**.

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit
- **Backend Logic:** Python
- **AI Model:** Meta LLaMA (via HuggingFace Inference API)
- **ML Model:** Scikit-learn (Linear Regression)
- **Database:** SQLite
- **PDF Generation:** ReportLab
- **State Management:** Streamlit Session State

---

## 📁 Project Structure

```
ai_fitness_planner/
│
├── app.py                     # Main entry point
├── assets/
│   └── logo.png
│
├── backend/
│   ├── calculations.py        # BMI / BMR calculations
│   ├── workout_logic.py       # Rule-based workout logic
│   ├── diet_logic.py          # Rule-based diet logic
│   ├── ml_model.py            # ML calorie prediction
│   ├── llm_service.py         # LLM integration
│   └── database.py            # SQLite operations
│
├── pages/
│   ├── 1_User_Details.py
│   ├── 2_WorkoutPlan.py
│   ├── 3_DietPlan.py
│   └── 4_ProgressDashboard.py
│
├── requirements.txt
└── README.md
```

---

## 🔐 Key Design Decisions

### ✅ Session State Safety
- Separate session keys for **workout** and **diet**
- Prevents cross-page AI leakage
- No accidental auto-generation

### ✅ AI Generation Control
- AI runs **only on button click**
- Stored safely in session state
- Toggle-based mode switching (AI vs Rule)

### ✅ PDF Stability
- Uses `reportlab.platypus`
- Prevents text overlap / truncation
- Works for **any AI-generated text length**

---

## 🧪 Features

### 🧍 User Details
- Age, gender, height, weight
- Activity level
- Fitness goal

### 🏋️ Workout Plan
- Rule-based OR AI-generated
- Day-wise weekly structure
- BMI analysis
- PDF download

### 🥗 Diet Plan
- Rule-based OR AI-generated
- Calorie targets (formula + ML)
- Macronutrient visualization
- PDF download

### 📊 Progress Dashboard
- Weight progress tracking
- Visual charts
- Future-ready for more metrics

---

## 🛡️ AI Safety Measures

- Strict prompt rules
- Explicit END token handling
- No auto-regeneration
- Session-isolated AI outputs

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

Set HuggingFace token:

```bash
export HF_API_TOKEN=your_token_here
```

Run app:

```bash
streamlit run app.py
```

---

## 🎯 Future Improvements (Optional)

- Save AI plans history
- User authentication
- Mobile UI optimization
- Voice-based guidance

---

## 📄 License

This project is created for **educational and internship purposes**.

---

## 🙏 Acknowledgements

- HuggingFace
- Streamlit Community
- Open-source Python ecosystem

---

### ⭐ If you like this project, consider starring it on GitHub!

