# -*- coding: utf-8 -*-
from find_connection_networkx import find_connection
import pickle

player_graph = None

def handler(event, context):
    global player_graph
    if player_graph is None:
        player_graph = pickle.load(open('player_graph.pickle', 'rb'))

    initial = event['queryStringParameters']['p1']
    target = event['queryStringParameters']['p2']

    return find_connection(initial, target, player_graph).to_dict()
