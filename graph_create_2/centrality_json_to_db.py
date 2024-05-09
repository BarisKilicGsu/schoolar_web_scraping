from common import postgres_connect, execute_sql_query
import json


conn = postgres_connect("cities","admin","admin","localhost","5433")

cursor = conn.cursor()

# co_authorship_centrality tablo varsa silme işlemi


try:
    cursor.execute("DROP TABLE IF EXISTS co_authorship_centrality;")
    conn.commit()
    print("co_authorship_centrality tablosu varsa silindi.")
except Exception as e:
    print("co_authorship_centrality tablo silinirken bir hata oluştu:", e)


try:
    cursor.execute("DROP TABLE IF EXISTS user_to_user_centrality;")
    conn.commit()
    print("user_to_user_centrality tablosu varsa silindi.")
except Exception as e:
    print("user_to_user_centrality tablo silinirken bir hata oluştu:", e)



try:
    cursor.execute("DROP TABLE IF EXISTS article_to_article_centrality;")
    conn.commit()
    print("article_to_article_centrality tablosu varsa silindi.")
except Exception as e:
    print("article_to_article_centrality tablo silinirken bir hata oluştu:", e)




# Yeni tablo oluşturma işlemi

try:
    cursor.execute("""
        CREATE TABLE co_authorship_centrality (
            user_id SERIAL PRIMARY KEY REFERENCES users(id),
            comun_id INTEGER,
            betweenness DOUBLE PRECISION,
            closeness DOUBLE PRECISION,
            eigenvector DOUBLE PRECISION
            
        );
    """)
    conn.commit()
    print("co_authorship_centrality tablosu oluşturuldu.")
except Exception as e:
    print("co_authorship_centrality tablo oluşturulurken bir hata oluştu:", e)

try:
    cursor.execute("""
        CREATE TABLE user_to_user_centrality (
            user_id SERIAL PRIMARY KEY REFERENCES users(id),
            comun_id INTEGER,
            betweenness DOUBLE PRECISION,
            closeness DOUBLE PRECISION,
            eigenvector DOUBLE PRECISION
            
        );
    """)
    conn.commit()
    print("user_to_user_centrality tablosu oluşturuldu.")
except Exception as e:
    print("user_to_user_centrality tablo oluşturulurken bir hata oluştu:", e)


try:
    cursor.execute("""
        CREATE TABLE article_to_article_centrality (
            article_id SERIAL PRIMARY KEY REFERENCES articles(id),
            comun_id INTEGER,
            betweenness DOUBLE PRECISION,
            closeness DOUBLE PRECISION,
            eigenvector DOUBLE PRECISION
            
        );
    """)
    conn.commit()
    print("article_to_article_centrality tablosu oluşturuldu.")
except Exception as e:
    print("article_to_article_centrality tablo oluşturulurken bir hata oluştu:", e)




# --------------------- data doldurma -------------------------------



with open("datas/co_authorship/co_authorship_centrality.json", "r") as f:
    json_data = json.load(f)
i = 0
for data in json_data:
    
    betweenness = data["centrality_data"]["betweenness"]
    closeness = data["centrality_data"]["closeness"]
    eigenvector = data["centrality_data"]["eigenvector"]

    for user_id in betweenness.keys():
        try:
            cursor.execute("""
                INSERT INTO co_authorship_centrality (user_id, betweenness, closeness, eigenvector, comun_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (int(user_id), betweenness[user_id], closeness[user_id], eigenvector[user_id], i))
            conn.commit()
        except Exception as e:
            print("Veri eklenirken bir hata oluştu1:", e)
    i+= 1

# -------------------------------------------------------------------

with open("datas/user_to_user/user_to_user_centrality.json", "r") as f:
    json_data = json.load(f)
i = 0
for data in json_data:
    
    betweenness = data["centrality_data"]["betweenness"]
    closeness = data["centrality_data"]["closeness"]
    eigenvector = data["centrality_data"]["eigenvector"]

    for user_id in betweenness.keys():
        try:
            cursor.execute("""
                INSERT INTO user_to_user_centrality (user_id, betweenness, closeness, eigenvector, comun_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (int(user_id), betweenness[user_id], closeness[user_id], eigenvector[user_id], i))
            conn.commit()
        except Exception as e:
            print("Veri eklenirken bir hata oluştu2:", e)
    i+= 1

# -------------------------------------------------------------------

with open("datas/article_to_article/article_to_article_centrality.json", "r") as f:
    json_data = json.load(f)
i = 0
for data in json_data:
    
    betweenness = data["centrality_data"]["betweenness"]
    closeness = data["centrality_data"]["closeness"]
    eigenvector = data["centrality_data"]["eigenvector"]

    for article_id in betweenness.keys():
        try:
            cursor.execute("""
                INSERT INTO article_to_article_centrality (article_id, betweenness, closeness, eigenvector, comun_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (int(article_id), betweenness[article_id], closeness[article_id], eigenvector[article_id], i))
            conn.commit()
        except Exception as e:
            print("Veri eklenirken bir hata oluştu3:", e)
    i+= 1
    

# PostgreSQL bağlantısını kapatma
cursor.close()
conn.close()
print("PostgreSQL bağlantısı kapatıldı.")