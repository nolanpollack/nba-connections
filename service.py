# -*- coding: utf-8 -*-
import pickle

from find_connection_networkx import find_connection
from get_team_graph import get_shortest_paths_teams

player_graph = None


def handler(event, context):
    global player_graph
    if player_graph is None:
        player_graph = pickle.load(open("player_graph.pickle", "rb"))

    # initial = event['queryStringParameters']['p1']
    # target = event['queryStringParameters']['p2']
    #
    # return find_connection(initial, target, player_graph).to_dict()
    player_name = event["queryStringParameters"]["player"]
    return get_shortest_paths_teams(player_name).to_dict()
