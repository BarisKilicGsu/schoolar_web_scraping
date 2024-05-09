import networkx as nx
from common import create_centrality
import json

# JSON dosyasını oku
with open("datas/user_to_user/user_to_user_sub_graph.json", "r") as f:
    data = json.load(f)

all_data = []

for sub_data in data:
    G = nx.node_link_graph(sub_data)
    centrality_data = create_centrality(G)
    all_data.append({"graph":sub_data, "centrality_data":centrality_data})


# JSON dosyasına kaydet
with open("datas/user_to_user/user_to_user_centrality.json", "w") as dosya:
    json.dump(all_data, dosya)

print("JSON dosyası oluşturuldu")

    
