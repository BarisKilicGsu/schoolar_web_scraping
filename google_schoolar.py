import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time
from db import *
from utils import *
from fake_useragent import UserAgent
from playsound import playsound

ses_dosyasi = "uyari_ses.mp3"


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


# --------------------------------------------------------- orcid user bulma ----------------------------------------------------- 

def orcid_user_control(orcid: str):
    try:
        random_bekleme()
        cook = session_manager.load_session()

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
        'Cookie': cook
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
    except:
        return None

# ------------------------------------------------------- orcid user makalelerini bulma --------------------------------------------------- 

def orcid_find_user_makaleleri(orcid: str ):
    random_bekleme()
    cook = session_manager.load_session()
    url = f"https://orcid.org/{orcid}/worksExtendedPage.json?offset=0&sort=date&sortAsc=false&pageSize=50"
    ua = UserAgent()
    payload = {}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'Host': 'orcid.org',
    'User-Agent': ua.random,
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': cook
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    session_manager.save_session(response)
    makaleler = [] 
    if response.status_code == 200:
        json_data = response.json()
        
        for group in json_data.get("groups", []):
            for work in group.get("works", []):
                title_value = work.get("title", {}).get("value", "")
                if title_value.lower() not in makaleler:
                    makaleler.append(title_value.lower())
        
        return makaleler
    else:
        return None


# --------------------------------------------------------- userların kodlaırnı bulma ----------------------------------------------------- 


def find_lecturer_code(name:str, driverManager):
    try:
        random_bekleme()
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
        for h3_tag in h3_tags:
            # Her h3 etiketi içindeki a etiketini bulun, bu user codunu linkleyen objedir
            a_tag = h3_tag.find('a')

            href_value = ""
            print(a_tag)
            if a_tag and 'href' in a_tag.attrs:
                href_value = a_tag['href']

            if not are_strings_equal_case_insensitive_and_no_whitespace(a_tag.get_text(), name):
                continue

            parsed_url = urlparse(href_value)
            query_params = parse_qs(parsed_url.query)
            user_value = query_params.get('user', [])[0] if 'user' in query_params else None

            return user_value

        return None
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return None
    


# ------------------------------------------------------ userların profil bilgilerini ve makalelerini bulma ----------------------------------------------------- 


def find_profil_detail(code:str, driverManager):
    try:
        random_bekleme()
        url = build_parameterized_url("https://scholar.google.com/citations",{"user":code,"hl":"tr","pagesize":10000,"cstart":0} )
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
        
        makaleler = []
        # her makale bilgisinin bulunduğu obje
        tr_tags = soup.find_all('tr', {'class': 'gsc_a_tr'})
        for tr_tag in tr_tags:
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
                "makale_href": makale_href_value,
                "makale_kod":  makale_code_value,
                "alinti_sayisi": alinti_sayisi,
                "alinti_href": cities_href_value,
                "alinti_kod" : cities_code_value
            }
            makaleler.append(makale_bilgi)
            
        return makaleler
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return None
    


# -------------------------------------------------------- makale alintilananları bul ------------------------------------------------------ 


def find_alinti_yapmis_makaleler(code:str, size:int, driverManager, conn, ana_makale_id):
    try:
        random_bekleme()
        alinti_yapmis_makaleler = []

        for i in range(0, size + 10, 10):

            url = build_parameterized_url("https://scholar.google.com/scholar",{"cites":code,"hl":"tr","start":i,"oi":"bibs"} )
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
            
    
            # her makale bilgisinin bulunduğu obje
            div_tags = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})
            for div_tag in div_tags:

                makale_id = ""
                if 'data-aid' in div_tag.attrs:
                    makale_id = div_tag['data-aid']
                elif 'data-cid' in div_tag.attrs:
                    makale_id = div_tag['data-cid']
                elif 'data-did' in div_tag.attrs:
                    makale_id = div_tag['data-did']
                
                data_cid = div_tag['data-cid']
                makale_bilgi = alinti_etiketini_al(data_cid, driverManager)
                a_tag = div_tag.find('h3', {'class': 'gs_rt'}).find('a')
                href_value = ""
                if a_tag is not None and 'href' in a_tag.attrs:
                    href_value = a_tag['href']
                
                gs_a_div = div_tag.find('div', {'class': 'gs_a'})
                text_content2= ""
                # div etiketinin içindeki metni yazdırın
                if gs_a_div:
                    text_content2 = gs_a_div.get_text(strip=True)

                makale_bilgi["alintilayan_makale_ek_divs"] = text_content2
                makale_bilgi["alintilayan_makale_href"] = href_value
                makale_bilgi["alintilayan_makale_id"] = makale_id
                upsert_alintilayan_makale(conn, ana_makale_id, makale_bilgi)
                alinti_yapmis_makaleler.append(makale_bilgi)
               
        return alinti_yapmis_makaleler
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return None
    
def alinti_etiketini_al( code:str , driverManager):

    info = {
        "Authors":"",
        "Title":"",
        "Journal":"",
        "Citation Info":"",
    }
    
    try:
        random_bekleme()

        url = build_parameterized_url("https://scholar.google.com/scholar",{"q":f"info:{code}:scholar.google.com/","hl":"en","scirp":"0","output":"cite"})
        driverManager.driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driverManager.driver.page_source, 'html.parser')
        if "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text():
            driverManager.refresh_driver()
            driverManager.driver.get(url)
            soup = BeautifulSoup(driverManager.driver.page_source, "html.parser")
        if "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text():
            playsound(ses_dosyasi)
            print("Lütfen bir robot olmadığınızı gösterin")
            user_input = input("Enter 'y' to continue: ")
            if user_input.lower() != "y":
                print("Exiting due to user input.")
                return
            driverManager.driver.get(url)
            soup = BeautifulSoup(driverManager.driver.page_source, "html.parser")

        
        
        for tr in soup.select('table tr'):
            # th etiketini kontrol et
            th = tr.find('th', {'class': 'gs_cith'})
            if th and th.text.strip() == 'Chicago':
                # Chicago ise, div etiketindeki metni al
                # &quot; arasındaki kısmı ayır
                divChicago = tr.find('div', {'class': 'gs_citr'})
                if divChicago is None or divChicago.contents is None or  divChicago.contents[0] is None or len(divChicago.contents) <= 0:
                    return info
                
                chicago_text = divChicago.contents[0].strip()
                authors_title_parts = chicago_text.split('"')
                # Liste boyutunu kontrol et
                if len(authors_title_parts) > 1:
                    authors = authors_title_parts[0].strip()
                    title = authors_title_parts[1].strip()

                    # <i> </i> arasındaki kısmı ayır
                    i_element = tr.find('i')
                    journal = i_element.text.strip() if i_element else ''

                    c_info = ""
                    if len(divChicago.get_text(strip=False, separator='\n').split('\n')) == 3:
                        c_info = divChicago.get_text(strip=False, separator='\n').split('\n')[2]
                    elif len(authors_title_parts) > 2:
                        c_info = authors_title_parts[2].strip()
                    else :
                        c_info = ""

                    # Verileri yazdır
                    info["Authors"] = authors
                    info["Title"] = title
                    info["Journal"] = journal
                    info["Citation Info"] = c_info
                else:
                    print("Hata: 'authors_title_parts' listesinde beklenen sayıda öğe yok.")

        return info
    
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        return info

# ------------------------------------------------------------------ main ------------------------------------------------------------------ 
