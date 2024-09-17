import streamlit as st

with open('logs.txt', 'r') as f:
    log_contents = f.read()
    f.close()
col1,col2 = st.columns([3,1])
with col1:
    st.title("Logs File")
with col2:
    clearAll = st.button("Clear Logs")
    if clearAll:
        open('logs.txt','w').close()
        st.rerun()

st.text(log_contents)