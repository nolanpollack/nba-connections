import ast
import time
from collections import deque

import pandas as pd
from nba_api.stats.static import players

# Constants
start = time.time()
first_player = 'Scoot Henderson'
second_player = 'Bill Russel'

visited = set()


def main():
    # Initialize variables
    player_data = pd.read_csv('player_data_test.csv', converters={'teammates': lambda x: set(ast.literal_eval(x))}, index_col=0)
    player1, player2 = get_player_ids(first_player, second_player)
    queue = deque([(player1['id'], [])])

    start_search(player_data, player2, queue)

def get_player_ids(p1, p2):
    player1 = players.find_players_by_full_name(p1)[0]
    player2 = players.find_players_by_full_name(p2)[0]
    return player1, player2


def start_search(player_data, player2, queue):
    while queue:
        player_id, path = queue.popleft()
        handle_player(player_data, player2, player_id, path, queue)
    else:
        print('No connection found')


def handle_player(player_data, player2, player_id, path, queue):
    if player_id in visited:
        return
    visited.add(player_id)
    teammates = player_data.loc[player_data.index == player_id, 'teammates']
    if teammates.size == 0:
        return
    for teammate in teammates.iloc[0]:
        teammate_id = teammate[0]
        if teammate_id in visited:
            continue
        # if player_name.size == 0:
        #     continue
        # player_name = player_name.iloc[0]
        # new_path = path + [player_name]
        new_path = path + [(teammate_id, teammate[1], teammate[2])]
        if teammate_id == player2['id']:
            for player in new_path:
                player_name = player_data.loc[player_data.index == player[0], 'full_name'].iloc[0]
                print(player_name, player[1], player[2])
            print("Players searched: ", len(visited))
            print("Time elapsed: ", time.time() - start)
            exit()
        queue.append((teammate_id, new_path))


main()
