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
  I will use these three tables to assess the team's past combat effectiveness, as well as the game data for each of the 2016-2017 NBA regular season and playoff games in the 2015-16 NBA Schedule and Results. Elo score (explained in the experimental section that follows). Follow the time from the regular season to the playoffs in Basketball Reference.com. Listed the matches for each game from October 2016 to June 2017.
  </p>
 <h2>Data Analysis</h2>
  After obtaining the data, I will use each team's past game situation and Elo rating to determine the winning probability of each team. In evaluating the past matches of each team, I will use the data from the three tables of Team Per Game Stats, Opponent Per Game Stats and Miscellaneous Stats (hereafter referred to as T, O and M tables) as representative of the game. The characteristics of a team's game. I will eventually achieve each game and predict which team will win in the game, but it will not give an absolute victory or defeat, but the probability of winning the team. So I will build a feature vector that represents the game. The statistics of the previous match statistics (T, O and M tables) of the two teams and the respective Elo ranks of the two teams.
<h2>Model training and prediction based on data</h2>
In this lab environment, I will use python's pandas, numpy, scipy and sklearn libraries.
  
