from typing import List,Tuple
import json
import pandas as pd
import numpy as np


def addTeams(teams: str)-> bool:
    teamList = teams.split('\n')
    tempdf = pd.DataFrame()
    for team in teamList:
        teamStats = team.strip().split(" ")
        if len(teamStats) == 3:
            team = pd.Series(teamStats[0],teamStats[1],int(teamStats[2]),0,0,0,0,0,0,0)
        else:
            print("Error, too many attributes listed")
            return False
    return True

def addResults(scores: str)-> bool:
    scoreList = scores.split('\n')
    for score in scoreList:
        scoreStats = score.strip().split(" ")
        assert len(scoreStats) == 4, "Too Many attributes"
        winner = scoreStats[0] if scoreStats[2] > scoreStats[3] else scoreStats[1]
        score = json.dumps({'firstTeamName':scoreStats[0],'secondTeamName':scoreStats[1],'firstTeamScore': int(scoreStats[2]),'secondTeamScore': int(scoreStats[3]), 'winner': winner})
        print(score)

def highlight_rows(row_data: pd.Series):
  return ["background-color: green" for _ in row_data]

def styleDataFrame(df: pd.DataFrame)-> pd.DataFrame:
    firstFour = df.head(4)
    styled_df = firstFour.style.apply(highlight_rows)
    