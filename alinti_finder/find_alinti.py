from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
import os, sys

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]) + "/common")
from utils2 import *
from db2 import *


def find_article_citing(code:str, size:int,conn, a, b):
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
            url = build_parameterized_url("https://scholar.google.com/scholar",{"start":i,"hl":"tr",'as_sdt':'2005',"cites":code,"num":20,"scipsc":""} )
            if i == 0:
                url = build_parameterized_url("https://scholar.google.com/scholar",{"oi":"bibs","hl":"tr","cites":code,"num":20} )

            soup, result = get_response_change_ip_if_necessary(url,headers)
            if soup == None:
                return None, result
            print(soup.text)
            div_tags = soup.find_all('div', {'class': 'gs_r gs_or gs_scl'})
            if len(div_tags) == 0:
                continue
            for div_tag in div_tags:
                insert_article_citing_just_div_tag(conn , a, b, str(div_tag) )
            all_div_tags.extend(div_tags)

        return all_div_tags, True
    
    except Exception as e:
        print(f'Hata oluştu 214: {e}')
        return None, False
    
def parse_gsc_a_tr_class(html):
    pass

def main():

    if len(sys.argv) != 2:
        print("Kullanım: python program.py <tek veya cift>")
    else:
        tek_cift = sys.argv[1]
        conn = postgres_connect("cities","admin","admin","localhost","5433")
        print(tek_cift)
        sayac = 0
        while True:
            article = get_first_unprocessed_2_article(conn, tek_cift )
            if sayac > 1:
                change_ip()
                print("ip changed")
                sayac = 0
            else:
                sayac += 1

            if article:
                print("İşlenmemiş article:", article[0])
                if int(article[6]) == 0:
                    sayac -= 1
                    set_processed_2_status_for_article(conn, article[0])
                    continue
                div_tags, result = find_article_citing(article[5], article[6], conn , article[0], article[1])
                if not result:
                    print(f'kullanici makalesi cekilirken hata opldu, not found olarak islendi = {article[0]}')
                    set_not_found_status_for_article(conn, article[0])
                    continue
                print(f'-------------------------> {len(div_tags)}')
                
                set_processed_2_status_for_article(conn, article[0])  
            else:
                print("İşlenmemiş article bulunamadı.")
                break

if __name__ == "__main__":
    main()
