# ---------------- Imports ----------------
import streamlit as st
import pandas as pd
import joblib
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow import keras
from db_config import users_collection


# ------------------ Simple Auth Setup ------------------
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

def login_page():
    st.title("🌱 Smart Farming AI Advisor")
    st.subheader("🔐 Login or Sign Up to Continue")

    option = st.radio("Select an option:", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            user = users_collection.find_one({"username": username, "password": password})
            if user:
                st.session_state.user_authenticated = True
                st.success(f"Welcome back, {username} 👋")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif option == "Sign Up":
        if st.button("Create Account"):
            existing_user = users_collection.find_one({"username": username})
            if existing_user:
                st.warning("Username already exists. Try logging in.")
            elif len(username.strip()) == 0 or len(password.strip()) == 0:
                st.warning("Please fill out both fields.")
            else:
                users_collection.insert_one({
                    "username": username,
                    "password": password
                })
                st.success("Account created successfully! You can now log in.")



# ---------------- DASHBOARD FUNCTION ----------------
def dashboard_page():
    st.title("🌾 Smart Farming AI Advisor")
    st.sidebar.header("🌿 Input Field Conditions")

    # ---------------- Load Trained Models ----------------
    model_irrigation = joblib.load("models/model_irrigation.pkl")
    model_pesticide  = joblib.load("models/model_pesticide.pkl")
    model_health     = joblib.load("models/model_health.pkl")
    model_yield      = joblib.load("models/model_yield.pkl")

    # --- User Inputs (Sliders) ---
    moisture = st.sidebar.slider("Soil Moisture", 0.0, 1.0, 0.2)
    rainfall = st.sidebar.slider("Rainfall (mm)", 0.0, 150.0, 20.0)
    humidity = st.sidebar.slider("Average Humidity (%)", 10, 100, 60)
    mean_temp = st.sidebar.slider("Mean Temperature (°C)", 5, 45, 28)
    min_temp = st.sidebar.slider("Min Temperature (°C)", 0, 40, 20)
    max_temp = st.sidebar.slider("Max Temperature (°C)", 10, 55, 35)
    alkaline = st.sidebar.selectbox("Is soil alkaline?", [0, 1])
    sandy = st.sidebar.selectbox("Is soil sandy?", [0, 1])
    chalky = st.sidebar.selectbox("Is soil chalky?", [0, 1])
    clay = st.sidebar.selectbox("Is soil clay?", [0, 1])

    # --- Input Summary ---
    input_df = pd.DataFrame([{
        "Moisture": moisture,
        "rainfall": rainfall,
        "Average Humidity": humidity,
        "Mean Temp": mean_temp,
        "Min temp": min_temp,
        "max Temp": max_temp,
        "alkaline": alkaline,
        "sandy": sandy,
        "chalky": chalky,
        "clay": clay
    }])

    st.write("### 📋 Input Summary")
    st.dataframe(input_df)

    # ---------------- Random Forest Predictions ----------------
    X_i = input_df[["Moisture", "rainfall", "Average Humidity", "Mean Temp"]]
    X_p = input_df[["Moisture", "rainfall", "Average Humidity", "Mean Temp", "alkaline", "sandy", "clay"]]
    X_h = input_df[["Moisture", "Average Humidity", "Mean Temp", "alkaline", "sandy", "clay"]]

    pred_irrigation = model_irrigation.predict(X_i)[0]
    pred_pesticide = model_pesticide.predict(X_p)[0]
    pred_health = model_health.predict(X_h)[0]

    input_df["pesticide_dose"] = pred_pesticide
    input_df["crop_health_score"] = pred_health

    X_y = input_df[[
        "Moisture", "rainfall", "Average Humidity", "Mean Temp", "Min temp", "max Temp",
        "alkaline", "sandy", "chalky", "clay", "pesticide_dose", "crop_health_score"
    ]]
    pred_yield = max(0, model_yield.predict(X_y)[0])

    # --- Results Display ---
    st.markdown("---")
    st.subheader("🤖 AI Predictions")
    st.success(f"💧 Irrigation Needed: {'Yes' if pred_irrigation == 1 else 'No'}")
    st.info(f"🧪 Pesticide Dose: {pred_pesticide:.2f} ml/hectare")
    st.success(f"🌿 Crop Health Score: {pred_health:.2f}")
    st.success(f"🌾 Predicted Yield: {pred_yield:.2f} kg/hectare")

    # ---------------- Banana Leaf Image Analysis ----------------
    st.markdown("---")
    st.subheader("🍌 Banana Leaf Health Detection")
    st.write("Upload or capture an image of your banana leaf to check its condition:")

    model = tf.keras.models.load_model('models/banana_leaf_fixed.keras', compile=False)
    st.write("Model Input Shape:", model.input_shape)

    banana_classes = [
        "Banana Sigatoka Disease",
        "Banana Healthy",
        "Banana Xanthomonas Wilt"
    ]

    uploaded_image = st.file_uploader("Upload a banana leaf image", type=["jpg", "jpeg", "png"])
    camera_image = st.camera_input("Or take a picture")
    image_source = uploaded_image or camera_image

    if image_source:
        image = Image.open(image_source).convert("RGB").resize((200, 200))
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)[0]
        confidence = np.max(preds) * 100
        predicted_label = banana_classes[np.argmax(preds)]

        st.image(image, caption=f"Predicted: {predicted_label} ({confidence:.1f}% confidence)", use_column_width=True)
        st.write("Banana class probabilities:", {banana_classes[i]: f"{preds[i]*100:.1f}%" for i in range(len(banana_classes))})

        if "Healthy" in predicted_label:
            st.success("✅ The banana plant appears healthy!")
        else:
            st.warning(f"⚠️ Detected {predicted_label}. Consider treatment.")


# ------------------ Page Routing ------------------
if not st.session_state.user_authenticated:
    login_page()
else:
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update({"user_authenticated": False}))
    dashboard_page()
