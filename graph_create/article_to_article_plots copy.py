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



print(nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out', weight="weight"))
print(nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in', weight="weight"))
print(nx.degree_pearson_correlation_coefficient(G, x = 'in', y = 'out'))
print(nx.degree_pearson_correlation_coefficient(G, x = 'out', y = 'in'))

conn.close()
