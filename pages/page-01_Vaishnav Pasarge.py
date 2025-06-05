import streamlit as st
import json
import os

DATA_FILE = "calories_data.json"

def load_calories():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_calories(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

st.set_page_config(page_title="Health Tracker", page_icon="🍎")

st.title("🏥 Health Tracker App")

# --- BMI Calculator ---
st.header("🧮 BMI Calculator")

height = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0)
weight = st.number_input("Enter your weight (kg)", min_value=10.0, max_value=300.0)

if st.button("Calculate BMI"):
    if height and weight:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        st.success(f"Your BMI is: {bmi:.2f}")
        if bmi < 18.5:
            st.warning("You are underweight.")
        elif 18.5 <= bmi < 25:
            st.info("You are in the normal range.")
        elif 25 <= bmi < 30:
            st.warning("You are overweight.")
        else:
            st.error("You are obese.")
    else:
        st.error("Please enter both height and weight.")

# --- Calorie Intake Tracker ---
st.header("🍽️ Calorie Intake Tracker")

calories_data = load_calories()

with st.form("calorie_form"):
    meal = st.text_input("Meal / Food Item")
    cal = st.number_input("Calories", min_value=0, step=10)
    submitted = st.form_submit_button("Add")

    if submitted and meal.strip():
        calories_data.append({"meal": meal.strip(), "calories": cal})
        save_calories(calories_data)
        st.experimental_rerun()

if calories_data:
    st.subheader("Today's Intake")
    total = 0
    for i, item in enumerate(calories_data):
        st.write(f"🍽️ {item['meal']} — {item['calories']} kcal")
        total += item['calories']
    st.markdown(f"**🔢 Total Calories: {total} kcal**")

    if st.button("🧹 Clear Meals"):
        calories_data.clear()
        save_calories(calories_data)
        st.experimental_rerun()
else:
    st.info("No meals logged yet.")

