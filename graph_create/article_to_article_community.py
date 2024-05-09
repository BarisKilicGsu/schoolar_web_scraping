from psycopg2 import sql
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph
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
    

print(len(edges))

sorted_lists = nx.weakly_connected_components(G)

all_dict = {}
j = 1
for each_list in sorted_lists:

    if len(each_list) < 10 :
        continue

    en_büyük_component = list(each_list)
    en_büyük_component_int = []
    for eleman in en_büyük_component:
        yeni_eleman = int(eleman)
        en_büyük_component_int.append(yeni_eleman)
    '''
    print(len(en_büyük_component))
    query = "SELECT alinti_yapan, alinti_yapılan FROM article_to_article_citations WHERE alinti_yapan IN %s AND alinti_yapılan IN %s;"

    cursor = conn.cursor()
    cursor.execute(query, (tuple(en_büyük_component_int), tuple(en_büyük_component_int)))
    # Sonuçları al
    newEdges = cursor.fetchall()
    conn.commit()
    '''
    newG = nx.DiGraph()
    lll = len(edges)
    iii = 0
    for edge in edges:
        print(f"{iii}/{lll}")
        iii += 1
        source, target = edge
        if source in en_büyük_component_int and target in en_büyük_component_int:
            newG.add_edge(str(source), str(target))
    
    print("len(sorted_communities)")

    communs = nx.community.louvain_communities(newG, resolution=5 ,seed=123)
    sorted_communities = sorted(communs, key=len, reverse=True)

    print(len(sorted_communities))

    comune_liste = [list(item) for item in sorted_communities]
    sonuc_dict = {}
    for i, eleman in enumerate(comune_liste, start=1):
        comun_record = {"size": len(eleman), "records":eleman}
        sonuc_dict[f"communiti_{i}"] =  comun_record

    all_dict[f"graph_{j}"] = {"communities": sonuc_dict, "size":len(sonuc_dict)}
    j += 1

# JSON dosyasına kaydet
with open("datas/article_to_article/article_to_article_communities.json", "w") as dosya:
    json.dump(all_dict, dosya)

print("JSON dosyası oluşturuldu: sonuc.json")

conn.close()
    
