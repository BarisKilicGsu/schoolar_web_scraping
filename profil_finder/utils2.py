import time
from unidecode import unidecode
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


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

 
def get_response_change_ip_if_necessary(url):

    counter = 10
    #---------------------------
    response = requests.get(url)

    if response.status_code == 403:
        print(f"\n403 status kod: \nurl = {url} \nYeniden ip veriliyor\n")
        while(True):
            if counter :
                print(f"\n!!!!!!!!! Yeniden Deneme Sınırı Doldu !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None
            change_ip()
            counter -= 1
            #---------------------------
            response = requests.get(url)
            if response.status_code == 403:
                continue
            elif response.status_code != 200:
                print(f"\n!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None
            else:
                # yeni ip çek ve bastır
                break
    elif response.status_code != 200:
        print(f"\n!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    if "Lütfen bir robot olmadığınızı gösterin" in soup.get_text() or "Sistemimiz, bilgisayar ağınızdan gelen sıra dışı bir trafik algıladı" in soup.get_text() or "I'm not a robot" in soup.get_text() or "but your computer or network may be sending automated queries. To protect our users, we can't proc" in soup.get_text() :
        print(f"\nÇok fazla istek hatası: \nurl = {url} \nYeniden ip veriliyor\n")
        while(True):
            if counter :
                print(f"\n!!!!!!!!! Yeniden Deneme Sınırı Doldu !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None
            change_ip()
            counter -= 1
            #---------------------------
            response = requests.get(url)
            if response.status_code == 403:
                continue
            elif response.status_code != 200:
                print(f"\n!!!!!!!!! Bilinmeyen Hata !!!!!!!!!\n!!!!!!!!! url = {url} !!!!!!!!!\n!!!!!!!!! Status Code = {response.status_code} !!!!!!!!!\n!!!!!!!!! Yeniden ip veriliyor !!!!!!!!!\n")
                return None
            else:
                # yeni ip çek ve bastır
                break
        soup = BeautifulSoup(response.text, "html.parser")

    return soup

def change_ip():
    # tor için ip değiştirme kısmı

    time.sleep(2)
    return