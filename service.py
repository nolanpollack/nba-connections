# -*- coding: utf-8 -*-
from find_connection import find_connection
import ast
import pandas as pd

player_data = None

def handler(event, context):
    global player_data
    if player_data is None:
        player_data = pd.read_csv('player_data.csv', converters={'teammates': lambda x: set(ast.literal_eval(x))},
                                  index_col=0)

    initial = event['queryStringParameters']['p1']
    target = event['queryStringParameters']['p2']

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": find_connection(initial, target, player_data)
    }
