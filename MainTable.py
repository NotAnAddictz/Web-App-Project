import streamlit as st
import pandas as pd
import functions
import logging

TEAMLIST = 'teams.xlsx'
LOGFILE = "logs.txt"
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(LOGFILE)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  
    logger.addHandler(file_handler) 

if 'teams' not in st.session_state or 'matches' not in st.session_state:
    teams,matches = functions.readFiles()
    st.session_state['teams'] = teams
    st.session_state['matches'] = matches

matches = st.session_state['matches']
teams = st.session_state['teams']
teams = teams.fillna(0)
st.set_page_config(page_title="We are the Champions", page_icon=None, layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>We are the Champions</h1>", unsafe_allow_html=True)

updatedTeams = []
if len(teams) != 0:
 
    groupList = teams['GroupNo'].unique()
    for x in groupList:
        group = teams[teams['GroupNo'] == x].reset_index(drop=True)
        group = functions.parseTeams(group)
        updatedTeams.append(group)

if len(updatedTeams) == 2:
    col1,col2 = st.columns([3,3],gap='medium')
    with col1:
        st.header(f'Group {groupList[0]}')
        st.table(updatedTeams[0])

    with col2:
        st.header(f'Group {groupList[1]}')
        st.table(updatedTeams[1])
elif len(updatedTeams) == 1:
    st.header(f'Group {groupList[0]}')
    st.table(updatedTeams[0])
else:
    st.header("No Teams Registered")

# Add Teams text_area and button
col1,col2 = st.columns(2)
with col1:
    newTeams= st.text_area(label = "Add Teams",placeholder="TeamName, Date of Registration, Group Number")
    addTeams = st.button("Add Teams")
if addTeams:
    index,teams = functions.addTeams(newTeams,teams)
    if index == -1:
        teams = teams.fillna(0)
        st.session_state['teams'] = teams
        functions.save('teams',teams)
        logger.info(f"Add Teams: {newTeams.replace("\n",",")}")
        st.rerun()
    else:
        st.toast(f"Error in line {index}: {teams}")

with col2:
    lessTeams = st.text_area(label = "Remove Teams",placeholder="TeamName")
    removeTeams= st.button("Remove Teams")
    removeAll = st.button("Clear All")

if removeTeams:
    lessTeams,matches = functions.removeTeams(lessTeams.strip(),teams,matches)
    if type(lessTeams) == pd.DataFrame:
        teams = lessTeams
        st.session_state['teams'] = teams
        st.session_state['matches'] = matches
        functions.save('teams',teams)
        functions.save('matches',matches)
        st.rerun()
    else:
        st.toast(lessTeams)

if removeAll:
    functions.remove('teams')
    functions.remove('matches')
    del st.session_state['matches']
    del st.session_state['teams']
    logger.info("Removed All Teams and Matches")
    st.rerun()