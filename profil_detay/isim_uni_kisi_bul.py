from difflib import get_close_matches
import json
import ijson
from unidecode import unidecode
import re

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
    print(matches)
    # Eşleşme varsa, orijinal listeye göre eşleşen stringi dön
    if matches:
        match_index = string_list_lower.index(matches[0])
        return string_list[match_index]
    else:
        return 'None'

# Benzersiz üniversite listesini oku
with open('../files/unique_universities.json', 'r', encoding='utf-8') as f:
    universities_list = json.load(f)

# Örnek bir sorgu yap
query_string = 'YILDIZ TEKNİK ÜNİVERSİTESİ'
isim = 'Tuğçe Koç'


isim = remove_abbreviations_and_parentheses(isim)
print(isim)
parts = query_string.split(',')

matched_universty = ""

# Her bir parça için benzerlik fonksiyonunu çağır
for part in parts:
    part = part.strip()  # Boşlukları temizle
    result = find_similar_string(universities_list, part)
    if result != 'Bulunamadı':
        matched_universty = result
        print(f"Bulunan eşleşme: {result}")
        break
else:
    print("Eşleşme bulunamadı.")
    exit()


'''
def are_strings_equal_case_insensitive_and_no_whitespace(str1, str2):
    return unidecode(''.join(turkish_to_english_char(str1).lower().split())) in unidecode(''.join(turkish_to_english_char(str2).lower().split())) or unidecode(''.join(turkish_to_english_char(str2).lower().split())) in unidecode(''.join(turkish_to_english_char(str1).lower().split()))

file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if record["Üniversite"] == matched_universty and are_strings_equal_case_insensitive_and_no_whitespace(isim,record["Ad Soyad"]):
            print(record["Ad Soyad"])
            print(record)
'''

unique_names = set()
file_path = '../files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if record["Üniversite"] == matched_universty:
            unique_names.add(record["Ad Soyad"])
    
name_list = list(unique_names)
print(name_list)
matched_name = find_similar_string(name_list, isim, 0.8)

print(result)

file_path = '../files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if record["Üniversite"] == matched_universty and record["Ad Soyad"] == matched_name:
            print(record)
            break

# query_string = 'ZONGULDAK BÜLENT ECEVİT ÜNİVERSİTESİ'

