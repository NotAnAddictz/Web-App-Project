import streamlit as st
import pandas as pd
import numpy as np
st.title("We are the Champions")

teams = pd.read_csv("teams.csv",index_col = 0)

toDisplay = ['Position','TeamName']
teams = teams.filter(items=['TeamName','Score','Wins','Draw','Loss'])
st.header("League Table")
st.table(teams)
