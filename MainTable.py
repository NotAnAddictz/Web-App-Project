import streamlit as st
import pandas as pd
import functions
# Sanity chekc for presence of Data Files
try: 
    teams = pd.read_excel("teams.xlsx",header=0)
except:
    teams = pd.DataFrame({'Position':pd.Series(dtype='int'),
                          'TeamName':pd.Series(dtype='str'),
                          'RegistrationDate':pd.Series(dtype='str'),
                          'GroupNo':pd.Series(dtype='int'),
                          'Score':pd.Series(dtype='int'),
                          'GamesPlayed':pd.Series(dtype='int'),
                          'Wins':pd.Series(dtype='int'),
                          'Draw':pd.Series(dtype='int'),
                          'Loss':pd.Series(dtype='int'),
                          })
    teams.to_excel("teams.xlsx",index=False)

teams = teams.fillna(int(0))
st.title("We are the Champions")
print(teams)
# Table Display
teamsToDisplay = teams.filter(items=['Position','TeamName','GroupNo','Score','Wins','Draw','Loss']).set_index('Position')
st.header("League Table")

styled_df = teamsToDisplay.style.apply(lambda x: ['background-color: green'] * len(x) if x.name <= 4 else ['background-color: red'] * len(x), axis=1)
st.dataframe(styled_df,width=1000)

# Add Teams text_area and button
newTeams= st.text_area(label = "Add Teams",placeholder="TeamName, Date of Registration, Group Number")
submitted = st.button("Add Teams")
if submitted:
    index,teams = functions.addTeams(newTeams,teams)
    if index == -1:
        teams.to_excel("teams.xlsx",index=False)
        st.rerun()
    else:
        st.toast(f"Error in line {index}: {teams}")
