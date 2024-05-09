import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query, drawe_graph_plots


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


print(nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out', weight="weight"))
print(nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in', weight="weight"))
print(nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out'))
print(nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in'))


conn.close()
