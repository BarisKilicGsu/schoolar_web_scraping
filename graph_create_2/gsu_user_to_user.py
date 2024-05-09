import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph
import csv


conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT uu.alinti_yapan_user, uu.alinti_yapılan_user , COUNT(*) AS agirlik
FROM user_to_user_citations as uu
JOIN users as au1 on au1.id = uu.alinti_yapan_user
JOIN users as au2 on au2.id = uu.alinti_yapılan_user
where au1.university = 'GALATASARAY ÜNİVERSİTESİ' and au2.university = 'GALATASARAY ÜNİVERSİTESİ' 
GROUP BY alinti_yapan_user, alinti_yapılan_user;
"""

edges = execute_sql_query(conn, query )

query2 = """
SELECT id , name 
from users 
where university = 'GALATASARAY ÜNİVERSİTESİ'
"""

users = execute_sql_query(conn, query2 )

user_map = {}

for user in users:
    user_map[user[0]] = user[1]

user_to_user = []

for each in edges:
    alinti_yapan, alinti_yapılan, adet = each
    user_to_user.append({"Source": alinti_yapan, "Target": alinti_yapılan, "Weight": adet})

with open('user_to_user_gsu.csv', 'w', newline='') as csvfile:
    #fieldnames = ['alinti_yapan_user', 'alinti_yapılan_user', 'adet']
    fieldnames = ['Source', 'Target', 'Weight']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in user_to_user:
        writer.writerow(row)

print("CSV dosyası oluşturuldu: user_to_user.csv")

conn.close()      
