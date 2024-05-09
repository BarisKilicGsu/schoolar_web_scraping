import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_undirected_graph
import matplotlib.pyplot as plt
import pandas as pd
import json


# JSON dosyasını oku
with open("datas/co_authorship/co_authorship_main_graph.json", "r") as f:
    data = json.load(f)

# Graphı oluştur
G = nx.node_link_graph(data)

calculate_topologic_analiz_for_undirected_graph(G, 'co_authorship/co_authorship')

