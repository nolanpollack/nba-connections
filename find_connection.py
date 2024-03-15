from collections import deque

from nba_api.stats.static import players

class Response:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_dict(self):
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body
        }

def find_connection(initial, target, player_data) -> Response:
    if initial is None or target is None:
        return Response(400, {"Content-Type": "application/json"}, 'Please provide both p1 and p2 parameters')

    visited = set()
    initial, target = get_players(initial, target)
    if len(initial) == 0:
        return Response(400, {"Content-Type": "application/json"}, 'Player {} not found'.format(initial))
    if len(target) == 0:
        return Response(400, {"Content-Type": "application/json"}, 'Player {} not found'.format(target))

    initial = initial[0]
    target = target[0]

    queue = deque([(initial['id'], [])])

    return start_search(target['id'], queue, visited, player_data)


def get_players(p1, p2):
    # Replace + with space
    p1 = p1.replace('+', ' ')
    p2 = p2.replace('+', ' ')

    player1 = players.find_players_by_full_name(p1)
    player2 = players.find_players_by_full_name(p2)
    return player1, player2


def start_search(target_id, queue, visited, player_data) -> Response:
    while queue:
        player_id, path = queue.popleft()
        found_path = handle_player(target_id, player_id, path, queue, visited, player_data)
        if found_path is not None:
            return Response(200, {"Content-Type": "application/json"}, found_path)
    else:
        return Response(200, {"Content-Type": "application/json"}, 'No connection found')


def handle_player(target_id, player_id, path, queue, visited, player_data):
    # Check if player has been visited
    if player_id in visited:
        return
    visited.add(player_id)

    # Get teammates of player
    teammates = player_data.loc[player_data.index == player_id]
    if teammates.size == 0:
        return

    for teammate in teammates.itertuples():
        formatted_path = check_teammate(teammate, target_id, path, queue, visited, player_data)
        if formatted_path is not None:
            return formatted_path


# Check if teammate is the target player. If so, return the path. Else, add the teammate to the queue
def check_teammate(teammate, target_id, path, queue, visited, player_data):
    teammate_id = teammate.teammate_id
    if teammate_id in visited:
        return

    new_path = path + [(teammate_id, teammate.team_name, teammate.season)]
    if teammate_id == target_id:
        return get_formatted_path(new_path, player_data)

    queue.append((teammate_id, new_path))


def get_formatted_path(unformatted_path, player_data):
    formatted_path = []
    for player in unformatted_path:
        player_name = player_data.loc[player_data.index == player[0], 'full_name'].iloc[0]
        formatted_path.append({"team": player[1], "year": player[2], "player": player_name})
    return formatted_path
