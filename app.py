import streamlit as st

st.title("Simulation UI")

win_rate = st.slider("Choose Win Rate (%)", min_value=40, max_value=100, value=55)
st.pyplot(plt)