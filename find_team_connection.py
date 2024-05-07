import networkx as nx
from nba_api.stats.static import players
from response import Response
from get_team_graph import get_shortest_paths_teams


def find_connection(player_name):
    if player_name is None:
        return Response(400, {"Content-Type": "application/json"}, 'Please provide player parameter')

    player = get_player(player_name)

    if len(player) == 0:
        return Response(400, {"Content-Type": "application/json"}, 'Player {} not found'.format(player))

    player_id = player[0]['id']

    node = get_shortest_paths_teams(player_id)

    return Response(200, {"Content-Type": "application/json"}, node.to_dict())


def get_player(player_name):
    # Replace + with space
    player_name = player_name.replace('+', ' ')

    player = players.find_players_by_full_name(player_name)
    return player
