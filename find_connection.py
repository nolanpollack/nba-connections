from collections import deque

from nba_api.stats.static import players

def find_connection(initial, target, player_data):
    if initial is None or target is None:
        return 'Please provide both first_player and second_player parameters'

    visited = set()
    initial, target = get_players(initial, target)
    if len(initial) == 0 or len(target) == 0:
        return 'Player not found'

    initial = initial[0]
    target = target[0]

    queue = deque([(initial['id'], [])])

    return start_search(target['id'], queue, visited, player_data)


def get_players(p1, p2):
    player1 = players.find_players_by_full_name(p1)
    player2 = players.find_players_by_full_name(p2)
    return player1, player2


def start_search(target_id, queue, visited, player_data):
    while queue:
        player_id, path = queue.popleft()
        found_path = handle_player(target_id, player_id, path, queue, visited, player_data)
        if found_path is not None:
            return found_path
    else:
        return 'No connection found'


def handle_player(target_id, player_id, path, queue, visited, player_data):
    # Check if player has been visited
    if player_id in visited:
        return
    visited.add(player_id)

    # Get teammates of player
    teammates = player_data.loc[player_data.index == player_id, 'teammates']
    if teammates.size == 0:
        return

    for teammate in teammates.iloc[0]:
        formatted_path = check_teammate(teammate, target_id, path, queue, visited, player_data)
        if formatted_path is not None:
            return formatted_path


# Check if teammate is the target player. If so, return the path. Else, add the teammate to the queue
def check_teammate(teammate, target_id, path, queue, visited, player_data):
    teammate_id = teammate[0]
    if teammate_id in visited:
        return

    new_path = path + [(teammate_id, teammate[1], teammate[2])]
    if teammate_id == target_id:
        return get_formatted_path(new_path, player_data)

    queue.append((teammate_id, new_path))


def get_formatted_path(unformatted_path, player_data):
    formatted_path = []
    for player in unformatted_path:
        player_name = player_data.loc[player_data.index == player[0], 'full_name'].iloc[0]
        formatted_path.append({"team": player[2], "year": player[1], "player": player_name})
    return formatted_path
