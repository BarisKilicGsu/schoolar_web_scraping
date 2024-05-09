
import ijson
from itertools import combinations
import json


def main():
    file_path = '../files/all.json'

    sayac = 0
    uniq_isimler = []
    with open(file_path, "rb") as f:
        for record in ijson.items(f, "item"): 
            

            isim = record["Ad Soyad"]
            temel_alan = record["Temel Alan"]
            
            if isim == None or isim == "":
                continue
            if temel_alan == None or temel_alan == "":
                continue
            if "mühendis" not in temel_alan.lower():
                continue
            
            kelimeler = isim.split()
            if len(kelimeler) > 1:
                sayac += 1
                for r in range(2, len(kelimeler) + 1):
                    for combo in combinations(kelimeler, r):
                        alt_isim = ' '.join(combo)
                        if alt_isim not in uniq_isimler:
                            uniq_isimler.append(alt_isim)
            
    print(uniq_isimler)
    isim_map = {}
    for i, isim in enumerate(uniq_isimler):
        isim_map[i] = isim

    # JSON dosyasına yazma işlemi
    with open('isimler.json', 'w') as f:
        json.dump(isim_map, f)

    print(sayac)
if __name__ == "__main__":
    main()


