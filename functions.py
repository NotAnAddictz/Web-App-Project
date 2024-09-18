from typing import List
import pandas as pd
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
    index = 0
    newTeams = teams
    for index,team in enumerate(teamList):
        verified = verifyTeams(team,newTeams)
        if verified == True:
            teamStats = team.strip().split(" ")
            index +=1
            newSeries = pd.Series({"Position":len(teams),"TeamName":teamStats[0],"RegistrationDate":teamStats[1],"GroupNo":int(teamStats[2])})
            newTeams = pd.concat([newTeams,newSeries.to_frame().T],ignore_index=True)
        else:
            return (index,verified)
    return (-1,newTeams)


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

# Iterate through every match and update the scores accordingly
def updateScores(matches: pd.DataFrame, teams: pd.DataFrame)->pd.DataFrame:
    if len(matches) == 0:
        return teams
    else:
        colToUpdate = ['GamesPlayed','Goals','Wins','Draw','Loss','Score']
        for index,team in enumerate(teams['TeamName']):
            relevantRows = matches.loc[(matches['Team 1'] == team) | (matches['Team 2'] == team)]
            # GamesPlayed, Goals, Win, Draw, Losses, Score
            teamStats = [0,0,0,0,0,0]
            for row in relevantRows.index.tolist():
                teamStats[0]+=1
                teamStats[1]+=int(relevantRows.at[row,'Team 1 Goal'] if relevantRows.at[row,'Team 1'] == team else relevantRows.at[row,'Team 2 Goal'])
                if relevantRows.at[row,'Result'] == team:
                    teamStats[2]+=1
                elif relevantRows.at[row,'Result'] == 'Draw':
                    teamStats[3] +=1
                else:
                    teamStats[4] += 1
                teamStats[5] = teamStats[2]*3 + teamStats[3]
            teams.loc[index,colToUpdate] = pd.Series(teamStats,index=colToUpdate)
    return teams

def sortTeams(teams: pd.DataFrame)-> pd.DataFrame:
    teams['RegistrationDate'] = pd.to_datetime(teams['RegistrationDate'], format='%d/%m')
    teams['RegistrationDate'] = teams['RegistrationDate'].dt.date
    teams = teams.sort_values(by=["Score",'Goals','RegistrationDate'],ascending=[False,False,True])
    return teams
#================================================================================================================

# Helper Methods

def getResult(row)->str:
    if int(row['Team 1 Goal']) == int(row['Team 2 Goal']):
        return "Draw"
    elif int(row['Team 1 Goal']) > int(row['Team 2 Goal']):
        return row["Team 1"]
    else:
        return row['Team 2']
    
            
def remove(filePath: str)->bool | str:
    try:
        os.remove(filePath)
        return True 
    except Exception as e:
        return e
    