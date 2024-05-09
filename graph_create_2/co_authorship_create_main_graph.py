import networkx as nx
from common import postgres_connect, execute_sql_query, create_centrality_files
import json


conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT user_id, article_id 
FROM user_articles
ORDER BY article_id
"""

data = execute_sql_query(conn, query )

# Graph oluşturma
G = nx.Graph()


# Verileri işleyerek ilişkileri bulma
user_relations = {}

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        if data[i][1] != data[j][1]:
            break
        if data[i][0] != data[j][0]:
            user_pair = (data[i][0], data[j][0]) if data[i][0] < data[j][0] else (data[j][0], data[i][0])
            user_relations[user_pair] = user_relations.get(user_pair, 0) + 1


for users, weight in user_relations.items():
    user1_id, user2_id = users
    G.add_edge(str(user1_id), str(user2_id), weight=weight)


connected_components = sorted(nx.connected_components(G), key=len, reverse=True)
en_büyük_component = connected_components[0]
print(len(en_büyük_component))

newG = nx.Graph()

for users, weight in user_relations.items():
    user1_id, user2_id = users
    if str(user1_id) in en_büyük_component and str(user2_id) in en_büyük_component:
        newG.add_edge(str(user1_id), str(user2_id), weight=weight)


data = nx.node_link_data(newG)


# JSON dosyasına kaydet
with open("datas/co_authorship/co_authorship_main_graph.json", "w") as dosya:
    json.dump(data, dosya)

print("JSON dosyası oluşturuldu: sonuc.json")







conn.close()
