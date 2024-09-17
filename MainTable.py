import streamlit as st
import pandas as pd
import functions
import logging

TEAMLIST = 'teams.xlsx'
MATCHLIST = 'scoreList.xlsx'
LOGFILE = "logs.txt"
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(LOGFILE)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  
    logger.addHandler(file_handler) 

try:
    matches = pd.read_excel(MATCHLIST,header = 0)
except:
    matches = None
try: 
    teams = pd.read_excel(TEAMLIST,header=0)
except:
    teams = pd.DataFrame({'Position':pd.Series(dtype='int'),
                          'TeamName':pd.Series(dtype='str'),
                          'RegistrationDate':pd.Series(dtype='str'),
                          'GroupNo':pd.Series(dtype='int'),
                          'Score':pd.Series(dtype='int'),
                          'GamesPlayed':pd.Series(dtype='int'),
                          'Goals':pd.Series(dtype='int'),
                          'Wins':pd.Series(dtype='int'),
                          'Draw':pd.Series(dtype='int'),
                          'Loss':pd.Series(dtype='int'),
                          })
    teams.to_excel(TEAMLIST,index=False)

teams = teams.fillna(int(0))
st.title("We are the Champions")

# Updating Scores
teams = functions.sortTeams(functions.updateScores(matches,teams)).reset_index(drop=True)
teams['Position'] = teams.index + 1

# Table Display
teamsToDisplay = teams.filter(items=['Position','TeamName','GroupNo','Score','Wins','Draw','Loss','Goals']).set_index('Position')
st.header("League Table")

styled_df = teamsToDisplay.style.apply(lambda x: ['background-color: green'] * len(x) if x.name <= 4 else ['background-color: red'] * len(x), axis=1).format(precision=0)
st.table(styled_df)

# Add Teams text_area and button
newTeams= st.text_area(label = "Add Teams",placeholder="TeamName, Date of Registration, Group Number")
col1,col2 = st.columns([1,1])
with col1:
    submitted = st.button("Add Teams")
if submitted:
    index,teams = functions.addTeams(newTeams,teams)
    if index == -1:
        teams.to_excel("teams.xlsx",index=False)
        logger.info(f"Add Teams: {newTeams.replace("\n",",")}")
        st.rerun()
    else:
        st.toast(f"Error in line {index}: {teams}")

# Clearing all teams
with col2:
    removeAll = st.button("Clear All")
if removeAll:
    functions.remove(TEAMLIST)
    logger.info("Removed All Teams")
    st.rerun()