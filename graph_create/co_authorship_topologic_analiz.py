import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_undirected_graph
import matplotlib.pyplot as plt
import pandas as pd


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


'''
# DataFrame oluşturma
df = pd.DataFrame(list(user_relations.items()), columns=['Users', 'Common Articles'])

# Users sütununu user_1 ve user_2 olarak iki ayrı sütuna ayırma
df[['user_1', 'user_2']] = pd.DataFrame(df['Users'].tolist(), index=df.index)

# Gereksiz Users sütununu kaldırma
df.drop(columns=['Users'], inplace=True)

# CSV dosyasına yazma
df.to_csv('co_authorship.csv', index=False)
'''


# Grafı göster
# nx.draw(G, with_labels=True)
# plt.show()

print([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)])
calculate_topologic_analiz_for_undirected_graph(G, 'co_authorship/co_authorship')



conn.close()
