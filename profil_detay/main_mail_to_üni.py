from unidecode import unidecode
import re
import psycopg2
from psycopg2 import sql
from bs4 import BeautifulSoup

def postgres_connect(database, user, password, host, port):
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
        print(f"Hata 9314s: {e}")
        return None

def set_processed_status_for_user(conn, a,b):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users set university = {} where university = 'None' and uni_mail = {}").format(sql.Literal(a),sql.Literal(b))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)


conn = postgres_connect("cities","admin","admin","localhost","5433")


cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("""SELECT university, 
       (SELECT uni_mail 
        FROM users AS u2 
        WHERE u1.university = u2.university AND u2.uni_mail != ''
        GROUP BY uni_mail 
        ORDER BY COUNT(*) DESC 
        LIMIT 1) AS most_common_uni_mail
FROM users AS u1
WHERE university NOT LIKE '%,%' and university != 'None' and university != ''
GROUP BY university;""")
cursor.execute(query)
users = cursor.fetchall()
cursor.close()

for user in users:
    print(user)
    set_processed_status_for_user(conn, user[0], user[1])
    
    #print(f'user id : {user[0]}  matchs : {matching_text}')
  
    #set_uni_user(conn, user[0], unis)
    



