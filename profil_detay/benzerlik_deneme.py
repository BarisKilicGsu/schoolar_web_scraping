from difflib import get_close_matches
import json

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
        return 'Bulunamadı'

# Benzersiz üniversite listesini oku
with open('../files/unique_universities.json', 'r', encoding='utf-8') as f:
    universities_list = json.load(f)

# Örnek bir sorgu yap
query_string = 'Marmara Üniversitesi'
parts = query_string.split(',')

# Her bir parça için benzerlik fonksiyonunu çağır
for part in parts:
    part = part.strip()  # Boşlukları temizle
    result = find_similar_string(universities_list, part)
    if result != 'Bulunamadı':
        print(f"Bulunan eşleşme: {result}")
        break
else:
    print("Eşleşme bulunamadı.")
# query_string = 'ZONGULDAK BÜLENT ECEVİT ÜNİVERSİTESİ'

