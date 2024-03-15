# -*- coding: utf-8 -*-
from find_connection import find_connection
import ast
import pandas as pd
import time

player_data = None

def handler(event, context):
    global player_data
    starttime = time.time()
    if player_data is None:
        player_data = pd.read_parquet('player_data.parquet')

    print('Time to read data:', time.time() - starttime)

    initial = event['queryStringParameters']['p1']
    target = event['queryStringParameters']['p2']

    starttime = time.time()
    body = find_connection(initial, target, player_data)
    print('Time to find connection:', time.time() - starttime)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": body
    }
