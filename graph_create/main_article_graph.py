import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
from igraph import Graph, plot
import matplotlib.pyplot as plt
import numpy as np


def postgres_connect(database, user, password, host, port):
    print(database, user, password, host, port)
    try:
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Bağlantı başarılı.")
        return connection
    except Exception as e:
        return None
    


def execute_sql_query(conn, query, params=None):
    try:
        # Veritabanına bağlan
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Sonuçları al
        results = cursor.fetchall()

        conn.commit()

        # Sonuçları döndür
        return results
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return None
    
conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT alinti_yapan_user,alinti_yapılan_user , COUNT(*) AS agirlik
FROM user_to_user_citations
GROUP BY alinti_yapan_user, alinti_yapılan_user
LIMIT 1000;
"""

edges = execute_sql_query(conn, query )

# Boş bir graph oluştur
graph = Graph(directed=True)
print("girdi")
# Düğümleri ekleyin
nodes = set()
for edge in edges:
    source, target, _ = edge
    if source not in nodes:
        nodes.add(str(source))
    if target not in nodes:
        nodes.add(str(target))

print("girdi")
# Düğümleri grafa ekle
graph.add_vertices(list(nodes))
print("girdi")
# Edge'leri ve ağırlıkları ekleyin
for edge in edges:
    source, target, weight = edge
    graph.add_edge(str(source), str(target), weight=weight)

print("girdi")

#plot(graph, bbox=(10000, 10000), margin=20, target="graph.png", vertex_label=graph.vs["name"], edge_label=graph.es["weight"])


# Node sayısı
node_count = graph.vcount()
print("Node Sayısı:", node_count)

# Link sayısı
link_count = graph.ecount()
print("Link Sayısı:", link_count)

# Density
density = graph.density()
print("Density:", density)

# Ortalama derece (average degree)
average_degree = sum(graph.degree()) / graph.vcount()
print("Ortalama Derece:", average_degree)

# Maksimum derece (maximum degree)
max_degree = max(graph.degree())
print("Maksimum Derece:", max_degree)

# Minimum derece (minimum degree)
min_degree = min(graph.degree())
print("Minimum Derece:", min_degree)


# Diameter
diameter = graph.diameter()
print("Diameter:", diameter)

# İzole düğüm (isolated node) sayısı
isolated_nodes = len(graph.vs.select(_degree = 0))
print("İzole Düğüm Sayısı:", isolated_nodes)

# Bağlı bileşen (connected component) sayısı
connected_components = graph.connected_components()
print("Bağlı Bileşen Sayısı:", len(connected_components))

# Transitivity (clustering coefficient)
transitivity = graph.transitivity_undirected()
print("Transitivity (Clustering Coefficient):", transitivity)


