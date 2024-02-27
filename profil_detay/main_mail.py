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

def set_processed_status_for_user(conn, user_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed_2 = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Kullanıcı ID {user_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 245:", e)

def set_uni_user(conn, user_id, uni):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed_2 = {}, uni_mail = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(uni),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)

def extract_edu_domains(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(text=True)
    matching_domains = []
    for element in elements:
        matches = re.findall(r'\b(\S*\.edu\S*)\b', element)
        matching_domains.extend(matches)
    return matching_domains


conn = postgres_connect("cities","admin","admin","localhost","5433")


cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT * FROM users WHERE is_processed_2 = {}").format( sql.Literal(False))
cursor.execute(query)
users = cursor.fetchall()
cursor.close()

for user in users:
    profil_detay_tag = user[7]

    if profil_detay_tag == 'None':
        # işlendi olarak işaretler
        set_processed_status_for_user(conn,user[0])
        continue
    
    matching_text = extract_edu_domains(profil_detay_tag)
    birlesik_string = ', '.join(matching_text)
    set_uni_user(conn, user[0],birlesik_string)
    
    #print(f'user id : {user[0]}  matchs : {matching_text}')
  
    #set_uni_user(conn, user[0], unis)
    



