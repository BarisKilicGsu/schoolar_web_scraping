import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph

import json


# JSON dosyasını oku
with open("datas/article_to_article/article_to_article_main_graph.json", "r") as f:
    data = json.load(f)


for each_data in data["graphs"]:
    # Graphı oluştur
    G = nx.node_link_graph(each_data)

    if G.number_of_nodes() < 200:
        continue

    calculate_topologic_analiz_for_directed_graph(G, 'article_to_article/article_to_article')


