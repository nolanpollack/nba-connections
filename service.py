# -*- coding: utf-8 -*-
import pickle

from find_team_connection import find_connection as find_team_connection

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
    return find_team_connection(player_name).to_dict()
