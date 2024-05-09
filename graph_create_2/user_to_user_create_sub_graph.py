import networkx as nx
from common import find_sub_graph_with_louvain_communities
import json

# JSON dosyasını oku
with open("datas/user_to_user/user_to_user_main_graph.json", "r") as f:
    data = json.load(f)

# Graphı oluştur
G = nx.node_link_graph(data)

sup_graphs, modularity = find_sub_graph_with_louvain_communities(G,5)
print(modularity)
sub_graph_datas = []

for sup_graph in sup_graphs:
    if sup_graph.number_of_nodes() < 6:
        continue
    data = nx.node_link_data(sup_graph)   
    sub_graph_datas.append(data)

# JSON dosyasına kaydet
with open("datas/user_to_user/user_to_user_sub_graph.json", "w") as dosya:
    json.dump(sub_graph_datas, dosya)

print("JSON dosyası oluşturuldu")

    
