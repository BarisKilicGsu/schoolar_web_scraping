import time
from unidecode import unidecode
import random
import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
from difflib import get_close_matches
import re
from playsound import playsound
ses_dosyasi = "uyari_ses.mp3"


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

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

def are_strings_equal_case_insensitive_and_no_whitespace(str1, str2):
    return unidecode(''.join(str1.lower().split())) == unidecode(''.join(str2.lower().split()))

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

 
def get_response_change_ip_if_necessary(url, headers):

    counter = 10
    #---------------------------
    response = requests.request('GET',url, proxies=proxies, headers=headers)
    if response.status_code == 404 :
        return None, False
    if response.status_code == 403 :
        print(f"\n403 status kod: \nurl = {url} \nYeniden ip veriliyor\n")
        while(True):
            if counter < 1:
                print(f"\n11!!!!!!!!! Yeniden Deneme Sınırı Doldu !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None, False
            change_ip()
            counter -= 1
            #---------------------------
            response = requests.request('GET',url, proxies=proxies, headers=headers)
            if response.status_code == 403 :
                print(f"\n010!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                continue
            if response.status_code == 404 :
                print('test')
                return None, False
            elif response.status_code != 200:
                print(f"\n93!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Body  = {response.text} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None, False
            else:
                # yeni ip çek ve bastır
                break
    elif response.status_code != 200:
        print(f"\n33!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Body  = {response.text} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
        return None, False
    
    soup = BeautifulSoup(response.text, 'html.parser')

    if check_error_text(soup):
        print(f"\nÇok fazla istek hatası: \nurl = {url}\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!! \nYeniden ip veriliyor\n")
        while(True):
            if counter  < 1 :
                print(f"\n44!!!!!!!!! Yeniden Deneme Sınırı Doldu !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None, False
            change_ip()
            counter -= 1
            #---------------------------
            response = requests.request('GET',url, proxies=proxies, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            if response.status_code == 403 or response.status_code == 429 or (response.status_code == 200 and check_error_text(soup)):
                continue
            if response.status_code == 404 :
                return None, False
            elif response.status_code != 200:
                print(f"\n55!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Body = {response.text} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None, False
            else:
                # yeni ip çek ve bastır
                break
        soup = BeautifulSoup(response.text, "html.parser")

    return soup, True

def change_ip():
    # tor için ip değiştirme kısmı
    with Controller.from_port(port = 9051) as c:
        c.authenticate(password = "1805Sila")
        c.signal(Signal.NEWNYM)
    
    headers = { 'User-Agent': UserAgent().random }
    print(f"Your IP is : {requests.request('GET','https://ident.me', proxies=proxies, headers=headers).text}")

def change_ip_2(driver):
    # tor için ip değiştirme kısmı
    with Controller.from_port(port = 9051) as c:
        c.authenticate(password = "1805Sila")
        c.signal(Signal.NEWNYM)
    print('ip chaged')
    time.sleep(1)


def create_tor_driver():


    chrome_options = Options()
    chrome_options.add_argument("--window-size=1280x800")
    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

    # options.add_argument('--headless')

    # specifies the path to the chromedriver.exe
    
    driver = webdriver.Chrome(service=Service('/usr/lib/chromium-browser/chromedriver'), options=chrome_options)

    return driver
  
def get_response_change_ip_if_necessary_with_selenium(driver ,url):

    counter = 10
    #---------------------------
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if check_error_text(soup):
        print(f"\nÇok fazla istek hatası: \nurl = {url} \nYeniden ip veriliyor\n")
        
        while(check_error_text(soup)):
            change_ip_2(driver)
            user_input = input("Enter 'y' to continue: ")
            if user_input != 'y':
                print("Exiting due to user input.")
                return None, False
            driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
            
    return soup, True


def check_error_text(soup):
    return 'robot olmadığınızı doğrulayamıyoruz' in soup.text or  "Maalesef JavaScript kapalıyken sizin robot olmadığınızı doğrulayamıyoruz" in soup.text or 'Please enable JavaScript in your browser and reload this page' in soup.get_text() or "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text() or "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text()
