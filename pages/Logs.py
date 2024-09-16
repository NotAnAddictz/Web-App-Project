import streamlit as st

with open('logs.txt', 'r') as f:
    log_contents = f.read()
st.title("Logs File")
st.text(log_contents)