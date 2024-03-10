from nba_api.stats.endpoints import playercareerstats, commonteamroster
from nba_api.stats.static import players, teams
import json

first_player = 'LeBron James'
second_player = 'Michael Jordan'

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
    try:
        player_info = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict()
    except:
        continue
    team_ids = [(season['TEAM_ID'], season['SEASON_ID']) for season in player_info['SeasonTotalsRegularSeason']]
    for team in team_ids:
        if team[0] not in visited_teams:
            visited_teams.add(team)
            players_on_team = commonteamroster.CommonTeamRoster(team_id=team[0], season=team[1]).get_normalized_dict()
            player_ids = [player['PLAYER_ID'] for player in players_on_team['CommonTeamRoster']]
            for pid in player_ids:
                queue.append((pid, path + [(team[0], team[1], pid)]))
    if player_id == player2['id']:
        for item in path:
            team_name = teams.find_team_name_by_id(item[0])
            player_name = players.find_player_by_id(item[2])['full_name']
            print("Team: " + team_name + " Season: " + str(item[1]) + " Player: " + player_name)
        break