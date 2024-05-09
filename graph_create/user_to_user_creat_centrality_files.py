import psycopg2
import networkx as nx
import csv
from common import postgres_connect, execute_sql_query, create_centrality_files


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


file_name = "user_to_user/user_to_user"

katz_centrality = nx.katz_centrality(G, max_iter=8000000)
# Sonucu bir dosyaya kaydet
with open(f'datas/{file_name}_katz_centrality.csv', 'w', newline='') as csvfile:
    fieldnames = ['Node', 'Katz Centrality']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for node, centrality in katz_centrality.items():
        writer.writerow({'Node': node, 'Katz Centrality': centrality})


exit()
  
create_centrality_files(G, file_name)



conn.close()
