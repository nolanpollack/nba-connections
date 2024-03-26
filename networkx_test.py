import networkx as nx
import pickle
from nba_api.stats.static import players
import json


class PlayerNode:
    def __init__(self, node_id, name, teams):
        self.id = node_id
        self.name = name
        self.teams = teams

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "teams": [team.to_dict() for team in self.teams]
        }


class TeamNode:
    def __init__(self, team_name, season, player_nodes):
        self.id = hash(team_name + season)
        self.team_name = team_name
        self.season = season
        self.players = player_nodes

    def to_dict(self):
        return {
            "id": self.id,
            "team_name": self.team_name,
            "season": self.season,
            "players": [player.to_dict() for player in self.players]
        }


def get_shortest_paths(player_name):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    player_graph = pickle.load(open('player_graph.pickle', 'rb'))
    shortest_paths = nx.single_source_shortest_path(player_graph, player_id)
    # Convert the paths to the desired JSON format
    json_data = []
    for node, path in shortest_paths.items():
        json_data = create_nested_structure(json_data, path, player_graph)

    json.dump(json_data, open('paths_wemby.json', 'w'))


def get_shortest_paths_teams(player_name):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    player_graph = pickle.load(open('player_graph.pickle', 'rb'))
    shortest_paths = nx.single_source_shortest_path(player_graph, player_id)
    # Convert the paths to the desired JSON format
    player_node = PlayerNode(player_id, player_graph.nodes[player_id]['full_name'], [])
    for node, path in shortest_paths.items():
        player_node = create_nested_structure_teams(player_node, path, player_graph)

    json.dump(player_node.to_dict(), open('paths_teams.json', 'w'))


def create_nested_structure(data, paths, player_graph):
    if len(paths) == 1:
        if 'full_name' in player_graph.nodes[paths[0]]:
            player_name = player_graph.nodes[paths[0]]['full_name']
            data.append({"id": paths[0], "children": [], "name": player_name})
        return data
    else:
        for child in data:
            if child["id"] == paths[0]:
                create_nested_structure(child["children"], paths[1:], player_graph)
                return data
        if 'full_name' in player_graph.nodes[paths[0]]:
            player_name = player_graph.nodes[paths[0]]['full_name']
            data.append(
                {"id": paths[0], "children": create_nested_structure([], paths[1:], player_graph), "name": player_name})
        return data


def create_nested_structure_teams(player_node: PlayerNode, paths, player_graph) -> PlayerNode:
    if len(paths) == 1:
        return player_node
    if len(paths) == 2:
        team_edge = player_graph.edges[paths[0], paths[1]]
        player = player_graph.nodes[paths[1]]

        if 'team_name' in team_edge and 'full_name' in player:
            team_id = hash(team_edge['team_name'] + team_edge['season'])
            for team in player_node.teams:
                if team.id == team_id:
                    team.players.append(PlayerNode(paths[1], player_graph.nodes[paths[1]]['full_name'], []))
                    return player_node

            # Team node does not exist, create it
            new_player_node = PlayerNode(paths[1], player['full_name'], [])
            node = TeamNode(team_edge['team_name'], team_edge['season'], [new_player_node])
            player_node.teams.append(node)
        return player_node
    else:
        team_edge = player_graph.edges[paths[0], paths[1]]
        player = player_graph.nodes[paths[1]]

        if 'team_name' in team_edge and 'full_name' in player:
            team_id = hash(team_edge['team_name'] + team_edge['season'])
            for team in player_node.teams:
                if team.id == team_id:
                    for team_player in team.players:
                        if team_player.id == paths[1]:
                            team_player = create_nested_structure_teams(team_player, paths[1:], player_graph)
                            return player_node

                    new_player_node = PlayerNode(paths[1], player['full_name'], [])
                    new_player_node = create_nested_structure_teams(new_player_node, paths[1:], player_graph)
                    team.players.append(new_player_node)
                    return player_node

            # Team node does not exist, create it
            new_player_node = PlayerNode(paths[1], player['full_name'], [])
            new_player_node = create_nested_structure_teams(new_player_node, paths[1:], player_graph)
            node = TeamNode(team_edge['team_name'], team_edge['season'], [new_player_node])
            player_node.teams.append(node)
        return player_node


get_shortest_paths_teams('LeBron James')