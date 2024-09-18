import functions
import streamlit as st
import pandas as pd
import logging

LOGFILE = "logs.txt"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(LOGFILE)  
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler) 

st.set_page_config(page_title="Matches", page_icon=None, layout="wide")
st.title("Matches")
if 'teams' not in st.session_state or 'matches' not in st.session_state:
    teams,matches = functions.readFiles()
    st.session_state['teams'] = teams
    st.session_state['matches'] = matches

# Displaying Matches
teams = st.session_state['teams']
matches = st.session_state['matches']
modifiedMatches = matches.fillna(int(0))
modifiedMatches["Delete?"] = False
# Make Delete be the first column
modifiedMatches = modifiedMatches[["Delete?"] + modifiedMatches.columns[:-1].tolist()]
with st.form("Matches"):
    editedDF = st.data_editor(data=modifiedMatches,
                              width=2000,
                              hide_index=True,key="matchform")
    submitted = st.form_submit_button("Update")
    if submitted:
        editedDF['Result'] = editedDF.apply(functions.getResult,axis=1)
        rowsToDelete = functions.callback(editedDF)
        editedDF = editedDF.drop(columns=['Delete?'])
        if len(rowsToDelete) >0:
            matches = editedDF.drop(rowsToDelete).reset_index(drop=True)
        verified = functions.verifyTable(editedDF,teams)
        if verified == True:
            if len(rowsToDelete) >0:
                matches = editedDF.drop(rowsToDelete).reset_index(drop=True)
            if matches.empty:
                del st.session_state['matches']
                functions.remove('matches')
            else:
                st.session_state['matches'] = matches
                st.session_state['teams'] = functions.updateScores(matches,teams)
                functions.save('matches',st.session_state['matches'])
            logger.info("Edited Matches")
            st.rerun()
        else:
             st.toast(f"Error: {verified}")


# Adding matches
newScore= st.text_area(label = "Add Matches",placeholder="First Team, Second Team, First Team Goals, Second Team Goals")
col1,col2 = st.columns([15,1])

with col1:
    submitted = st.button("Add Result")
with col2:
    removeAll = st.button('Clear All')

if submitted:
    index,matches = functions.addResults(newScore.strip(),matches,teams)
    if index == -1:
        matches['Result'] = matches.apply(functions.getResult,axis=1)
        st.session_state['matches'] = matches
        functions.save('matches',st.session_state['matches'])
        logger.info(f"Added Matches: {newScore.replace("\n",",")}")
        st.session_state['teams'] = functions.updateScores(matches,teams) 
        st.rerun()
    else:
        st.toast(f"Error in line {index}: {matches}")
# Clearing all matches
if removeAll:
    functions.remove('matches')
    del st.session_state['matches']
    logger.info("Removed All Matches")
    st.rerun()