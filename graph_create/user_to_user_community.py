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


print(len(edges))

connected_components = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
en_büyük_component = connected_components[0]
print(len(en_büyük_component))

newG = nx.DiGraph()

for edge in edges:
    source, target, weight = edge
    if str(source) in en_büyük_component and str(target) in en_büyük_component:
        newG.add_edge(str(source), str(target), weight=weight)
    
communs = nx.community.louvain_communities(newG, resolution=5 ,seed=123)
sorted_communities = sorted(communs, key=len, reverse=True)

print(len(sorted_communities))

comune_liste = [list(item) for item in sorted_communities]
sonuc_dict = {}
for i, eleman in enumerate(comune_liste, start=1):
    comun_record = {"size": len(eleman), "records":eleman}
    sonuc_dict[f"communiti_{i}"] =  comun_record

# JSON dosyasına kaydet
with open("datas/user_to_user/user_to_user_communities.json", "w") as dosya:
    json.dump(sonuc_dict, dosya)

print("JSON dosyası oluşturuldu: sonuc.json")


file_name = "user_to_user/user_to_user_alt_graph"
create_centrality_files(newG, file_name)


conn.close()
    
