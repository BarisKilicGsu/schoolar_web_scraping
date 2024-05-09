from difflib import get_close_matches
import json
import ijson
from unidecode import unidecode
import re

import psycopg2
from psycopg2 import sql

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


def set_bilim_alani_user(conn, user_id, bilim_alani):
    # Veritabanı bağlantısı oluştur
    cursor = conn.cursor()

    # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
    query = sql.SQL("UPDATE users SET is_processed_2 = {}, bilim_alani = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(bilim_alani),sql.Literal(user_id))
    cursor.execute(query)
    # Veritabanı değişikliklerini kaydet
    conn.commit()
    # Veritabanı bağlantısını kapat
    cursor.close()

conn = postgres_connect("cities","admin","admin","localhost","5433")


with open('../files/all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Boş bir sözlük oluştur
orcid_map = {}

# Her bir girişi işle
for entry in data:
    if 'ORCID' not in entry or entry['ORCID'] == '':
        continue
    orcid = entry['ORCID']
    bilim_alani = entry['Bilim Alan']
    
    orcid_map[orcid] = bilim_alani


orcid_list = list(orcid_map.keys())

cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT id, orcid FROM users WHERE is_processed_2 = {} and orcid IS NOT NULL AND orcid != ''").format( sql.Literal(False))
cursor.execute(query)
users = cursor.fetchall()
cursor.close()

count = 0
count2 = 0
count3 = 0

for user in users:
    id = user[0]
    orcid = user[1]

    if orcid not in orcid_list:
        count2 += 1
        continue

    set_bilim_alani_user(conn, id, orcid_map[orcid])
    count3 += 1

print(count)
print(count2)
print(count3)
print(len(users))


