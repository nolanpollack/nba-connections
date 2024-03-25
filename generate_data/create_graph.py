import pandas as pd
import networkx as nx
import pickle

data = pd.read_parquet('player_data.parquet')

G = nx.from_pandas_edgelist(data, source='id', target='teammate_id', edge_attr=['team_name', 'season'])

nx.set_node_attributes(G, pd.Series(data.full_name.values, index=data.id).to_dict(), 'full_name')

pickle.dump(G, open('player_graph.pickle', 'wb'))