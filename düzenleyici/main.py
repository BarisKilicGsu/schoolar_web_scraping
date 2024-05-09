import os, sys
import psycopg2
from psycopg2 import sql



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
        print(f"Hata 9314s: {e}")
        return None
    
def get_first_unprocessed_3_article(conn):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM articles WHERE is_processed_3 = {} ORDER BY alinti_sayisi DESC LIMIT 1").format(sql.Literal(False))

        cursor.execute(query)
        article = cursor.fetchone()

        query = sql.SQL("INSERT INTO articles2 (tr_tag, name, makale_kod, alinti_kod, alinti_sayisi, makale_url, alinti_url, is_processed, is_found) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}) RETURNING id").format(
                                sql.Literal(article[2]),
                                sql.Literal(article[3]),
                                sql.Literal(article[4]),
                                sql.Literal(article[5]),
                                sql.Literal(article[6]),
                                sql.Literal(article[7]),
                                sql.Literal(article[8]),
                                sql.Literal(article[9]),
                                sql.Literal(article[11])
                            )
            
        cursor.execute(query)

        query = sql.SQL("DELETE FROM articles WHERE name = {}").format(sql.Literal(article[3]))
        cursor.execute(query)

        # Veritabanı bağlantısını kapat
        conn.commit()
        cursor.close()
        # İlk kaydı döndür
        return None
    except Exception as e:
        print("Hata oluştu 62453:", e)
        conn.rollback()
        return e
    

def main():

    conn = postgres_connect("cities","admin","admin","localhost","5433")
    while True: 
        if get_first_unprocessed_3_article(conn):
            print("İşlenmemiş article bulunamadı.")
            break
if __name__ == "__main__":
    main()

