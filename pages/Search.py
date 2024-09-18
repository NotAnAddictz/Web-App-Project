import streamlit as st
import functions
import pandas as pd
import logging
st.set_page_config(page_title="Matches", page_icon=None, layout="wide")
LOGFILE = "logs.txt"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(LOGFILE)  
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler) 

if 'teams' not in st.session_state or 'matches' not in st.session_state:
    teams,matches = functions.readFiles()
    st.session_state['teams'] = teams
    st.session_state['matches'] = matches

# Displaying Matches
teams = st.session_state['teams']
matches = st.session_state['matches']

st.title("Search Team Information")
with st.form("Search"):
    teamName = st.selectbox("Team Name",
                (teams['TeamName'].unique()))
    submitted = st.form_submit_button('Search')
    if submitted:
        st.header("Team Information")
        team = teams[teams['TeamName']== teamName]
        team = team.drop(columns = 'Position')
        st.table(team.style.format(precision=0))
        st.header("Matches")
        match = pd.concat([matches[matches['Team 1']== teamName],matches[matches['Team 2']== teamName]])
        if match.empty:
            st.write("No matches found")
        else:
            st.table(match.style.format(precision=0))
            logger.info(f"Searched for {teamName}")
