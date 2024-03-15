# -*- coding: utf-8 -*-
from find_connection import find_connection


def handler(event, context):
    # Your code goes here!
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": find_connection(event.get('p1'), event.get('p2'))

    }
