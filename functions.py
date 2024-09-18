from typing import List
import pandas as pd
import re
import os
MATCHLIST = 'scoreList.xlsx'
TEAMLIST = 'teams.xlsx'

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
        if len(teams['GroupNo'].unique()) == 2:
            assert int(temp[2]) in teams['GroupNo'].unique(), "Too many groups"
        if len(teams[teams['GroupNo'] == int(temp[2])]) == 6:
            raise Exception("Too many teams in the same group")
        return True
    except ValueError as e:
        return "Invalid Type for Group Number"
    except Exception as e:
        return e

def verifyResults(results: str,teams: pd.DataFrame)-> bool | str:
    result = results.strip().split(" ")
    try:
        assert len(result) == 4, "Invalid number of fields"
        assert str(result[0]) in teams['TeamName'].unique(),"First Team not found"
        assert str(result[1]) in teams['TeamName'].unique(),"Second Team not found"
        assert teams[teams['TeamName'] == str(result[0])]['GroupNo'].values[0] == teams[teams['TeamName'] == result[1]]['GroupNo'].values[0], "A team cant play against an opposite group!"
        result[2] = int(result[2])
        result[3] = int(result[3])
        return True
    except ValueError as e:
        return "Invalid Scores"
    except Exception as e:
        return e

def verifyTable(matches: pd.DataFrame,teams:pd.DataFrame)->bool|str:
    if len(matches) == 0:
        return "No Table Found"
    for x in range(len(matches)):
        try:
            assert matches.at[x,'Team 1'] in teams['TeamName'].unique(),"First Team not found"
            assert matches.at[x,'Team 2'] in teams['TeamName'].unique(),"Second Team not found"
            assert matches.at[x,'Team 1'] != matches.at[x,'Team 2'],"A team can't play against itself!"
            int(matches.at[x,'Team 1 Goal'])
            int(matches.at[x,'Team 2 Goal'])
        except ValueError as e:
            return "Invalid Scores"
        except Exception as e:
            return e
    return True

#=======================================================================================================
# Updating Tables

def parseTeams(group:pd.DataFrame)->pd.DataFrame:
    # Updating Scores
    group = sortTeams(group).reset_index(drop=True)
    group['Position'] = group.index + 1
    group = group.filter(items=['Position','TeamName','Score','Wins','Draw','Loss','Goals']).set_index('Position')
    group = group.style.apply(lambda x: ['background-color: rgb(0,155,0);color:rgb(255,255,255)'] * len(x) if x.name <= 4 else ['background-color: red;color:rgb(0,0,0)'] * len(x), axis=1).format(precision=0)

    return group
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

def removeTeams(teamsToRemove: str,teams: pd.DataFrame,matches: pd.DataFrame)-> tuple[pd.DataFrame | str] | tuple[str,str]:
    teamList = teamsToRemove.split('\n')
    originalTeams = teams['TeamName'].unique()
    for x in teamList:
        if x in originalTeams:
            teams = teams[teams['TeamName']!= x]
        else:
            return "Team not found!","Matches not found!",
        rowsToDrop = []
        for y in range(len(matches)):
            if matches.at[y,'Team 1'] == x or matches.at[y,'Team 2'] == x:
                rowsToDrop.append(y)
        matches=matches.drop(rowsToDrop).reset_index(drop=True)
    return teams,matches

def addResults(scores: str,matches: pd.DataFrame,teams: pd.DataFrame)-> pd.DataFrame:
    scoreList = scores.split('\n')
    tempList = []
    for index,score in enumerate(scoreList):
        verified = verifyResults(score,teams)
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
    save('teams',teams)
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
    
            
def remove(fileType: str)->bool | str:
    match fileType:
        case 'teams':
            os.remove(TEAMLIST)
            return True
        case 'matches':
            os.remove(MATCHLIST)
            return True
        case _:
            return "File already deleted"
def save(fileType: str, data: pd.DataFrame)->bool | str:
    match fileType:
        case 'teams':
            data.to_excel(TEAMLIST,index=False)
        case 'matches':
            data.to_excel(MATCHLIST,index=False)
            return True
        case _:
            return "File Error"
def callback(editedRows: pd.DataFrame)-> List:
    rows_to_delete = []

    for x in editedRows.index:
        if editedRows.at[x,'Delete?'] == True:
            rows_to_delete.append(x)
    
    return rows_to_delete

def readFiles()-> tuple[pd.DataFrame,pd.DataFrame]:
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
    return teams,matches