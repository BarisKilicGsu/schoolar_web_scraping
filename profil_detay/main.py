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



# Benzersiz üniversite listesini oku
with open('../files/unique_universities.json', 'r', encoding='utf-8') as f:
    universities_list = json.load(f)



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
        query = sql.SQL("UPDATE users SET is_processed_2 = {}, university = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(uni),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(text=True)
    text_list = [element.strip() for element in elements if element.strip()]
    return ', '.join(text_list)

conn = postgres_connect("cities","admin","admin","localhost","5433")


cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT * FROM users WHERE is_processed_2 = {} and created_at > '2024-03-10 08:24:10.48032+00'").format( sql.Literal(False))
cursor.execute(query)
users = cursor.fetchall()
cursor.close()
for user in users:
    profil_detay_tag = user[7]

    if profil_detay_tag == 'None':
        # işlendi olarak işaretler
        set_processed_status_for_user(conn,user[0])
        continue
    
    result = extract_text(profil_detay_tag)
    print(result)
    print("*-------------------------*------")
    parts = result.split(',')

    eslesmeler = []
    for part in parts:
        pattern = r'(?i).*?(university|üniversite|üniversitesi)\b'

        match = re.match(pattern, part)
        if match:
            part = match.group(0)
        print(part)
        part = part.strip()  # Boşlukları temizle
        result = find_similar_string(universities_list, part)
        if result != 'None':
            eslesmeler.append(result)
    
    print(f'user id : {user[0]}  div_tag : {result}  eslesmeler : {eslesmeler}')
    unis = ", ".join(eslesmeler)
    set_uni_user(conn, user[0], unis)



