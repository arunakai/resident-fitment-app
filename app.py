import streamlit as st
import requests
import pdfplumber
import re

# Your Flask backend endpoint (running locally)
FLASK_API_URL = "https://resident-fitment-api.onrender.com/predict"

# Function to extract values from a structured PDF
def extract_pdf_data(uploaded_file):
    extracted = {}
    patterns = {
        "age": r"Age:\s*(\d+)",
        "cognitive_score": r"Cognitive Score:\s*([0-9.]+)",
        "mobility": r"Mobility Level:\s*([0-9.]+)",
        "behavioral_stability": r"Behavioral Stability:\s*([0-9.]+)",
        "continence": r"Continence Level:\s*([0-9.]+)",
        "comorbidity_index": r"Comorbidity Index:\s*([0-9.]+)",
        "support_system": r"Support System:\s*([0-9.]+)",
        "nutrition": r"Nutritional Risk Score:\s*([0-9.]+)",
        "mental_health": r"Mental Health Score:\s*([0-9.]+)",
        "pain_level": r"Chronic Pain Score:\s*([0-9.]+)",
        "language_barrier": r"Language Barrier Score:\s*([0-9.]+)",
        "cultural_fit": r"Cultural/Religious Alignment:\s*([0-9.]+)"
    }

    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted[key] = float(match.group(1)) if match else 0.5  # default value if not found

    return extracted

# ---- UI Starts Here ----

st.set_page_config(page_title="Resident Fitment Evaluation", layout="centered")
st.title("🏥 Resident Application Fitment Evaluation (Burton Manor)")
st.markdown("Evaluate LTC resident fitment based on application details.")

uploaded_file = st.file_uploader("📄 Upload Resident Application PDF", type=["pdf"])

# ---- If PDF is Uploaded ----
if uploaded_file:
    extracted = extract_pdf_data(uploaded_file)

    st.subheader("🧾 Extracted Fitment Values")
    for k, v in extracted.items():
        st.write(f"**{k.replace('_', ' ').title()}**: {v}")

    if st.button("🔍 Evaluate Fitment (from PDF)"):
        features = [
            extracted["age"] / 100.0,
            extracted["cognitive_score"],
            extracted["mobility"],
            extracted["behavioral_stability"],
            extracted["continence"],
            extracted["comorbidity_index"],
            extracted["support_system"],
            extracted["nutrition"],
            extracted["mental_health"],
            extracted["pain_level"],
            extracted["language_barrier"],
            extracted["cultural_fit"]
        ]
        try:
            response = requests.post(FLASK_API_URL, json={"features": features})
            result = response.json()
            st.success(result["message"])
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---- If No PDF: Show Manual Input Form ----
else:
    st.subheader("✍️ Manual Input Form")
    with st.form("manual_input_form"):
        age = st.slider("Age", 50, 100, 75)
        cognitive_score = st.slider("Cognitive Function Score", 0.0, 1.0, 0.5)
        mobility = st.slider("Mobility Level", 0.0, 1.0, 0.5)
        behavioral_stability = st.slider("Behavioral Stability", 0.0, 1.0, 0.5)
        continence = st.slider("Continence Level", 0.0, 1.0, 0.5)
        comorbidity_index = st.slider("Comorbidity Index", 0.0, 1.0, 0.5)
        support_system = st.slider("Support System Availability", 0.0, 1.0, 0.5)
        nutrition = st.slider("Nutritional Risk Score", 0.0, 1.0, 0.5)
        mental_health = st.slider("Mental Health Score", 0.0, 1.0, 0.5)
        pain_level = st.slider("Chronic Pain Score", 0.0, 1.0, 0.5)
        language_barrier = st.slider("Language Barrier Score", 0.0, 1.0, 0.5)
        cultural_fit = st.slider("Cultural/Religious Alignment", 0.0, 1.0, 0.5)
        submit = st.form_submit_button("🔍 Evaluate Fitment (Manual Input)")

    if submit:
        features = [
            age / 100.0,
            cognitive_score,
            mobility,
            behavioral_stability,
            continence,
            comorbidity_index,
            support_system,
            nutrition,
            mental_health,
            pain_level,
            language_barrier,
            cultural_fit
        ]
        try:
            response = requests.post(FLASK_API_URL, json={"features": features})
            result = response.json()
            st.success(result["message"])
        except Exception as e:
            st.error(f"❌ Error: {e}")
