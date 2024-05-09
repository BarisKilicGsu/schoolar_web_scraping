import networkx as nx
import json

# JSON dosyasını oku
with open("datas/co_authorship/co_authorship_main_graph.json", "r") as f:
    data = json.load(f)

# Graphı oluştur
G = nx.node_link_graph(data)


communs = nx.community.louvain_communities(G, resolution=1 )
modularityy = nx.community.modularity(G=G, communities=communs)
print(f"resolution=1 için modularity değeri = {modularityy}")

communs = nx.community.louvain_communities(G, resolution=3 )
modularityy = nx.community.modularity(G=G, communities=communs)
print(f"resolution=3 için modularity değeri = {modularityy}")

communs = nx.community.louvain_communities(G, resolution=5 )
modularityy = nx.community.modularity(G=G, communities=communs)
print(f"resolution=5 için modularity değeri = {modularityy}")

communs = nx.community.louvain_communities(G, resolution=7 )
modularityy = nx.community.modularity(G=G, communities=communs)
print(f"resolution=7 için modularity değeri = {modularityy}")
