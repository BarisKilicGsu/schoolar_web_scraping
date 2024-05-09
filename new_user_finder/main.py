from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
import os, sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import json


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


def find(driver, url:str):
 
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    while "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text() or "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text() :
        playsound(ses_dosyasi)
        print("Our systems have detected unusual traffic. Please intervene and confirm you are not a robot.")
        user_input = input("Enter 'yes' to continue: ")
        if user_input.lower() != "yes":
            print("Exiting due to user input.")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    return soup, True

def find_lecturer_code(name:str, driver):
    try:
        users = {}
        url = build_parameterized_url("https://scholar.google.com/citations",{"mauthors":name,"hl":"tr","view_op":"search_authors","btnG":""})
       
        soup, result = find(driver, url)
        if soup == None:
            return None, result
          
        # h3 etiketlerini topla, bu user ismi ve linkine değer olucak
        h3_tags = soup.find_all('h3', {'class': 'gs_ai_name'})
        i = 0
        for h3_tag in h3_tags:
            
            # Her h3 etiketi içindeki a etiketini bulun, bu user codunu linkleyen objedir
            a_tag = h3_tag.find('a')

            href_value = ""
            if a_tag and 'href' in a_tag.attrs:
                href_value = a_tag['href']

            parsed_url = urlparse(href_value)
            query_params = parse_qs(parsed_url.query)
            user_value = query_params.get('user', [])[0] if 'user' in query_params else None

            users[i] = {"a_tag": a_tag.get_text() ,"user_value":user_value}
            i+=1
        return users, True
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return None
    

def upsert_user(conn, name, google_scholar_code, is_found):
    
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM users WHERE google_scholar_code = {}").format(sql.Literal(google_scholar_code))
        cursor.execute(query)
        existing_user = cursor.fetchone()
        profile_url = ""
        if google_scholar_code != None:
            profile_url = build_parameterized_url("https://scholar.google.com/citations",{"user":google_scholar_code,"hl":"tr","pagesize":10000,"cstart":0} )
        if existing_user:
            # ORCID zaten var, kullanıcıyı güncelle
            query = sql.SQL("UPDATE users SET name = {},  profile_url = {}, is_found = {}, updated_at = CURRENT_TIMESTAMP WHERE google_scholar_code = {} RETURNING id").format(
                                sql.Literal(name),
                                sql.Literal(profile_url),
                                sql.Literal(is_found),
                                sql.Literal(google_scholar_code)
                            )
            cursor.execute(query)
            updated_user_id = cursor.fetchone()
            cursor.close()

            if updated_user_id:
                return updated_user_id[0]
        else:
            # ORCID yok, yeni kullanıcı ekle
            query = sql.SQL("INSERT INTO users ( name, google_scholar_code,profile_url, is_found) VALUES ( {}, {},{}, {}) RETURNING id").format(
                                sql.Literal(name),
                                sql.Literal(google_scholar_code),
                                sql.Literal(profile_url),
                                sql.Literal(is_found)
                            )
            
            cursor.execute(query)
            new_user_id = cursor.fetchone()
            cursor.close()
 
            if new_user_id:
                return new_user_id[0]

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()


def main():
    conn = postgres_connect("cities","admin","admin","localhost","5433")
    print(conn)

    driver = setup()

    with open('isimler.json', 'r') as f:
        isim_map = json.load(f)

    
    for key, isim in isim_map.items():
        print(key)
        if int(key) < 42882:
            continue
        users , result = find_lecturer_code(isim, driver)
        if not result:
            print('kullanici  cekilirken hata opldu')
            exit()
        
        for _, value in users.items():
            upsert_user(conn, value["a_tag"], value["user_value"], True)

if __name__ == "__main__":
    main()
