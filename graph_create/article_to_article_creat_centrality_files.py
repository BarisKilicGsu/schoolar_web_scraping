import psycopg2
import networkx as nx
import csv
from common import postgres_connect, execute_sql_query, create_centrality_files


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

file_name = "article_to_article/article_to_article"

create_centrality_files(G, file_name)


        

conn.close()
