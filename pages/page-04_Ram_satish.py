import streamlit as st
import datetime

st.title("🏐 Volleyball Score Tracker")

# Team names
team1 = st.text_input("Team 1", "Team A")
team2 = st.text_input("Team 2", "Team B")

# Session state
for k in ["t1", "t2", "s1", "s2", "over"]: 
    if k not in st.session_state: st.session_state[k] = 0 if k != "over" else False

# Score buttons
c1, c2 = st.columns(2)
with c1: 
    if st.button(f"Point: {team1}"): 
        if not st.session_state.over: st.session_state.t1 += 1
with c2: 
    if st.button(f"Point: {team2}"): 
        if not st.session_state.over: st.session_state.t2 += 1

# Display scores
st.write(f"## {team1}: {st.session_state.t1} | Sets: {st.session_state.s1}")
st.write(f"## {team2}: {st.session_state.t2} | Sets: {st.session_state.s2}")

# Set win logic
if st.session_state.t1 >= 25 and (st.session_state.t1 - st.session_state.t2) >= 2:
    st.success(f"{team1} wins the set!")
    st.session_state.s1 += 1; st.session_state.over = True
elif st.session_state.t2 >= 25 and (st.session_state.t2 - st.session_state.t1) >= 2:
    st.success(f"{team2} wins the set!")
    st.session_state.s2 += 1; st.session_state.over = True

# Match winner
