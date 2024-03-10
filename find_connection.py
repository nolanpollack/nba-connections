from nba_api.stats.static import players
import pandas as pd
import ast

first_player = 'Trae Young'
second_player = 'Gene Berce'

rosters = pd.read_csv('rosters.csv')

# Get player ids
player1 = players.find_players_by_full_name(first_player)[0]
player2 = players.find_players_by_full_name(second_player)[0]

visited = set()
visited_teams = set()
queue = [(player1['id'], [])]

while queue:
    player_id, path = queue.pop(0)
    if player_id in visited:
        continue
    visited.add(player_id)
    teams = rosters[rosters['player_ids'].apply(lambda x: str(player_id) in x)]

    for index, team in teams.iterrows():
        team_tuple = (team['team_id'], team['season_id'])
        if team_tuple not in visited_teams:
            visited_teams.add(team_tuple)
            for pid in ast.literal_eval(team['player_ids']):
                queue.append((pid, path + [(team['team_name'], team['season_id'], players.find_player_by_id(pid)['full_name'])]))
    if player_id == player2['id']:
        print(path)
        break
else:
    print('No connection found')