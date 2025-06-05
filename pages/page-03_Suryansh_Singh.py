import streamlit as st
import random

# Zodiac signs and date ranges
zodiac_signs = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21))
]

# Random predictions for each sign
predictions = {
    "Aries": "Today is a great day to start something new!",
    "Taurus": "Patience will reward you today.",
    "Gemini": "Communication is your strength — use it wisely.",
    "Cancer": "Take time to care for yourself today.",
    "Leo": "Confidence will open unexpected doors.",
    "Virgo": "Your attention to detail will pay off.",
    "Libra": "Balance is key — find your center.",
    "Scorpio": "An exciting opportunity is coming your way.",
    "Sagittarius": "Adventure awaits — say yes!",
    "Capricorn": "Hard work today will lead to great rewards.",
    "Aquarius": "Think outside the box for creative solutions.",
    "Pisces": "Trust your intuition; it won’t let you down."
}

# Function to get zodiac sign
def get_zodiac_sign(month, day):
    for sign, (start_month, start_day), (end_month, end_day) in zodiac_signs:
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign
    return "Unknown"

# Streamlit App
st.title("🔮 Horoscope: Your Future for Today")

st.write("Select your **birth month** and **day** to reveal your Zodiac sign and today's fortune!")

# Month and Day input
months = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

month_name = st.selectbox("Select your birth month", list(months.keys()))
day = st.number_input("Enter your birth day", min_value=1, max_value=31, step=1)

month = months[month_name]

# Validate date before proceeding
if st.button("Tell My Future!"):
    if (month == 2 and day > 29) or (month in [4, 6, 9, 11] and day > 30):
        st.error("Invalid date for selected month.")
    else:
        zodiac_sign = get_zodiac_sign(month, day)
        if zodiac_sign != "Unknown":
            st.write(f"✨ Your Zodiac sign is **{zodiac_sign}**.")
            prediction = predictions.get(zodiac_sign, "Today holds surprises for you.")
            st.success(f"**Your future for today:** {prediction}")
        else:
            st.error("Could not determine Zodiac sign. Please check your date.")

# Footer
st.write("---")
st.caption("🪐 Made with Streamlit & Python")
