import ast
from collections import deque

import pandas as pd
from flask import Flask
from nba_api.stats.static import players

app = Flask(__name__)

visited = set()
player_data = pd.read_csv('player_data_test.csv', converters={'teammates': lambda x: set(ast.literal_eval(x))},
                          index_col=0)


@app.route('/')
def find_connection(first_player, second_player):
    initial, target = get_players(first_player, second_player)
    queue = deque([(initial['id'], [])])

    return start_search(target['id'], queue)


def get_players(p1, p2):
    player1 = players.find_players_by_full_name(p1)[0]
    player2 = players.find_players_by_full_name(p2)[0]
    return player1, player2


def start_search(target_id, queue):
    while queue:
        player_id, path = queue.popleft()
        found_path = handle_player(target_id, player_id, path, queue)
        if found_path is not None:
            return found_path
    else:
        print('No connection found')


def handle_player(target_id, player_id, path, queue):
    # Check if player has been visited
    if player_id in visited:
        return
    visited.add(player_id)

    # Get teammates of player
    teammates = player_data.loc[player_data.index == player_id, 'teammates']
    if teammates.size == 0:
        return

    for teammate in teammates.iloc[0]:
        formatted_path = check_teammate(teammate, target_id, path, queue)
        if formatted_path is not None:
            return formatted_path


# Check if teammate is the target player. If so, return the path. Else, add the teammate to the queue
def check_teammate(teammate, target_id, path, queue):
    teammate_id = teammate[0]
    if teammate_id in visited:
        return

    new_path = path + [(teammate_id, teammate[1], teammate[2])]
    if teammate_id == target_id:
        return get_formatted_path(new_path)

    queue.append((teammate_id, new_path))


def get_formatted_path(unformatted_path):
    formatted_path = []
    for player in unformatted_path:
        player_name = player_data.loc[player_data.index == player[0], 'full_name'].iloc[0]
        formatted_path.append({"team": player[2], "year": player[1], "player": player_name})
    return formatted_path
