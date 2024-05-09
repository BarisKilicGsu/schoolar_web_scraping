from difflib import get_close_matches
from difflib import get_close_matches
import json
import ijson
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

def set_uni_user(conn, user_id, name):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE articles_citing SET is_processed = {}, name = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(name),sql.Literal(user_id))
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
query = sql.SQL("SELECT * FROM articles_citing WHERE is_processed = {} LIMIT 300000").format( sql.Literal(False))
cursor.execute(query)
articel_citings = cursor.fetchall()
cursor.close()

for articel_citing in articel_citings:
    div = articel_citing[2]
    
    soup = BeautifulSoup(div, 'html.parser')
    
    # data-aid veya data-cid'yi kontrol et
    data_aid = soup.find('div', {'data-aid': lambda x: x is not None and x != ''})
    data_cid = soup.find('div', {'data-cid': lambda x: x is not None and x != ''})

    if data_aid:
        link_id = data_aid['data-aid']
    elif data_cid:
        link_id = data_cid['data-cid']
    else:
        link_id = None

    # link_id'ye eşit olan <a> etiketini bul
    metin = ""
    if link_id:
        link = soup.find('a', {'id': link_id})
        if link:
            metin = link.text.strip()
        else:
            link = soup.find('span', {'id': link_id})
            if link:
                metin = link.text.strip()
            else:
                print(articel_citing[0])
                print("Link not found.")
                continue
    else:
        print(articel_citing[0])
        print("Data ID not found.")
        continue

    set_uni_user(conn, articel_citing[0],metin)
    
    #print(f'user id : {user[0]}  matchs : {matching_text}')
  
    #set_uni_user(conn, user[0], unis)
    



