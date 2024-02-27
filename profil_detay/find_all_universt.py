import ijson
import json

file_path = 'files/all.json'
unique_universities = set()

# JSON dosyasını oku ve 'Üniversite' alanındaki benzersiz değerleri topla
with open(file_path, "rb") as f:
    for record in ijson.items(f, "item"):
        unique_universities.add(record["Üniversite"])

# Benzersiz 'Üniversite' değerlerini içeren bir JSON dosyasına yaz
output_file_path = 'files/unique_universities.json'
with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(list(unique_universities), outfile, ensure_ascii=False, indent=4)

print(f"Benzersiz üniversiteler {output_file_path} dosyasına yazıldı.")
