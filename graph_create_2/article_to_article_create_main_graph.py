from psycopg2 import sql
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query
import json

conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT alinti_yapan, alinti_yapılan 
FROM article_to_article_citations;
"""

edges = execute_sql_query(conn, query )

# Boş bir yönlü graf oluşturalım
G = nx.DiGraph()

# Kenarları ekleme
for edge in edges:
    source, target = edge
    G.add_edge(str(source), str(target))
    

sorted_lists = nx.weakly_connected_components(G)

all_data_list = []

for each_list in sorted_lists:
    
    if len(each_list) < 10 :
        continue
    
    en_büyük_component = list(each_list)
    en_büyük_component_int = []
    for eleman in en_büyük_component:
        yeni_eleman = int(eleman)
        en_büyük_component_int.append(yeni_eleman)

    newG = nx.DiGraph()
    lll = len(edges)
    iii = 0
    for edge in edges:
        print(f"{iii}/{lll}")
        iii += 1
        source, target = edge
        if source in en_büyük_component_int and target in en_büyük_component_int:
            newG.add_edge(str(source), str(target))

    data = nx.node_link_data(newG)      
    all_data_list.append(data)

all_dict = {"graphs": all_data_list}

with open("datas/article_to_article/article_to_article_main_graph.json", "w") as dosya:
    json.dump(all_dict, dosya)

conn.close()
    
