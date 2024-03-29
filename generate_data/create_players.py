import pandas as pd
from nba_api.stats.library.data import players

rosters = pd.read_csv('../rosters.csv')

rosters['player_ids'] = rosters['player_ids'].apply(lambda x: set(eval(x)) if x != '[]' and x[0] == '[' else set())

player_data = []

for player in players:
    teammates_id = set()
    player_id = player[0]
    teams = rosters.loc[rosters['player_ids'].apply(lambda x: player_id in x)].to_dict('records')
    for team in teams:
        teammates_id_tuple = map(lambda x: (x, team['team_name'], team['season_id']),
                                 (team['player_ids'] - {player_id}))
        teammates_id.update(teammates_id_tuple)
    player_data.append({'id': player[0], 'full_name': player[3], 'teammates': teammates_id})

df = pd.DataFrame(player_data, columns=['id', 'full_name', 'teammates'])

df = df[df['teammates'].apply(len) > 0]

df = df.explode('teammates')
df[['teammate_id', 'team_name', 'season']] = pd.DataFrame(df['teammates'].tolist(), index=df.index)
df.drop('teammates', axis=1, inplace=True)

df.dropna(inplace=True)

df.to_parquet('player_data_new.parquet')
