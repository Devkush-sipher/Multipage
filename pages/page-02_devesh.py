
import streamlit as st
import pandas as pd
import altair as alt

st.title("Static Site Generator Popularity")


if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        {"Generator": [], "Stars (×1 000)": []}
    )


with st.form("add_row"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Static-site generator (name)", placeholder="e.g. Hugo")
    with c2:
        stars = st.number_input("GitHub stars (×1 000)", min_value=0.0, step=0.1)
    if st.form_submit_button("Add to chart") and name:
        st.session_state.data = pd.concat(
            [st.session_state.data,
             pd.DataFrame({"Generator": [name], "Stars (×1 000)": [stars]})],
            ignore_index=True,
        )


if not st.session_state.data.empty and st.button("Clear data"):
    st.session_state.data = st.session_state.data.iloc[0:0]


if not st.session_state.data.empty:
    chart = (
        alt.Chart(st.session_state.data)
        .mark_bar()
        .encode(
            x=alt.X(
                "Generator",
                sort="-y",
                axis=alt.Axis(labelFontSize=16, titleFontSize=18) 
            ),
            y="Stars (×1 000)",
            tooltip=["Generator", "Stars (×1 000)"],
        )
        .properties(width=650, height=450)
    )
    st.altair_chart(chart, use_container_width=True)
    st.caption("Add rows above to update the graph (values are thousands of GitHub stars).")

