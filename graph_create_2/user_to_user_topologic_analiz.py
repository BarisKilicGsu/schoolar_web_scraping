import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph
import json

# JSON dosyasını oku
with open("datas/user_to_user/user_to_user_main_graph.json", "r") as f:
    data = json.load(f)

# Graphı oluştur
G = nx.node_link_graph(data)


calculate_topologic_analiz_for_directed_graph(G, 'user_to_user/user_to_user')

