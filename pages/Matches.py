import functions
import streamlit as st
import pandas as pd

st.title("Matches")

try: 
    matches = pd.read_excel("scoreList.xlsx",index_col = 0)
except:
    matches = pd.DataFrame({"Team 1": pd.Series(dtype='str'),
                            "Team 2": pd.Series(dtype='str'),
                            "Team 1 Goal": pd.Series(dtype="int"),
                            "Team 2 Goal": pd.Series(dtype="int"),
                            "Result": pd.Series(dtype='str')
                            })
    matches.to_excel("scoreList.xlsx",index=False)

editedDF = st.data_editor(matches,width=1000)
editedDF.to_excel("scoreList.xlsx",index=False)

newTeams= st.text_area(label = "Add Teams",placeholder="First Team, Second Team, First Team Goals, Second Team Goals")
if newTeams:
    functions.addTeams(newTeams)