import networkx as nx
from common import postgres_connect, execute_sql_query, calculate_topologic_analiz_for_directed_graph
import csv


conn = postgres_connect("cities","admin","admin","localhost","5433")


query = """
SELECT user_id, article_id 
FROM user_articles as ua 
JOIN users as u on u.id = ua.user_id
where u.university = 'GALATASARAY ÜNİVERSİTESİ'
ORDER BY article_id
"""

data = execute_sql_query(conn, query )

# Graph oluşturma
G = nx.Graph()


# Verileri işleyerek ilişkileri bulma
user_relations = {}

for each in data:
    user, makale = each
    for each2 in data:
        user2, makale2 = each2
        if user != user2 and makale2 == makale:
            user_pair = (user, user2) if user < user2 else (user2, user)
            print(user_pair)
            if user_pair in user_relations:
                user_relations[user_pair] += 1
            else:
                user_relations[user_pair] = 1
    



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

for users, weight in user_relations.items():
    user1_id, user2_id = users
    user_to_user.append({"user_1": user_map[user1_id], "user_2": user_map[user2_id], "adet": weight})

with open('co_authorship_gsu.csv', 'w', newline='') as csvfile:
    fieldnames = ['user_1', 'user_2', 'adet']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in user_to_user:
        writer.writerow(row)

print("CSV dosyası oluşturuldu: user_to_user.csv")

conn.close()      


