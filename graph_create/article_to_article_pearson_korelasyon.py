import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query, drawe_graph_plots


conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT alinti_yapan, alinti_yapılan 
FROM article_to_article_citations;
"""

edges = execute_sql_query(conn, query )

# Boş bir yönlü graf oluşturalım
G = nx.DiGraph()

# Kenarları ekleme
for edge in edges:
    source, target = edge
    G.add_edge(str(source), str(target))


a = nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out', weight="weight")
b = nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in', weight="weight")
c = nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out')
d = nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in')

print(a)
print(b)
print(c)
print(d)

file_name = "article_to_article/article_to_article"

with open(f'datas/{file_name}_pearson_korelasyon.txt', 'w') as f:
        f.write("Pearson Korelasyon Katsayısı (x = 'in', y = 'out', weight='weight'): {}\n".format(a))
        f.write("Pearson Korelasyon Katsayısı (x = 'out', y = 'in', weight='weight'): {}\n".format(b))
        f.write("Pearson Korelasyon Katsayısı (x = 'in', y = 'out'): {}\n".format(c))
        f.write("Pearson Korelasyon Katsayısı (x = 'out', y = 'in'): {}\n".format(d))

conn.close()
