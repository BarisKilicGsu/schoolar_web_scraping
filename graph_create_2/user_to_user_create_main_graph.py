import networkx as nx
from common import postgres_connect, execute_sql_query, create_centrality_files
import json

conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT alinti_yapan_user,alinti_yapılan_user , COUNT(*) AS agirlik
FROM user_to_user_citations
GROUP BY alinti_yapan_user, alinti_yapılan_user;
"""

edges = execute_sql_query(conn, query )

# Boş bir ağırlıklı yönlü graf oluşturalım
G = nx.DiGraph()

# Kenarları ve ağırlıkları ekleme
for edge in edges:
    source, target, weight = edge
    G.add_edge(str(source), str(target), weight=weight)


connected_components = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
en_büyük_component = connected_components[0]

newG = nx.DiGraph()

for edge in edges:
    source, target, weight = edge
    if str(source) in en_büyük_component and str(target) in en_büyük_component:
        newG.add_edge(str(source), str(target), weight=weight)

data = nx.node_link_data(newG)      
    
# JSON dosyasına kaydet
with open("datas/user_to_user/user_to_user_main_graph.json", "w") as dosya:
    json.dump(data, dosya)

print("JSON dosyası oluşturuldu: sonuc.json")

conn.close()
    
