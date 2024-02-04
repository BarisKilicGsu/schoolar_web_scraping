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
        print(f"Hata: {e}")
        return None


def upsert_user(conn, orcid, name, google_scholar_code, is_found):
    
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM users WHERE orcid = {}").format(sql.Literal(orcid))
        cursor.execute(query)
        existing_user = cursor.fetchone()
        if existing_user:
            # ORCID zaten var, kullanıcıyı güncelle
            query = sql.SQL("UPDATE users SET name = {}, google_scholar_code = {}, is_found = {} WHERE orcid = {} RETURNING id").format(
                                sql.Literal(name),
                                sql.Literal(google_scholar_code),
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
            query = sql.SQL("INSERT INTO users (orcid, name, google_scholar_code, is_found) VALUES ({}, {}, {}, {}) RETURNING id").format(
                                sql.Literal(orcid),
                                sql.Literal(name),
                                sql.Literal(google_scholar_code),
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



def upsert_makale(conn, user_id,article):
    
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM articles WHERE name = {} AND user_id = {}").format(sql.Literal(article["makale_ismi"]),sql.Literal(user_id))
        cursor.execute(query)
        existing_article = cursor.fetchone()
        if article["alinti_sayisi"] == "":
            article["alinti_sayisi"] = "0"
        if existing_article:
            query = sql.SQL("UPDATE articles SET makale_kod = {}, alinti_kod = {}, alinti_sayisi = {}, makale_href = {}, alinti_href = {} WHERE name = {} AND user_id = {} RETURNING id").format(
                                sql.Literal(article["makale_kod"]),
                                sql.Literal(article["alinti_kod"]),
                                sql.Literal(int(article["alinti_sayisi"])),
                                sql.Literal(article["makale_href"]),
                                sql.Literal(article["alinti_href"]),
                                sql.Literal(article["makale_ismi"]),
                                sql.Literal(user_id)
                            )
            cursor.execute(query)
            updated_article_id = cursor.fetchone()
            cursor.close()

            if updated_article_id:
                return updated_article_id[0], True
        else:
            query = sql.SQL("INSERT INTO articles (user_id, name, makale_kod, alinti_kod, alinti_sayisi, makale_href, alinti_href) VALUES ({}, {}, {}, {}, {}, {}, {}) RETURNING id").format(
                                sql.Literal(user_id),
                                sql.Literal(article["makale_ismi"]),
                                sql.Literal(article["makale_kod"]),
                                sql.Literal(article["alinti_kod"]),
                                sql.Literal(int(article["alinti_sayisi"])),
                                sql.Literal(article["makale_href"]),
                                sql.Literal(article["alinti_href"])
                            )
            
            cursor.execute(query)
            new_article_id = cursor.fetchone()
            cursor.close()
 
            if new_article_id:
                return new_article_id[0], False

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()


def upsert_alintilayan_makale(conn, article_id , alintilayan_makale):
    
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM alintilayan_makaleler WHERE title = {} AND article_id = {}").format(sql.Literal(alintilayan_makale["Title"]),sql.Literal(article_id))
        cursor.execute(query)
        existing_article = cursor.fetchone()
       
        if existing_article:
            query = sql.SQL("UPDATE alintilayan_makaleler SET authors = {}, journal = {}, citation_info = {}, alintilayan_makale_ek_divs = {}, alintilayan_makale_href = {}, alintilayan_makale_id = {} WHERE title = {} AND article_id = {} RETURNING id").format(
                                sql.Literal(alintilayan_makale["Authors"]),
                                sql.Literal(alintilayan_makale["Journal"]),
                                sql.Literal(alintilayan_makale["Citation Info"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_ek_divs"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_href"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_id"]),
                                sql.Literal(alintilayan_makale["Title"]),
                                sql.Literal(article_id)
                            )
            cursor.execute(query)
            updated_article_id = cursor.fetchone()
            cursor.close()

            if updated_article_id:
                return updated_article_id[0]
        else:
            query = sql.SQL("INSERT INTO alintilayan_makaleler (article_id, title, authors, journal, citation_info, alintilayan_makale_ek_divs, alintilayan_makale_href, alintilayan_makale_id) VALUES ({}, {}, {}, {}, {}, {}, {}, {}) RETURNING id").format(
                                sql.Literal(article_id),
                                sql.Literal(alintilayan_makale["Title"]),
                                sql.Literal(alintilayan_makale["Authors"]),
                                sql.Literal(alintilayan_makale["Journal"]),
                                sql.Literal(alintilayan_makale["Citation Info"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_ek_divs"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_href"]),
                                sql.Literal(alintilayan_makale["alintilayan_makale_id"])
                            )
            
            cursor.execute(query)
            new_article_id = cursor.fetchone()
            cursor.close()
 
            if new_article_id:
                return new_article_id[0]

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
        query = sql.SQL("SELECT * FROM users WHERE name = {} and is_found = {}").format(sql.Literal(name), sql.Literal(True))
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