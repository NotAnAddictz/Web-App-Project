import streamlit as st
import pandas as pd
import functions

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
# Sanity chekc for presence of Data Files
try: 
    teams = pd.read_csv("teams.csv",header=0)
except:
    teams = pd.DataFrame(columns=['Position','TeamName','RegistrationDate','GroupNumber','Score','GamesPlayed','Wins','Draw','Loss','GoalsScored','GoalsAgainst'])
    teams.to_csv("teams.csv")


st.title("We are the Champions")

# Table Display
teams = teams.filter(items=['Position','TeamName','Score','Wins','Draw','Loss']).set_index('Position')
st.header("League Table")

styled_df = teams.style.apply(lambda x: ['background-color: green'] * len(x) if x.name <= 4 else ['background-color: red'] * len(x), axis=1)
st.dataframe(styled_df,width=1000)
newTeams= st.text_area(label = "Add Teams",placeholder="TeamName, Date of Registration, Group Number")
if newTeams:
    functions.addTeams(newTeams)