import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph


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
    
calculate_topologic_analiz_for_directed_graph(G, 'article_to_article/article_to_article')


conn.close()
