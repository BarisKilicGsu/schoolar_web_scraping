import networkx as nx
from common import find_sub_graph_with_louvain_communities
import json


# JSON dosyasını oku
with open("datas/article_to_article/article_to_article_main_graph.json", "r") as f:
    data = json.load(f)

sub_graph_datas = []

for each_data in data["graphs"]:

    # Graphı oluştur
    G = nx.node_link_graph(each_data)

    if G.number_of_nodes() < 6:
        continue
    elif G.number_of_nodes() < 300:
        sup_graphs, modularity = find_sub_graph_with_louvain_communities(G,1)
    else:
        sup_graphs, modularity = find_sub_graph_with_louvain_communities(G,5)
    print(modularity)
    for sup_graph in sup_graphs:
        datax = nx.node_link_data(sup_graph)   
        sub_graph_datas.append(datax)

# JSON dosyasına kaydet
with open("datas/article_to_article/article_to_article_sub_graph.json", "w") as dosya:
    json.dump(sub_graph_datas, dosya)

print("JSON dosyası oluşturuldu")


