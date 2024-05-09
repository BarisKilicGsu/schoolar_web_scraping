import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph


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


calculate_topologic_analiz_for_directed_graph(G, 'user_to_user/user_to_user')


conn.close()      
