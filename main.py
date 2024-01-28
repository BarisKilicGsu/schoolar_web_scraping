from utils import *
from google_schoolar import *
import ijson
from config import settings
from db import *
import json
from playsound import playsound

ses_dosyasi = "uyari_ses.mp3"


def bulunan_kullanici_islemleri(conn ,record, code, driverManager):
    user_id = upsert_user(conn, record["ORCID"], record["Ad Soyad"], code, True )
    if user_id == None:
        print("!!!!!!!!!!!!!!!!! user id alınırken hataa !!!!!!!!!!!!!!!!!")
        return
    
    makaleler = find_profil_detail(code, driverManager)

    #print(makaleler)
    print(len(makaleler))
    for makale in makaleler:
        makale_id, is_exist = upsert_makale(conn, user_id, makale)

        if int(makale['alinti_sayisi']) == 0 or is_exist:
            continue

        alintilayan_makaleler = find_alinti_yapmis_makaleler(makale['alinti_kod'], int(makale['alinti_sayisi']), driverManager, conn , makale_id)
        print(len(alintilayan_makaleler), makale['alinti_sayisi'])

    print("bulunan eklendi")
    

    

def bulunamayan_kullanici_islemleri(conn ,record, code):
    upsert_user(conn, record["ORCID"],  record["Ad Soyad"], code , False)
    print("bulunamadı db ye eklendi")


def main():
    playsound(ses_dosyasi)
    file_path = 'files/gsu.json'

    db_connection = postgres_connect(settings.POSTGRES_DB, settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_HOST, settings.POSTGRES_PORT)
    driverManager = DriverManager()

    # deneme baslangıc
    '''
    bulunan_kullanici_islemleri(db_connection, record={"ORCID": "0000-0002-2243-7129", "Ad Soyad":"ÇAĞLA TANSUĞ"}, code="r08gEekAAAAJ", driver=driver)
    exit()
    '''
    # deneme son

    with open(file_path, "rb") as f:
        for record in ijson.items(f, "item"): 

            if record["ORCID"] == None or record["Ad Soyad"] == None or record["Ad Soyad"] == "":
                continue

            if user_is_exist_with_name(db_connection, record["Ad Soyad"]):
                print("-------------> user db de var, geçildi: " ,record["Ad Soyad"])
                continue

            code = find_lecturer_code(record["Ad Soyad"], driverManager)

            if code == None:

                if record["ORCID"] == None or record["ORCID"] == "":
                    print("-------------> Kullanıcı bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"])
                    bulunamayan_kullanici_islemleri(db_connection, record=record, code=code)
                    continue

                # olası ismi orciden bul 
                olasi_isim = orcid_user_control(record["ORCID"])
                # olasi isim orciden bulunamadıysa geç
                if olasi_isim == None or are_strings_equal_case_insensitive_and_no_whitespace(olasi_isim, record["Ad Soyad"]):
                    print("-------------> olasi isim bulunamadı, Kullanıcı bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"])
                    bulunamayan_kullanici_islemleri(db_connection, record=record, code=code)
                    continue

                # olasi ismi dene
                else:
                    random_bekleme()
                    olasi_code = find_lecturer_code(olasi_isim, driverManager)
                    #olasi isimle de bulunamadı
                    if olasi_code == None:
                        print("-------------> Kullanıcı orcidle beraber de bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"], olasi_isim)
                        bulunamayan_kullanici_islemleri(db_connection, record=record, code=code)
                        continue
                    # olasi isim bulundu ve eklendi
                    else:
                        bulunan_kullanici_islemleri(db_connection, record=record, code=olasi_code, driverManager=driverManager)
                        continue
            
            bulunan_kullanici_islemleri(db_connection, record=record, code=code, driverManager=driverManager)



if __name__ == "__main__":
    main()

