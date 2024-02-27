
import ijson
from unidecode import unidecode


'''
def are_strings_equal_case_insensitive_and_no_whitespace(str1, str2):
    return unidecode(''.join(str1.lower().split())) == unidecode(''.join(str2.lower().split()))

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

count_total = 0
count_temel_alan = 0
count_bilim_alan = 0

isim = "Prof.Dr.Nuray  Karabudak Yıldız"
target_word = "mühendis"
target_word2 = remove_abbreviations_and_parentheses(isim)

print(target_word2)
file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if are_strings_equal_case_insensitive_and_no_whitespace(target_word2,record["Ad Soyad"]):
            print(record)


file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if 'ORCID' in record and record['ORCID'] == '0000-0002-3090-2254':
            print(record)
            exit()
'''

 
file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        if 'Üniversite' in record and record['Üniversite'] == 'KOÇ ÜNİVERSİTESİ':
            if 'Ad Soyad' in record and 'SENA' in record['Ad Soyad']:     
                print(record['Ad Soyad'] , record['ORCID'])
        