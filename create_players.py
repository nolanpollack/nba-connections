import pandas as pd
from collections import deque
from nba_api.stats.library.data import players

rosters = pd.read_csv('rosters.csv', converters={'player_ids': lambda x: set(eval(x))})

player_data = []

for player in players:
    teammates = set()
    player_id = player[0]
    teams = rosters.loc[rosters['player_ids'].apply(lambda x: player_id in x)].to_dict('records')
    for team in teams:
        teammates_tuple = map(lambda x: (x, team['team_name'], team['season_id']), (team['player_ids'] - {player_id}))
        teammates.update(teammates_tuple)
    player_data.append({'id': player[0], 'full_name':player[3], 'teammates': teammates})

df = pd.DataFrame(player_data, columns=['id', 'full_name', 'teammates'])
df.to_csv('player_data_test.csv', index=False)