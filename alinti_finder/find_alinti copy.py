from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
import os, sys
import time
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]) + "/common")
from utils2 import *
from db2 import *


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
    


def find_article_citing_2(code:str, size:int, driver):
    try:

        all_div_tags = []
        for i in range(0, size, 10):
        
            url = build_parameterized_url("https://scholar.google.com/scholar",{"start":i,"hl":"tr",'as_sdt':'2005',"sciodt":"0,5","cites":code,"scipsc":""} )
            if i == 0:
                url = build_parameterized_url("https://scholar.google.com/scholar",{"oi":"bibs","hl":"tr","cites":code} )
            soup, result = get_response_change_ip_if_necessary_with_selenium(driver, url)
            if soup == None:
                return None, result
            
            div_tags = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})
            if len(div_tags) == 0:
                continue
            time.sleep(3)
            all_div_tags.extend(div_tags)

        return all_div_tags, True
    
    except Exception as e:
        print(f'Hata oluştu 214: {e}')
        return None, False


def parse_gsc_a_tr_class(html):
    pass

def main():
    driver = create_tor_driver()
    conn = postgres_connect("cities","admin","admin","localhost","5433")

    while True:

        article = get_first_unprocessed_2_articl_by_uni(conn, "GALATASARAY ÜNİVERSİTESİ")

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
