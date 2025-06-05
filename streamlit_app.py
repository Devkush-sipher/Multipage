# Multipage_app.py
"""
Entry point for the “Multipage App”.

• Keep this file at the project root.
• Put each feature page (app.py, hello.py, …) inside a folder named `pages/`.
  Streamlit will discover them and show them in the sidebar automatically.
• Launch with:  streamlit run Multipage_app.py
"""

import streamlit as st

# ----- basic page config -----
st.set_page_config(
    page_title="Multipage App",
    page_icon="📚",
    layout="wide",
)

# ----------- Hero section -----------
st.markdown(
    """
    <h1 style="text-align:center; font-size:3.5rem; font-weight:800;">
        Multipage App
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align:center; font-size:1.25rem;">
        <strong>created by</strong><br>
        Devesh&nbsp;Kushwaha<br>
        Suryansh&nbsp;Singh<br>
        Ram&nbsp;Satish<br>
        Vansh&nbsp;Seth<br>
        Vaishnav&nbsp;Pasarge
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown(
    "<h3 style='text-align:center;'>✅ Check out the <em>side&nbsp;menu</em> to see all the pages.</h3>",
    unsafe_allow_html=True,
)
