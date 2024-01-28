import ijson
from config import settings
import json
from unidecode import unidecode
import random
from playsound import playsound
import psycopg2
from psycopg2 import sql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time
from fake_useragent import UserAgent



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
        print(f"Hata: {e}")
        return None


def upsert_user(conn, orcid, name, google_scholar_code, is_found):
    
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM users2 WHERE orcid = {}").format(sql.Literal(orcid))
        cursor.execute(query)
        existing_user = cursor.fetchone()
        profile_url = ""
        if google_scholar_code != None:
            profile_url = build_parameterized_url("https://scholar.google.com/citations",{"user":google_scholar_code,"hl":"tr","pagesize":10000,"cstart":0} )
        if existing_user:
            # ORCID zaten var, kullanıcıyı güncelle
            query = sql.SQL("UPDATE users2 SET name = {}, google_scholar_code = {}, profile_url = {}, is_found = {} WHERE orcid = {} RETURNING id").format(
                                sql.Literal(name),
                                sql.Literal(google_scholar_code),
                                sql.Literal(profile_url),
                                sql.Literal(is_found),
                                sql.Literal(orcid)
                            )
            cursor.execute(query)
            updated_user_id = cursor.fetchone()
            cursor.close()

            if updated_user_id:
                return updated_user_id[0]
        else:
            # ORCID yok, yeni kullanıcı ekle
            query = sql.SQL("INSERT INTO users2 (orcid, name, google_scholar_code,profile_url, is_found) VALUES ({}, {}, {},{}, {}) RETURNING id").format(
                                sql.Literal(orcid),
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


def user_is_exist_with_name(conn, name):
    
    cursor = conn.cursor()

    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM users2 WHERE name = {} ").format(sql.Literal(name))
        cursor.execute(query)
        existing_user = cursor.fetchone()

        if existing_user:
            return True
        else:
            return False

    except Exception as e:
        print("Hata:", e)
        return False

    finally:
        # Bağlantıyı kapat
        cursor.close()


class DriverManager:
    def __init__(self):
        self.driver = self.setup()

    def setup(self):
        options = Options()
        #options.add_argument('--headless')

        # specifies the path to the chromedriver.exe
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        return driver

    def refresh_driver(self):
        self.driver.quit()
        time.sleep(2)
        self.driver = self.setup()

def random_bekleme():
    wait_time = random.uniform(9, 10)  
    time.sleep(0.5)

 
def build_parameterized_url(base_url, params_dict):
    # Parametreleri URL formatına dönüştürmek için urllib.parse modülünü kullanabilirsiniz.
    from urllib.parse import urlencode

    # Parametrelerin URL formatına dönüştürülmesi
    param_str = urlencode(params_dict)

    # Temel URL ile birleştirilmesi
    parameterized_url = f"{base_url}?{param_str}"

    return parameterized_url

ses_dosyasi = "uyari_ses.mp3"


def bulunan_kullanici_islemleri(conn ,record, code, driverManager):
    user_id = upsert_user(conn, record["ORCID"], record["Ad Soyad"], code, True )

def bulunamayan_kullanici_islemleri(conn ,record):
    upsert_user(conn, record["ORCID"],  record["Ad Soyad"], None , False)
    print("bulunamadı db ye eklendi")

class SessionManager:
    def __init__(self):
        self.session = requests.Session()

    def save_session(self, response):
        # Önceki oturumu sakla
        self.saved_cookies = response.cookies.get_dict()

    def load_session(self):
        # Önceki oturumu yükle
        if hasattr(self, 'saved_cookies'):
            self.session.cookies.update(self.saved_cookies)
            return self.saved_cookies
        else:
            return ""

    def reset_session(self):
        # Oturumu sıfırla (çerezleri temizle)
        self.session.cookies.clear()
        if hasattr(self, 'saved_cookies'):
            delattr(self, 'saved_cookies')

session_manager = SessionManager()


def orcid_user_control(orcid: str):
    try:
        random_bekleme()

        url = f"https://pub.orcid.org/v3.0/expanded-search/?q=orcid%3A{orcid}&start=0&rows=50"
        ua = UserAgent()
        payload = {}
        headers = {
        'Sec-Fetch-Site': 'same-site',
        'Accept': 'application/json',
        'Origin': 'https://orcid.org',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Mode': 'cors',
        'Host': 'pub.orcid.org',
        'User-Agent': ua.random,
        'Referer': 'https://orcid.org/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        session_manager.save_session(response)
        print(response.text)

        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("expanded-result", []) == None:
                return None
            for result in json_data.get("expanded-result", []):
                orcid_id = result.get("orcid-id", "")
                if orcid_id == orcid:
                    return result.get("given-names", "") + " " + result.get("family-names", "")

        else:
            return None
    except Exception as e:
        print(f'Hata oluştu: {e}')
        return None



def find_lecturer_code(name:str, driverManager):
    try:
        random_bekleme()
        users = {}
        url = build_parameterized_url("https://scholar.google.com/citations",{"mauthors":name,"hl":"tr","view_op":"search_authors","btnG":""})
        driverManager.driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driverManager.driver.page_source, 'html.parser')
        if "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text():
            driverManager.refresh_driver()
            driverManager.driver.get(url)
            soup = BeautifulSoup(driverManager.driver.page_source, "html.parser")
        if "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text() :
            playsound(ses_dosyasi)
            print("Lütfen bir robot olmadığınızı gösterin")
            user_input = input("Enter 'y' to continue: ")
            if user_input.lower() != "y":
                print("Exiting due to user input.")
                return
            driverManager.driver.get(url)
            soup = BeautifulSoup(driverManager.driver.page_source, "html.parser")
        
        # h3 etiketlerini topla, bu user ismi ve linkine değer olucak
        h3_tags = soup.find_all('h3', {'class': 'gs_ai_name'})
        i = 0
        for h3_tag in h3_tags:
            
            # Her h3 etiketi içindeki a etiketini bulun, bu user codunu linkleyen objedir
            a_tag = h3_tag.find('a')

            href_value = ""
            print(a_tag)
            if a_tag and 'href' in a_tag.attrs:
                href_value = a_tag['href']

            if not are_strings_equal_or_include_case_insensitive_and_no_whitespace(a_tag.get_text(), name):
                continue
            
            parsed_url = urlparse(href_value)
            query_params = parse_qs(parsed_url.query)
            user_value = query_params.get('user', [])[0] if 'user' in query_params else None

            users[i] = {"a_tag": a_tag.get_text() ,"user_value":user_value}
            i+=1
        return users
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return None
    

def are_strings_equal_or_include_case_insensitive_and_no_whitespace(str1, str2):
    a = unidecode(''.join(str1.lower().split()))
    b = unidecode(''.join(str2.lower().split()))
    return (a == b ) or (a in b) or (b in a)


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

            users = find_lecturer_code(record["Ad Soyad"], driverManager)

            if len(users) == 0:

                if record["ORCID"] == None or record["ORCID"] == "":
                    print("-------------> Kullanıcı bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"])
                    bulunamayan_kullanici_islemleri(db_connection, record=record)
                    continue

                # olası ismi orciden bul 
                olasi_isim = orcid_user_control(record["ORCID"])
                # olasi isim orciden bulunamadıysa geç
                print(f"olasi isim = {olasi_isim}")
                if olasi_isim == None:
                    print("-------------> olasi isim bulunamadı, Kullanıcı bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"])
                    bulunamayan_kullanici_islemleri(db_connection, record=record)
                    continue

                # olasi ismi dene
                else:
                    random_bekleme()
                    olasi_users = find_lecturer_code(olasi_isim, driverManager)
                    #olasi isimle de bulunamadı
                    if olasi_users == None:
                        print("-------------> Kullanıcı orcidle beraber de bulunamadı hata, kullanıcı adı: " ,record["Ad Soyad"], olasi_isim)
                        bulunamayan_kullanici_islemleri(db_connection, record=record)
                        continue
                    # olasi isim bulundu ve eklendi
                    else:
                        if len(olasi_users) == 1:
                            bulunan_kullanici_islemleri(db_connection, record=record, code=olasi_users[0]["user_value"], driverManager=driverManager)
                            continue
                        if len(olasi_users) > 1:
                            playsound(ses_dosyasi)
                            print(f"\n\nIsmi = {record["Ad Soyad"]}\nORCIDE = {record["ORCID"]}\nkardo yeri: {record["Kadro Yeri"]}\n")
                            for key, value in olasi_users.items():
                                print(f"{key}: {value}")  
                            witch_user = input("hangi user alınsın, e girilise hiçbiri kabul edilir: ")
                            if witch_user == "e":
                                bulunamayan_kullanici_islemleri(db_connection, record=record)
                                continue
                            bulunan_kullanici_islemleri(db_connection, record=record, code=olasi_users[int(witch_user)]["user_value"], driverManager=driverManager)
                            continue
            if len(users) == 1:
                bulunan_kullanici_islemleri(db_connection, record=record, code=users[0]["user_value"], driverManager=driverManager)
                continue
            if len(users) > 1:
                playsound(ses_dosyasi)
                print(f"\n\nIsmi = {record["Ad Soyad"]}\nORCIDE = {record["ORCID"]}\nkardo yeri: {record["Kadro Yeri"]}\n")
                for key, value in users.items():
                    print(f"{key}: {value}")  
                witch_user = input("hangi user alınsın, e girilise hiçbiri kabul edilir: ")
                if witch_user == "e":
                    bulunamayan_kullanici_islemleri(db_connection, record=record)
                    continue
                bulunan_kullanici_islemleri(db_connection, record=record, code=users[int(witch_user)]["user_value"], driverManager=driverManager)
                continue
                

if __name__ == "__main__":
    main()


