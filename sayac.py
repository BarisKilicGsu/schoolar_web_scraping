
# --- sayac 1-----
'''
import ijson
from unidecode import unidecode

def are_strings_equal_case_insensitive_and_no_whitespace(str1, str2):
    return unidecode(''.join(str1.lower().split())) == unidecode(''.join(str2.lower().split()))


count_total = 0
count_temel_alan = 0
count_bilim_alan = 0

target_word = "mühendis"
target_word2 = "Zühal"
file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        count_total += 1
        if are_strings_equal_case_insensitive_and_no_whitespace(target_word2,record["Ad Soyad"]):
            print(record)


print(count_total)

        for key, value in record.items():
            if isinstance(value, str) and target_word in value.lower():
                count_total += 1
                if key == "Temel Alan":
                    count_temel_alan += 1
                elif key == "Bilim Alan":
                    count_bilim_alan += 1


print(f"Herhangi bir alanda '{target_word}' kelimesini içeren record sayısı: {count_total}")
print(f"'Temel Alan' alanında '{target_word}' kelimesini içeren record sayısı: {count_temel_alan}")
print(f"'Bilim Alan' alanında '{target_word}' kelimesini içeren record sayısı: {count_bilim_alan}")
        
'''
        

# --- sayac 2 -----


import psycopg2
from psycopg2 import sql
import ijson
from difflib import get_close_matches
import re

def postgres_connect(database, user, password, host, port):
    print(database, user, password, host, port)
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

def get_first_unprocessed_user(conn):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM users WHERE is_found = {} and is_processed_2 = {} LIMIT 1").format( sql.Literal(True), sql.Literal(False))
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 456:", e)
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
        return None
    
def write_number_to_file(number, file_name):
    # Dosyayı "append" modunda aç
    with open(file_name, "a") as file:
        # Sayıyı virgülle birlikte dosyaya yaz
        file.write(',' + str(number))

    
'''
# Veritabanı bağlantısını oluşturma
cur = conn.cursor()

# Veritabanından tüm kullanıcı isimlerini çekme
cur.execute("SELECT name FROM users")

# Sonuçları alıp diziye dönüştürme
all_users_in_db = [row[0] for row in cur.fetchall()]

# Veritabanı ve imleci kapatma
cur.close()
'''



unique_names = set()
file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if record["Ad Soyad"] != "" and record["Ad Soyad"] != None:
            unique_names.add(record["Ad Soyad"])
    
all_users_in_json = list(unique_names)

conn = postgres_connect("cities","admin","admin","localhost","5433")


'''
bulunamayanlar = []

for user_in_db in all_users_in_db:
    result = find_similar_string(all_users_in_json, remove_abbreviations_and_parentheses(user_in_db))
    if result == 'Bulunamadı':
        bulunamayanlar.append(user_in_db)
        print(user_in_db)

print(len(bulunamayanlar))
'''

cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT count(*) FROM users WHERE is_found = {} and is_processed_2 = {} LIMIT 1").format( sql.Literal(True), sql.Literal(False))
cursor.execute(query)
row = cursor.fetchone()
# Veritabanı bağlantısını kapat
cursor.close()

file_name = 'files/will_deleting_user_ids.txt'
count = 1
all_count = row[0]
while True:
    user_in_db = get_first_unprocessed_user(conn)
    if user_in_db:
        user_ismi = user_in_db[2]
        user_id = user_in_db[0]

        result = find_similar_string(all_users_in_json, remove_abbreviations_and_parentheses(user_ismi))
        if not result:
            print(user_ismi)
            write_number_to_file(user_id,file_name)

        set_processed_status_for_user(conn, user_id)

        print(f"{count}/{all_count}")
        count += 1
    else:
        print("İşlenmemiş article bulunamadı.")
        break

conn.close()
