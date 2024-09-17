from typing import List
import json
import pandas as pd
import numpy as np
import re
import os

# Verification Methods:
#=========================================================================================================
def verifyTeams(teamInput: str,teams: pd.DataFrame) -> bool | str:
    temp = teamInput.strip().split(" ")
    pattern = "^(0[1-9]|[1-2]\\d|3[0-1])\\/(0[1-9]|1[0-2])$"
    try:
    # Checking if only the 3 fields are present
        assert len(temp) == 3, "Invalid number of Fields"
        assert str(temp[0]) not in teams['TeamName'].unique(), "Team name already in use"
        assert re.match(pattern,temp[1]),"Invalid Date"    
        assert int(temp[2]) not in teams['GroupNo'].unique(), "Group Number already in use"
        return True
    except ValueError as e:
        return "Invalid Type for Group Number"
    except Exception as e:
        return e

def verifyResults(results: str,matches: pd.DataFrame,teams: pd.DataFrame)-> bool | str:
    result = results.strip().split(" ")
    try:
        assert len(result) == 4, "Invalid number of fields"
        assert str(result[0]) in teams['TeamName'].unique(),"First Team not found"
        assert str(result[1]) in teams['TeamName'].unique(),"Second Team not found"
        assert str(result[0]) != str(result[1]),"A team can't play against itself!"
        assert int(result[2])
        assert int(result[3])
        return True
    except ValueError as e:
        return "Invalid Scores"
    except Exception as e:
        return e

def verifyTable(matches: pd.DataFrame,teams:pd.DataFrame)->bool|str:
    for x in range(len(matches)):
        try:
            assert matches.at[x,'Team 1'] in teams['TeamName'].unique(),"First Team not found"
            assert matches.at[x,'Team 2'] in teams['TeamName'].unique(),"Second Team not found"
            assert matches.at[x,'Team 1'] != matches.at[x,'Team 2'],"A team can't play against itself!"
            assert int(matches.at[x,'Team 1 Goal'])
            assert int(matches.at[x,'Team 2 Goal'])
        except ValueError as e:
            return "Invalid Scores"
        except Exception as e:
            return e
    return True
#=======================================================================================================

def addTeams(teamsToAdd: str, teams: pd.DataFrame)-> tuple[int,pd.DataFrame] | tuple[int,str]:
    teamList = teamsToAdd.split('\n')
    tempList= []
    index = 0
    for index,team in enumerate(teamList):
        verified = verifyTeams(team,teams)
        if verified == True:
            teamStats = team.strip().split(" ")
            index +=1
            team = pd.Series([len(teams)+index,teamStats[0],teamStats[1],int(teamStats[2])],index=['Position','TeamName','RegistrationDate','GroupNo'])
            tempList.append(team)
        else:
            return (index,verified)
    if len(tempList) > 0:
        newDF = pd.DataFrame(tempList)
        teams = pd.concat([teams,newDF],ignore_index=True)
    return (-1,teams)


def addResults(scores: str,matches: pd.DataFrame,teams: pd.DataFrame)-> pd.DataFrame:
    scoreList = scores.split('\n')
    tempList = []
    logList = []
    for index,score in enumerate(scoreList):
        verified = verifyResults(score,matches,teams)
        if verified == True:
            scoreStats = score.strip().split(" ")
            scores = pd.Series(scoreStats+[0],index=['Team 1','Team 2','Team 1 Goal','Team 2 Goal','Result'])
            tempList.append(scores)
        else:
            return index,verified
    if len(tempList) > 0:
        newDF = pd.DataFrame(tempList)
        matches = pd.concat([matches,newDF],ignore_index=True)
    return (-1,matches)

#================================================================================================================

# Helper Methods

def getResult(row)->str:
    if row['Team 1 Goal'] == row['Team 2 Goal']:
        return "Draw"
    elif row['Team 1 Goal'] > row['Team 2 Goal']:
        return row["Team 1"]
    else:
        return row['Team 2']
    
# Iterate through every match and update the scores accordingly
def updateScores(matches: pd.DataFrame, teams: pd.DataFrame)->pd.DataFrame:
    if len(matches) == 0:
        return teams
    else:
        teamList = dict(pd.unique(matches['Team 1','Team 2'].values()))
        print(teamList)
        for x in range(len(matches)): 
            pass
            
def remove(filePath: str)->bool | str:
    try:
        os.remove(filePath)
        return True 
    except Exception as e:
        return e
    