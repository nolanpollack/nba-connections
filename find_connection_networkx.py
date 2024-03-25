import networkx as nx
from nba_api.stats.static import players
from response import Response


def find_connection(source, target, graph):
    if source is None or target is None:
        return Response(400, {"Content-Type": "application/json"}, 'Please provide both p1 and p2 parameters')

    source_player, target_player = get_players(source, target)

    if len(source_player) == 0:
        return Response(400, {"Content-Type": "application/json"}, 'Player {} not found'.format(source))
    if len(target) == 0:
        return Response(400, {"Content-Type": "application/json"}, 'Player {} not found'.format(target))

    source_id = source_player[0]['id']
    target_id = target_player[0]['id']

    path = nx.shortest_path(graph, source=source_id, target=target_id)

    found_path = []
    for i in range(len(path) - 1):
        # Print path edges with team and season
        player_name = graph.nodes[path[i + 1]]['full_name']
        team = graph.edges[path[i], path[i + 1]]['team_name']
        season = graph.edges[path[i], path[i + 1]]['season']
        found_path += [(player_name, team, season)]
    return Response(200, {"Content-Type": "application/json"}, found_path)


def get_players(p1, p2):
    # Replace + with space
    p1 = p1.replace('+', ' ')
    p2 = p2.replace('+', ' ')

    player1 = players.find_players_by_full_name(p1)
    player2 = players.find_players_by_full_name(p2)
    return player1, player2
