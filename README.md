<h1>Data analysis of NBA games using Python</h1>
<h2>Introduction</h2>
<p>I am an nba fan. Every goal in the game, steals or reverses the buzzer ball can make you boil. 
In addition to watching the exciting game, I want to try to judge the combat effectiveness of each team 
and predict the outcome of a game by using the previous statistics of the NBA game.</p>
<h2>Built With<h2>
  <ul>
    <li>Python 3.7</li>
    <li>Sklearn 0.20.0</li>
    </ul>
 <h2>NBA game statistics gathering</h2>
    In this lab, I will use the statistics from Basketball Reference.com. In this website, you can see basic statistics of different players, teams, seasons and league games, such as scores, number of fouls, etc., the number of wins and so on. And we will use the data in the 2016-17 NBA Season Summary here.</p>
  <p>In all the tables summarized in 2016-17, we will use the following three data tables:
  <ul>
  <li>Team Per Game Stats</li>
    <li>Opponent Per Game Stats</li>
    <li>Miscellaneous Stats</li>
  </ul>
  I will use these three tables to assess the team's past combat effectiveness, as well as the game data for each of the 2015-2016 NBA regular season and in the 2015-16 NBA Schedule and Results. Elo score (explained in the experimental section that follows). Follow the time from the regular season to the playoffs in Basketball Reference.com. Listed the matches for each game from October 2015 to April 2016.
  </p>
 <h2>Data Analysis</h2>
  After obtaining the data, I will use each team's past game situation and Elo rating to determine the winning probability of each team. In evaluating the past matches of each team, I will use the data from the three tables of Team Per Game Stats, Opponent Per Game Stats and Miscellaneous Stats (hereafter referred to as T, O and M tables) as representative of the game. The characteristics of a team's game. I will eventually achieve each game and predict which team will win in the game, but it will not give an absolute victory or defeat, but the probability of winning the team. So I will build a feature vector that represents the game. The statistics of the previous match statistics (T, O and M tables) of the two teams and the respective Elo ranks of the two teams.
<h2>Model training and prediction based on data</h2>
In this lab environment, I will use python's pandas, numpy, scipy and sklearn libraries.
<h2>Code construct</h2>
<h3>Insert experimental related modules</h3>
<p>import pandas as pd<br />
import math<br />
import csv<br />
import numpy as np<br />
from sklearn import linear_model<br />
</p>
<h3>Initialize data at the very beginning, read data from T, O, and M tables, and remove some extraneous data</h3>
<p>
    pruneM = M_stat.drop(['Rk', 'Arena'],axis = 1)<br />
    pruneO = O_stat.drop(['Rk','G','MP'],axis = 1)<br />
    pruneT = T_stat.drop(['Rk','G','MP'],axis = 1)<br />
    mergeMO = pd.merge(pruneM, pruneO, how = 'left', on = 'Team')<br />
    newstat = pd.merge(mergeMO, pruneT,  how = 'left', on = 'Team')<br />
    return newstat.set_index('Team', drop = True, append = False)<br />
</p>
<h3>Get the Elo Score rating function for each team, and Define the Elo grade function for each team</h3>
<p>assign it to the initial base_elo value when there is no rating at the beginning.<br />
def GetElo(team):<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    try:<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp        return team_elos[team]<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    except:<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp        team_elos[team] = init_elo<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   return team_elos[team]<br />
def CalcElo(winteam, loseteam):<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    R1 = GetElo(winteam)<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   R2 = GetElo(loseteam)<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    E1 = 1/(1 + math.pow(10,(R2 - R1)/400))<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    E2 = 1/(1 + math.pow(10,(R1 - R2)/400)) <br />  
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    if R1>=2400:K=16<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    elif R1<=2100:K=32<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    else: K=24<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    R1new = round(R1 + K*(1 - E1))<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp    R2new = round(R2 + K*(0 - E2))<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   return R1new, R2new
</p>
<h3>Based on our initial good statistics and the Elo score calculation results of each team, we will establish a data set corresponding to each game in the 2015~2016 regular season (in the home and away games, we think the home team is more advantageous). Therefore, the home team will be given a corresponding rating of 100)</h3>
<p>
  def GenerateTrainData(stat, trainresult):<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbspX = []<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbspy = []<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp  for index, rows in trainresult.iterrows():<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp        winteam = rows['WTeam']<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp        loseteam = rows['LTeam']<br />
   &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp       winelo = GetElo(winteam)<br />
  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp        loseelo = GetElo(loseteam)<br />
</p>
  
