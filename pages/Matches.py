import functions
import streamlit as st
import pandas as pd

st.title("Matches")

try: 
    matches = pd.read_csv("scoreList.csv",index_col = 0)
except:
    matches = pd.DataFrame(columns=['Team 1','Team 2','Team 1 Goals', 'Team 2 Goals'])
    matches.to_csv("scoreList.csv")

editedDF = st.data_editor(matches,width=1000)
editedDF.to_csv("scoreList.csv")

newTeams= st.text_area(label = "Add Teams",placeholder="First Team, Second Team, First Team Goals, Second Team Goals")
if newTeams:
    functions.addTeams(newTeams)