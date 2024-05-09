import networkx as nx
import json


file_name = "co_authorship"
# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_sub_graph.json", "r") as f:
    data = json.load(f)

i = 1
for sub_data in data:
    G = nx.node_link_graph(sub_data)
    nx.write_graphml(G, f"datas/{file_name}/graphml/graph_{i}.graphml")
    i+=1

# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_main_graph.json", "r") as f:
    data = json.load(f)

G = nx.node_link_graph(data)
nx.write_graphml(G, f"datas/{file_name}/graphml/graph_0.graphml")


file_name = "user_to_user"
# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_sub_graph.json", "r") as f:
    data = json.load(f)

i = 1
for sub_data in data:
    G = nx.node_link_graph(sub_data)
    nx.write_graphml(G, f"datas/{file_name}/graphml/graph_{i}.graphml")
    i+=1

# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_main_graph.json", "r") as f:
    data = json.load(f)

G = nx.node_link_graph(data)
nx.write_graphml(G, f"datas/{file_name}/graphml/graph_0.graphml")



file_name = "article_to_article"
# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_sub_graph.json", "r") as f:
    data = json.load(f)

i = 1
for sub_data in data:
    G = nx.node_link_graph(sub_data)
    nx.write_graphml(G, f"datas/{file_name}/graphml/graph_{i}.graphml")
    i+=1

# JSON dosyasını oku
with open(f"datas/{file_name}/{file_name}_main_graph.json", "r") as f:
    data = json.load(f)

G = nx.node_link_graph(data)
nx.write_graphml(G, f"datas/{file_name}/graphml/graph_0.graphml")
