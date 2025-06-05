import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# Multipage_app.py
"""
Main router for the “Multipage app”.
Drop this file in the same folder as the other page-files and run:
    streamlit run Multipage_app.py
"""

import streamlit as st
import runpy           # lets us execute other .py files in the same process
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

st.set_page_config(page_title="Multipage app", page_icon="📚", layout="wide")

# ---------- Menu ----------
selected = option_menu(
    menu_title="Multipage app",          # shows as a centred title bar
    options=[
        "Static-Site Generator",
        "Volleyball Score Tracker",
        "Health Tracker",
        "Horoscope",
        "Financial Dashboard",
    ],
    icons=[
        "bar-chart-fill",
        "trophy-fill",
        "heart-pulse-fill",
        "moon-stars-fill",
        "bank",
    ],                           # any Bootstrap icon name
    default_index=0,
    orientation="horizontal",    # replicates the look in the YouTube video
    styles={
        "container": {"padding": "0!important"},
        "nav-link": {"font-size": "18px", "padding": "10px 18px"},
        "nav-link-selected": {"background-color": "#6c63ff"},
    },
)

# ---------- Simple router ----------
PAGE_TO_FILE = {
    "Static-Site Generator": "app.py",             # :contentReference[oaicite:6]{index=6}
    "Volleyball Score Tracker": "hello.py",        # :contentReference[oaicite:7]{index=7}
    "Health Tracker": "healthTrackerApp.py",       # :contentReference[oaicite:8]{index=8}
    "Horoscope": "Streamlit.py",                   # :contentReference[oaicite:9]{index=9}
    "Financial Dashboard": "Fin_Dashboard.py",     # :contentReference[oaicite:10]{index=10}
}

runpy.run_path(PAGE_TO_FILE[selected], run_name="__main__")
