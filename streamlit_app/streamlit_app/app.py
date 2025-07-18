import streamlit as st

st.set_page_config(page_title="Disease Predictor", layout="centered")

import joblib
import numpy as np

# === Load saved artifacts ===
model = joblib.load("../../models/random_forest.pkl")
label_encoder = joblib.load("../../models/label_encoder.pkl")
symptom_list = joblib.load("../../models/symptom_list.pkl")
scaler = joblib.load("../../models/scaler.pkl")

# === Sidebar ===
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=100)
st.sidebar.title("About")
st.sidebar.info(
    "This AI-powered app predicts possible diseases based on your selected symptoms. "
    "Select symptoms from the list and click 'Predict Disease'."
)
st.sidebar.markdown("---")
st.sidebar.write("Made with by Jagdish")

# === Main UI ===
st.title("🩺 AI Disease Predictor")
st.markdown(
    """
    <style>
    .result-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True
)
st.write("Select your symptoms below and let the AI suggest a possible disease.")

# === Multiselect symptom input ===
selected_symptoms = st.multiselect(
    "Select Symptoms",
    options=symptom_list,
    help="You can select multiple symptoms that you are experiencing."
)

# === Predict button ===
if st.button("Predict Disease"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        input_vector = [1 if symptom in selected_symptoms else 0 for symptom in symptom_list]
        input_scaled = scaler.transform([input_vector])
        prediction = model.predict(input_scaled)
        disease_name = label_encoder.inverse_transform(prediction)[0]

        st.markdown(
            f"<div class='result-box'><h3>🧠 Predicted Disease: <span style='color:#0072C6'>{disease_name}</span></h3></div>",
            unsafe_allow_html=True
        )
        st.info("This prediction is based on the symptoms you selected. For medical advice, consult a healthcare professional.")

# === Footer ===
st.markdown("---")
st.markdown("<center>Made with by <b>Jagdish</b></center>", unsafe_allow_html=True)
