import networkx as nx
import pandas as pd
import nba_api.stats.static.players as nba
import pickle

# G = nx.Graph()
#
# G.add_nodes_from(['Lebron James', 'Michael Jordan'])

# data = pd.read_parquet('player_data_new.parquet', )
#
# data = data.dropna(subset=['teammate_id'])
#
# G = nx.from_pandas_edgelist(data, source='full_name', target='teammate_id', edge_attr=['team_name', 'season'])
#
# pickle.dump(G, open('player_graph.pickle', 'wb'))

G = pickle.load(open('player_graph.pickle', 'rb'))

# Get path between players and print team and season

path = nx.shortest_path(G, source='Lebron James', target='Michael Jordan')

for i in range(len(path) - 1):
    G.
    print(f"{path[i]} -> {path[i + 1]}")

# for _, row in data.iterrows():
#     teammate = nba.find_player_by_id(row['teammate_id'])
#     if teammate is None:
#         continue
#     teammate_name = nba.find_player_by_id(row['teammate_id'])['full_name']
#
#     G.add_edge(row['full_name'], teammate_name, team_name=row['team_name'], season=row['season'])
#
# path = nx.shortest_path(G, source='Lebron James', target='Michael Jordan')
#
# for i in range(len(path) - 1):
#     print(f"{path[i]} -> {path[i + 1]}")
# pass