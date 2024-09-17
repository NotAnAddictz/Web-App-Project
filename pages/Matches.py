import functions
import streamlit as st
import pandas as pd
import logging

MATCHLIST = 'scoreList.xlsx'
TEAMLIST = 'teams.xlsx'
LOGFILE = "logs.txt"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(LOGFILE)  
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler) 

st.title("Matches")
st.session_state['Button'] = False
try:
    teams = pd.read_excel(TEAMLIST,header = 0)
except:
    teams = None
try: 
    matches = pd.read_excel(MATCHLIST,header = 0)
    
except:
    matches = pd.DataFrame({"Team 1": pd.Series(dtype='str'),
                            "Team 2": pd.Series(dtype='str'),
                            "Team 1 Goal": pd.Series(dtype="int"),
                            "Team 2 Goal": pd.Series(dtype="int"),
                            "Result": pd.Series(dtype='str')
                            })
    matches.to_excel(MATCHLIST,index=False)

# Displaying Matches
with st.form("Matches"):
    editedDF = st.data_editor(data=matches,width=1000,hide_index=True,key="matches")
    submitted = st.form_submit_button("Update")
    if submitted:
        verified = functions.verifyTable(editedDF,teams)
        if verified == True:
            editedDF['Result'] = editedDF.apply(functions.getResult,axis=1)
            editedDF.to_excel(MATCHLIST,index=False)
            logger.info("Edited Matches")
            st.rerun()
        else:
             st.toast(f"Error: {verified}")


# Adding matches
newScore= st.text_area(label = "Add Matches",placeholder="First Team, Second Team, First Team Goals, Second Team Goals")
col1,col2 = st.columns([1,1])
with col1:
    submitted = st.button("Add Result")
if submitted:
    index,matches = functions.addResults(newScore,matches,teams)
    if index == -1:
        matches['Result'] = matches.apply(functions.getResult,axis=1)
        matches.to_excel(MATCHLIST,index=False)
        logger.info(f"Added Matches: {newScore}")
        st.rerun()
    else:
        st.toast(f"Error in line {index}: {matches}")
with col2:
    removeAll = st.button('Clear All')

# Clearing all matches
if removeAll:
    functions.remove(MATCHLIST)
    logger.info("Removed All Matches")
    st.rerun()