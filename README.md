# Web-App-Project

This project is a simple Web-App titled "We are the Champions". It is built using Streamlit, which is an open-source Python framework.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Assumptions](#assumption)
- [Contact](#contact)

## Installation

To install the project, perform a git clone and install the required packages. Lastly, run the streamlit application

```bash
git clone https://github.com/NotAnAddictz/Web-App-Project.git
cd Web-App-Project
pip install -r requirements.txt
streamlit run MainTable.py
```

## Usage
### MainTable

The MainTable page displays the list of available teams, with a multi-line input to add teams. Teams are sorted in the order of Score, Goals, Registration Date. The top 4 teams will be coloured Green to indicate that they will advance, while the rest will be coloured Red

Format of the input is as follows:

\<TeamName>\<RegistrationDate>\<GroupNumber>

### Matches
The Matches page displays the list of matches and the resulting winner, with a multi-line input to add matches. If both scores are even, the Result will be computed as a 'Draw'.

Format of the input is as follows:

\<Team1Name>\<Team2Name>\<Team1Goals>\<Team2Goals>

### Logs
The Logs page tracks all user input and button clicks, as well as the Date Time 

### Search
The Search page enables the user to select an existing team and find all information and relevant matches to it.

## Features
### Data Type Verification
The app includes assertions and regex when parsing user input in order to verify the format of the data. If the format is invalid, the data will not be added in. Additional verification measures has been added, such as number of teams in a group, as well as preventing cross-team matches

### Auto Update
Due to streamlit's features, the Web Page will be refreshed after every user input. Thus, the displayed tables will be updated automatically.

### Dynamic Updating (Matches)
Using streamlit's ```data_editor```, we are able to allow dynamic updating of the dataframe. Simply update the relevant columns and press the ```Update``` button.

## Assumptions
Due to the flexible instructions given, there are a few assumptions that I have made regarding the logic of the project.
### 1. Deleting teams == deleting matches involved
### 2. Only 2 groups are available at one time
### 3. Registration Date must be in format %dd/%mm

## Contact:
If there are any issues with the code, do contact me at kwayyishen@gmail.com