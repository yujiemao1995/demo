# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 16:19:16 2017

@author: dc
"""

import pandas as pd 
import math
import numpy as np
from sklearn import linear_model
import csv

init_elo = 1600
team_elos = {}
#trainteamstat = {}

folder = 'data'

def PruneData(M_stat, O_stat, T_stat):
    #Pruning the data of many teams that were originally read into a team index
    #Arranged feature data
    
    #Discard statistics that are not related to team strength
    pruneM = M_stat.drop(['Rk', 'Arena'],axis = 1)
    pruneO = O_stat.drop(['Rk','G','MP'],axis = 1)
    pruneT = T_stat.drop(['Rk','G','MP'],axis = 1)
    
    #Combine multiple data into one data via the same index:team
    mergeMO = pd.merge(pruneM, pruneO, how = 'left', on = 'Team')
    newstat = pd.merge(mergeMO, pruneT,  how = 'left', on = 'Team')
    
    #Return the team as index data
    return newstat.set_index('Team', drop = True, append = False)

def GetElo(team):
    #
    try:
        return team_elos[team]
    except:
        team_elos[team] = init_elo
    return team_elos[team]


def CalcElo(winteam, loseteam):
    # Winteam, loseteam input should be a string
    
    # Give the current two teams' elo scores
    R1 = GetElo(winteam)
    R2 = GetElo(loseteam)
    
    # Calculate the grade points after the game, refer to the elo formula
    E1 = 1/(1 + math.pow(10,(R2 - R1)/400))
    E2 = 1/(1 + math.pow(10,(R1 - R2)/400))
    
    if R1>=2400:
        K=16
    elif R1<=2100:
        K=32
    else:
        K=24
        
    R1new = round(R1 + K*(1 - E1))
    R2new = round(R2 + K*(0 - E2))
    return R1new, R2new

def GenerateTrainData(stat, trainresult):
    #Construct the input as [[team1 feature, team2 feature],...[]...]
    X = []
    y = []
    
    for index, rows in trainresult.iterrows():
        
        winteam = rows['WTeam']
        loseteam = rows['LTeam']
        
        #Get the initial elo value of each team
        winelo = GetElo(winteam)
        loseelo = GetElo(loseteam)
        
        # Add 100 elo to the Home_team
        if rows['WLoc'] == 'H':
            winelo = winelo+100
        else:
            loseelo = loseelo+100
        
        # Use elo as the first eigenvalue for each team
        fea_win = [winelo]
        fea_lose = [loseelo]
        
        # Add statistics for each team we get from basketball reference.com
        for key, value in stat.loc[winteam].iteritems():
            fea_win.append(value)
        for key, value in stat.loc[loseteam].iteritems():
            fea_lose.append(value)
        
        
        # Randomly assign the eigenvalues ​​of the two teams to the left and right sides of each game data.
        # assign the corresponding 0/1 to the y value
        if np.random.random() > 0.5:
            X.append(fea_win+fea_lose)
            y.append(0)
        else:
            X.append(fea_lose+fea_win)
            y.append(1)
            
        # update team elo score
        win_new_score, lose_new_score = CalcElo(winteam, loseteam)
        team_elos[winteam] = win_new_score
        team_elos[loseteam] = lose_new_score
        
    #return np.nan_to_num(X),y
    return np.nan_to_num(X),y
        
def GeneratePredictData(stat,info):
    
    X=[]
    
    #Traverse all the data to be predicted and transform the data into feature forms
    for index, rows in stat.iterrows():
        
        #elo as the first feature
        #team2 is Home_team, add extra 100 score
        team1 = rows['Vteam']
        team2 = rows['Hteam']
        
        elo_team1 = GetElo(team1)
        elo_team2 = GetElo(team2)
        
        fea1 = [elo_team1]
        fea2 = [elo_team2+100]
        
        #Team statistics as a residual feature
        for key, value in info.loc[team1].iteritems():
            fea1.append(value)
        
        for key, value in info.loc[team2].iteritems():
            fea2.append(value)
        
        #Two team feature stitching
        X.append(fea1 + fea2)
    
    #nan_to_num has two functions: 1 convert the list to array,
    #                              2. remove the non-number in X, and ensure that the trainer can't read the problem.
    return np.nan_to_num(X)
        
        
        
if __name__ == '__main__':
    
    M_stat = pd.read_csv(folder + '/15-16Miscellaneous_Stat.csv')
    O_stat = pd.read_csv(folder + '/15-16Opponent_Per_Game_Stat.csv')
    T_stat = pd.read_csv(folder + '/15-16Team_Per_Game_Stat.csv')
    team_result = pd.read_csv(folder + '/2015-2016_result.csv')
    
    teamstat = PruneData(M_stat, O_stat, T_stat)
    #'''Temporarily save data'''
    #teamstat.to_csv(folder + '/Train_data.csv')
    X,y = GenerateTrainData(teamstat, team_result)
    
    limodel = linear_model.LogisticRegression()
    limodel.fit(X,y)
    
    #'''predict'''
    pre_data = pd.read_csv(folder + '/16-17Schedule.csv')
    pre_X = GeneratePredictData(pre_data, teamstat)
    pre_y = limodel.predict_proba(pre_X)
    
    #''' display the results'''
    predictlist = []
    for index, rows in pre_data.iterrows():
        reslt = [rows['Vteam'], pre_y[index][0], rows['Hteam'], pre_y[index][1]]
        predictlist.append(reslt)
    print(predictlist)    
    
    #'''Predict result preservation'''
    with open(folder+'/prediction of 2016-2017.csv', 'w',newline='') as f:
        writers = csv.writer(f)
        writers.writerow(['Visit Team', 'corresponding probability of winning', 'Home Team', 'corresponding probability of winning'])
        writers.writerows(predictlist)
