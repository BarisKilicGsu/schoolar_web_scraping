import ijson

count_total = 0
count_temel_alan = 0
count_bilim_alan = 0

target_word = "mühendis"

file_path = 'files/all.json'
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
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