import streamlit as st
st.set_page_config(page_title="Matches", page_icon=None, layout="wide")
with open('logs.txt', 'r') as f:
    log_contents = f.read()
    f.close()
col1,col2 = st.columns([5,1])
with col1:
    st.title("Logs File")
with col2:
    clearAll = st.button("Clear Logs")
    if clearAll:
        open('logs.txt','w').close()
        st.rerun()

st.text(log_contents)