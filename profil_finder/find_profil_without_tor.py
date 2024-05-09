from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
import sys, os
from psycopg2 import sql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from playsound import playsound

sys.path.append('..')  
from common.db2 import *
from common.utils2 import *


ses_dosyasi = "uyari_ses.mp3"


def setup():
    options = Options()
    #options.add_argument('--headless')

    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def find_profil_detail(url:str, driver):

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    while "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text() or "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text() :
        playsound(ses_dosyasi)
        print("Our systems have detected unusual traffic. Please intervene and confirm you are not a robot.")
        user_input = input("Enter 'yes' to continue: ")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # her makale bilgisinin bulunduğu obje
    profil_detay = soup.find('div', id='gsc_prf_i')
    profil_detay_2 = soup.find_all('div', {'class': 'gsc_rsb_s gsc_prf_pnl'})
    tr_tags = soup.find_all('tr', {'class': 'gsc_a_tr'})
    return profil_detay, profil_detay_2, True, tr_tags

def get_first_unprocessed_user11(conn):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM users WHERE university = 'GALATASARAY ÜNİVERSİTESİ' and is_found = {} and is_processed_2 = {} and created_at > '2024-03-10 08:24:10.48032+00' LIMIT 1").format( sql.Literal(True), sql.Literal(False))
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 456:", e)
        return None
    
def parse_gsc_a_tr_class(html):
    makale_bilgi = {
        "makale_ismi": "",
        "makale_url": "",
        "makale_kod":  "",
        "alinti_url": "",
        "alinti_kod" : "",
        "alinti_sayisi": 0
    }
    tr_tag = BeautifulSoup(html, 'html.parser')
    makale_a_tag = tr_tag.find('a', {'class': 'gsc_a_at'})
    makale_ismi = makale_a_tag.text.strip()
    makale_href_value = ""
    if makale_a_tag and 'href' in makale_a_tag.attrs:
        makale_href_value = makale_a_tag['href']
    parsed_url = urlparse(makale_href_value)
    query_params = parse_qs(parsed_url.query)
    makale_code_value = query_params.get('citation_for_view', [])[0] if 'citation_for_view' in query_params else None

    makale_yayin_bilgileri_divs = tr_tag.find_all('div', {'class': 'gs_gray'})
    makale_yayin_bilgileri = []
    for makale_bilgi_div in makale_yayin_bilgileri_divs:
        makale_yayin_bilgileri.append(makale_bilgi_div.text.strip())

    cities_a_tag = tr_tag.find('a', {'class': 'gsc_a_ac'})
    alinti_sayisi = cities_a_tag.text.strip()
    cities_href_value = ""
    if cities_a_tag and 'href' in cities_a_tag.attrs:
        cities_href_value = cities_a_tag['href']
    
    if alinti_sayisi == '':
        alinti_sayisi = '0'

    parsed_url = urlparse(cities_href_value)
    query_params = parse_qs(parsed_url.query)
    cities_code_value = query_params.get('cites', [])[0] if 'cites' in query_params else None

    makale_bilgi = {
        "makale_ismi": makale_ismi,
        "makale_url": makale_href_value,
        "makale_kod":  makale_code_value,
        "alinti_url": cities_href_value,
        "alinti_kod" : cities_code_value,
        "alinti_sayisi": int(alinti_sayisi),
    }

    return makale_bilgi


def set_processed_status_for_user11(conn, user_id, profil_detay, profil_detay_2, tr_tags):

    # Veritabanı bağlantısı oluştur
    cursor = conn.cursor()

    # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
    query = sql.SQL("UPDATE users SET is_processed_2 = {}, profil_detay = {} , profil_detay_2 = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(profil_detay),sql.Literal(profil_detay_2),sql.Literal(user_id))
    cursor.execute(query)

    for tr_tagg in tr_tags:
        tr_tag = str(tr_tagg)
        makale_bilgi = parse_gsc_a_tr_class(tr_tag)
        query = sql.SQL("SELECT id FROM articles WHERE name = {}").format(sql.Literal(makale_bilgi["makale_ismi"]))
        cursor.execute(query)
        existing_article = cursor.fetchone()
        if existing_article:
            query = sql.SQL("INSERT INTO user_articles (user_id, article_id) VALUES ({}, {}) RETURNING id").format(
                        sql.Literal(user_id),
                        sql.Literal(existing_article[0]),
                    )
            cursor.execute(query)
        else:
            query = sql.SQL("INSERT INTO articles (tr_tag) VALUES ({}) RETURNING id").format(
                        sql.Literal(str(tr_tag)),
                    )
            cursor.execute(query)
            new_article_id = cursor.fetchone()
            print(user_id, new_article_id[0])
            query = sql.SQL("INSERT INTO user_articles (user_id, article_id) VALUES ({}, {}) RETURNING id").format(
                        sql.Literal(user_id),
                        sql.Literal(new_article_id[0]),
                    )
            cursor.execute(query)

    # Veritabanı değişikliklerini kaydet
    conn.commit()
    # Veritabanı bağlantısını kapat
    cursor.close()
    print(f"Kullanıcı ID {user_id} işlenmiş olarak işaretlendi.")



def main():

    conn = postgres_connect("cities","admin","admin","localhost","5433")
    driver = setup()

    while True:
        user = get_first_unprocessed_user11(conn)
        if user:
            print("İşlenmemiş kullanıcı:", user[0])
            profil_detay, profil_detay_2, result, tr_tags = find_profil_detail(user[3], driver)
            
            if not result:
                print("HATAAAA")
                exit()
            
            set_processed_status_for_user11(conn, user[0], str(profil_detay), str(profil_detay_2), tr_tags)  # İlk sütun ID sütunu varsayıldı
        else:
            print("İşlenmemiş kullanıcı bulunamadı.")
            break

if __name__ == "__main__":
    main()
