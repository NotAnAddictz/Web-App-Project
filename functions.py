from typing import List
import json
import pandas as pd
import numpy as np
import re
# Verifies that each string input is correct, 
def verifyTeams(teamInput: str,teams: pd.DataFrame) -> bool | str:
    temp = teamInput.strip().split(" ")
    pattern = "^(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])$"
    try:
    # Checking if only the 3 fields are present
        assert len(temp) == 3, "Too many Fields"
        assert temp[0] not in teams['TeamName'].unique(), "Team name already in use"
        assert re.match(pattern,temp[1]),"Invalid Date"    
        assert int(temp[2]) not in teams['GroupNo'].unique(), "Group Number already in use"
        return True
    except ValueError as e:
        return "Invalid Type for Group Number"
    except Exception as e:
        return e

def verifyResults(results: str,teams: pd.DataFrame)-> bool | str:
    result = results.strip().split("")
    try:
        assert len(result) == 4, "Too many fields"
        assert result[0] in teams['TeamName'],"First Team not found"
        assert result[1] in teams['TeamName'],"Second Team not found"
        assert int(result[2])
        assert int(result[3])
        return True
    except ValueError as e:
        return "Invalid Scores"
    except Exception as e:
        return e


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

def addResults(scores: str,teams: pd.DataFrame)-> pd.DataFrame:
    scoreList = scores.split('\n')
    tempList = []
    for index,score in enumerate(scoreList):
        verified = verifyResults(score,teams)
        if verified == True:
            scoreStats = score.strip().split(" ")
            
