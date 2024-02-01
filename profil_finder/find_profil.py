from utils2 import *
from db2 import *
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent


def find_profil_detail(code:str):
    try:
        url = build_parameterized_url("https://scholar.google.com/citations",{"user":code,"hl":"tr","pagesize":10000,"cstart":0} )
        headers = { 'User-Agent': UserAgent().random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    }
        soup = get_response_change_ip_if_necessary(url,headers)
        if soup == None:
            return None
        
        # her makale bilgisinin bulunduğu obje
        tr_tags = soup.find_all('tr', {'class': 'gsc_a_tr'})
        
        return tr_tags
    
    except Exception as e:
        print(f'Hata oluştu 214: {e}')
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


def main():

    conn = postgres_connect("cities","admin","admin","localhost","5433")


    while True:
        user = get_first_unprocessed_user(conn)
        if user:
            print("İşlenmemiş kullanıcı:", user)
            tr_tags = find_profil_detail(user[3])
            for tr_tag in tr_tags:
                insert_makale_just_tr_tag(conn , user[0], str(tr_tag) )
            set_processed_status_for_user(conn, user[0])  # İlk sütun ID sütunu varsayıldı
        else:
            print("İşlenmemiş kullanıcı bulunamadı.")
            break

if __name__ == "__main__":
    main()
