import networkx as nx
import pickle
from nba_api.stats.static import players
import json

player_id = players.find_players_by_full_name('Victor Wembanyama')[0]['id']

player_graph = pickle.load(open('player_graph.pickle', 'rb'))



paths = nx.single_source_shortest_path(player_graph, player_id)

def create_nested_structure(data, paths):
    if len(paths) == 1:
        if 'full_name' in player_graph.nodes[paths[0]]:
            player_name = player_graph.nodes[paths[0]]['full_name']
            data.append({"id": paths[0], "children": [], "name": player_name})
        return data
    else:
        for child in data:
            if child["id"] == paths[0]:
                create_nested_structure(child["children"], paths[1:])
                return data
        if 'full_name' in player_graph.nodes[paths[0]]:
            player_name = player_graph.nodes[paths[0]]['full_name']
            data.append({"id": paths[0], "children": create_nested_structure([], paths[1:]), "name": player_name})
        return data


# Convert the paths to the desired JSON format
json_data = []
for node, path in paths.items():
    # node_data = {"id": node, "children": []}
    if len(path) > 2:
        pass
    json_data = create_nested_structure(json_data, path)



json.dump(json_data, open('paths_wemby.json', 'w'))