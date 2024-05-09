import networkx as nx
import json

# JSON dosyasını oku
with open("datas/user_to_user/user_to_user_main_graph.json", "r") as f:
    data = json.load(f)

# Graphı oluştur
G = nx.node_link_graph(data)

max_modularity = -1
best_seed = None

for i in range(10000):
    communs = nx.community.louvain_communities(G, resolution=5 ,seed=i)
    modularityy = nx.community.modularity(G=G, communities=communs)
    print(f"seed={i} modularity = {modularityy}")

    if modularityy > max_modularity:
        max_modularity = modularityy
        best_seed = i

    print(f"Best seed: {best_seed}, Max modularity: {max_modularity}")