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
ses_dosyasi = "uyari_ses.mp3"

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]) + "/common")
from utils2 import *
from db2 import *

import json


    
def find_article_citing(code:str, size:int):
    try:
        
        headers = {
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Alt-Used': 'scholar.google.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
        }

        all_div_tags = []
        if size > 1000:
            size = 1000
        for i in range(0, size, 20):
            url = build_parameterized_url("https://scholar.google.com/scholar",{"cites":code,"hl":"tr","start":i,"oi":"bibs","num":20} )

            soup, result = get_response_change_ip_if_necessary(url,headers)
            if soup == None:
                return None, result
            
            div_tags = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})
            if len(div_tags) == 0:
                continue
            all_div_tags.extend(div_tags)

        return all_div_tags, True
    
    except Exception as e:
        print(f'Hata oluştu 214: {e}')
        return None, False
    

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

def find_article_citing_2(code:str, size:int, driver):

    all_div_tags = []
    if size > 1000:
        size = 1000
    for i in range(0, size, 20):
    
        url = build_parameterized_url("https://scholar.google.com/scholar",{"start":i,"hl":"tr",'as_sdt':'2005',"sciodt":"0,5","cites":code,"num":20,"scipsc":""} )
        if i == 0:
            url = build_parameterized_url("https://scholar.google.com/scholar",{"oi":"bibs","hl":"tr","num":20,"cites":code} )
        soup, result = find(driver, url)
        if soup == None:
            return None, result
        
        div_tags = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})
        if len(div_tags) == 0:
            continue
        all_div_tags.extend(div_tags)

    return all_div_tags, True
    

def parse_gsc_a_tr_class(html):
    pass

def setup():
    options = Options()
    #options.add_argument('--headless')

    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

def main():
    
    playsound(ses_dosyasi)
    driver = setup()
    conn = postgres_connect("cities","admin","admin","localhost","5433")

    with open("unis.json", "r", encoding="utf-8") as file:
        universiteler = json.load(file)
    for universite in universiteler:
        while True:
            print(f'Üni = {universite}')
            article = get_first_unprocessed_2_articl_by_uni(conn, universite)

            if article:
                print("İşlenmemiş article:", article[0])
                if int(article[5]) == 0:
                    set_processed_2_status_for_article(conn, article[0])
                    continue
                div_tags, result = find_article_citing_2(article[4], article[5], driver)
                if not result:
                    print(f'kullanici makalesi cekilirken hata opldu, not found olarak islendi = {article[0]}')
                    set_not_found_status_for_article(conn, article[0])
                    continue
                for div_tag in div_tags:
                    insert_article_citing_just_div_tag(conn , article[0], str(div_tag) )
                set_processed_2_status_for_article(conn, article[0])  
            
            else:
                print("İşlenmemiş article bulunamadı.")
                break

if __name__ == "__main__":
    main()
