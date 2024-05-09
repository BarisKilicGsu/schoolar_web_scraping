import psycopg2
from psycopg2 import sql
from bs4 import BeautifulSoup

def postgres_connect(database, user, password, host, port):
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
        print(f"Hata 9314s: {e}")
        return None

def set_year_user(conn, user_id, year):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE articles SET is_processed = {}, year = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(year),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)


conn = postgres_connect("cities","admin","admin","localhost","5433")


cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT * FROM articles WHERE is_processed = {} LIMIT 200000").format( sql.Literal(False))
cursor.execute(query)
articles = cursor.fetchall()
cursor.close()

for article in articles:
    div = article[1]
    
    soup = BeautifulSoup(div, 'html.parser')

    # Belirli sınıf değerini (class) bul
    target_class = soup.find('span', class_='gsc_a_h gsc_a_hc gs_ibl')

    year = 0
    # Eğer bulunursa içeriğini alıp tam sayıya çevir
    if target_class:
        text = target_class.text.strip()
        if text == "":
            set_year_user(conn, article[0], None)
            continue
        year = int(text)
    else:
        print(article[0])
        print("Sınıf değeri bulunamadı.")
        continue
        
    set_year_user(conn, article[0],year)
    
    #print(f'user id : {user[0]}  matchs : {matching_text}')
  
    #set_uni_user(conn, user[0], unis)
    



