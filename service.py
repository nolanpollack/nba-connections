# -*- coding: utf-8 -*-
from find_connection import find_connection
import pandas as pd

player_data = None

def handler(event, context):
    global player_data
    if player_data is None:
        player_data = pd.read_parquet('player_data.parquet')

    initial = event['queryStringParameters']['p1']
    target = event['queryStringParameters']['p2']

    return find_connection(initial, target, player_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": find_connection(initial, target, player_data)
    }
