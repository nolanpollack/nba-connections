import pandas
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster

df = pd.read_csv('../rosters.csv')

rows = []

team_items = teams.get_teams()
for team in team_items:
    for year in list(range(team['year_founded'], 2024)):
        season = str(year) + '-' + str(year + 1)[2:]
        team_id = team['id']
        team_name = team['full_name']
        if df[(df['team_id'] == team_id) & (df['season_id'] == season)].shape[0] > 0:
            continue
        pass
        try:
            players_on_team = commonteamroster.CommonTeamRoster(team_id=team_id, season=season).get_normalized_dict()
        except:
            break
        player_ids = [player['PLAYER_ID'] for player in players_on_team['CommonTeamRoster']]
        player_names = [player['PLAYER'] for player in players_on_team['CommonTeamRoster']]
        rows.append({'team_id': team_id,
                     'season_id': season,
                     'player_ids': player_ids,
                     'team_name': team_name,
                     'player_name': player_names})
    else:
        continue
    break

new_df = pandas.DataFrame(rows, columns=['team_id', 'season_id', 'player_ids', 'team_name', 'player_name'])
combined_df = pd.concat([df, new_df], ignore_index=True)
combined_df.to_csv('rosters.csv', index=False)