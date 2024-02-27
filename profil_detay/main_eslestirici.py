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

def remove_abbreviations_and_parentheses(input_string):

    # noktadan sonra boşluk atar ve birden fazla boşlukları tek boşluğa düşürür
    input_string = re.sub(r'\b\w+\.', '', input_string).strip()
    input_string = re.sub(r'\s+', ' ', input_string)

    # Parantez içindeki herhangi bir metni ve parantezleri boşluğa göre ayır
    words = re.split(r'(\(.*?\))|\s', input_string)

    # "." ile biten kelimeleri ve parantezleri kaldır
    cleaned_words = [word for word in words if word is not None and not (word.endswith(".") or (word.startswith("(") and word.endswith(")")))]

    # Temizlenmiş kelimeleri birleştirerek yeni bir string oluştur
    cleaned_string = " ".join(cleaned_words)

    return cleaned_string

def turkish_to_english_char(string):
    """
    Türkçe karakterleri İngilizce karakterlere çevirir.
    """
    tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u', 'İ': 'I', 'Ç': 'C', 'Ğ': 'G', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}
    return ''.join(tr_chars.get(c, c) for c in string)

def find_similar_string(string_list, query_string, cutoff=0.7):
    # Türkçe karakterleri İngilizce karakterlere çevir ve küçük harfe çevir
    string_list_lower = [turkish_to_english_char(s).lower() for s in string_list]
    query_string_lower = turkish_to_english_char(query_string).lower()
    
    # Küçük harfe çevrilmiş ve karakterleri dönüştürülmüş listeyi ve sorgu stringini kullanarak benzerlik ara
    matches = get_close_matches(query_string_lower, string_list_lower, n=1, cutoff=cutoff)
    # Eşleşme varsa, orijinal listeye göre eşleşen stringi dön
    if matches:
        match_index = string_list_lower.index(matches[0])
        return string_list[match_index]
    else:
        return 'None'

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
    except Exception as e:
        print("Hata oluştu 245:", e)

def set_uni_user(conn, user_id, uni):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed_2 = {}, orcid = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(uni),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)

conn = postgres_connect("cities","admin","admin","localhost","5433")


with open('../files/all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Boş bir sözlük oluştur
universite_ad_soyad = {}
universite_map = {}

# Her bir girişi işle
for entry in data:
    universite = entry['Üniversite']
    ad_soyad = entry['Ad Soyad']
    
    # Eğer üniversite daha önce eklenmediyse yeni bir listeye başla
    if universite not in universite_ad_soyad:
        universite_ad_soyad[universite] = []
        universite_map[universite] = {}
    
    # Ad Soyad'ı ilgili üniversitenin listesine ekle
    universite_ad_soyad[universite].append(ad_soyad)
    universite_map[universite][ad_soyad] = entry


universities_list = list(universite_ad_soyad.keys())

cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT * FROM users WHERE is_processed_2 = {} and university != {} and university = {}").format( sql.Literal(False),sql.Literal('None'),sql.Literal("KOÇ ÜNİVERSİTESİ"))
cursor.execute(query)
users = cursor.fetchall()
cursor.close()

count = 0
count2 = 0
count3 = 0

for user in users:
    üni = user[9]
    isim = user[1]
    isim = remove_abbreviations_and_parentheses(isim)

    üni_eslesme = find_similar_string(universities_list, üni, 0.8)
    if üni_eslesme == 'None':
        #eslesme bulunamadı 
        print(f'Bulunamadı ------- id : {user[0]}  --- üni = {üni} --- isim = {user[1]} ---  link : {user[3]}')
        set_processed_status_for_user(conn, user[0])
        count += 1
        continue

    matched_name = find_similar_string(universite_ad_soyad[üni_eslesme], isim, 0.9)
    if matched_name == 'None':
        print(f'Bulunamadı------- id : {user[0]}  üni = {üni} --- isim = {user[1]}  ---  link : {user[3]}')
        set_processed_status_for_user(conn, user[0])
        count += 1
        continue

    #print(f' üni = {üni} --- isim = {user[1]}  ////  eslesen üni = {üni_eslesme} --- eslesen isim = {matched_name} ')
    #print(universite_map[üni_eslesme][matched_name], universite_map[üni_eslesme][matched_name]['ORCID'])
    if universite_map[üni_eslesme][matched_name]['ORCID'] == None:
        count2 += 1
        continue
    set_uni_user(conn, user[0], universite_map[üni_eslesme][matched_name]['ORCID'])
    count3 += 1

print(count)
print(count2)
print(count3)
print(len(users))


