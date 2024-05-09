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

def upsert_makale(conn, user_id,article):
    cursor = conn.cursor()
    try:
        # Verilen ORCID'yi kontrol et
        query = sql.SQL("SELECT * FROM articles WHERE name = {} AND user_id = {}").format(sql.Literal(article["makale_ismi"]),sql.Literal(user_id))
        cursor.execute(query)
        existing_article = cursor.fetchone()
        if existing_article:
            query = sql.SQL("UPDATE articles SET makale_kod = {}, alinti_kod = {}, alinti_sayisi = {}, makale_url = {}, alinti_url = {}, updated_at = CURRENT_TIMESTAMP WHERE name = {} AND user_id = {} RETURNING id").format(
                                sql.Literal(article["makale_kod"]),
                                sql.Literal(article["alinti_kod"]),
                                sql.Literal(int(article["alinti_sayisi"])),
                                sql.Literal(article["makale_url"]),
                                sql.Literal(article["alinti_url"]),
                                sql.Literal(article["makale_ismi"]),
                                sql.Literal(user_id)
                            )
            cursor.execute(query)
            updated_article_id = cursor.fetchone()
            cursor.close()

            if updated_article_id:
                return updated_article_id[0], True
        else:
            query = sql.SQL("INSERT INTO articles (user_id, name, makale_kod, alinti_kod, alinti_sayisi, makale_url, alinti_url) VALUES ({}, {}, {}, {}, {}, {}, {}) RETURNING id").format(
                                sql.Literal(user_id),
                                sql.Literal(article["makale_ismi"]),
                                sql.Literal(article["makale_kod"]),
                                sql.Literal(article["alinti_kod"]),
                                sql.Literal(int(article["alinti_sayisi"])),
                                sql.Literal(article["makale_url"]),
                                sql.Literal(article["alinti_url"])
                            )
            
            cursor.execute(query)
            new_article_id = cursor.fetchone()
            cursor.close()
 
            if new_article_id:
                return new_article_id[0], False

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata 6341:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()

def insert_makale_just_tr_tag(conn, user_id, tr_tag):
    cursor = conn.cursor()
    try:
        query = sql.SQL("INSERT INTO articles (user_id, tr_tag) VALUES ({}, {}) RETURNING id").format(
                            sql.Literal(user_id),
                            sql.Literal(tr_tag),
                        )
        
        cursor.execute(query)
        new_article_id = cursor.fetchone()
        cursor.close()

        if new_article_id:
            return new_article_id[0], False

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata 5783:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()
'''
def insert_makale_just_tr_tag(conn, user_id, tr_tag):
    cursor = conn.cursor()
    try:
        query = sql.SQL("SELECT id FROM articles WHERE tr_tag = {} AND user_id = {}").format(sql.Literal(tr_tag),sql.Literal(user_id))
        cursor.execute(query)
        existing_article = cursor.fetchone()
        if existing_article:
            return existing_article[0], True
        else:
            query = sql.SQL("INSERT INTO articles (user_id, tr_tag) VALUES ({}, {}) RETURNING id").format(
                                sql.Literal(user_id),
                                sql.Literal(tr_tag),
                            )
            
            cursor.execute(query)
            new_article_id = cursor.fetchone()
            cursor.close()
 
            if new_article_id:
                return new_article_id[0], False

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata 5783:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()

'''

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
        print("Hata 2375:", e)
        return False

    finally:
        # Bağlantıyı kapat
        cursor.close()

def get_first_unprocessed_user(conn):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM users WHERE is_found = {} and is_processed = {} and created_at > '2024-03-10 08:24:10.48032+00' LIMIT 1").format( sql.Literal(True), sql.Literal(False))
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 456:", e)
        return None
    
def set_processed_status_for_user(conn, user_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {}").format(sql.Literal(True),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Kullanıcı ID {user_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 245:", e)


def set_not_found_status_for_user(conn, user_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_found = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {}").format(sql.Literal(False),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Kullanıcı ID {user_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 249:", e)


def get_first_unprocessed_article(conn):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM articles WHERE is_found = {} and is_processed = {} LIMIT 1").format( sql.Literal(True), sql.Literal(False))
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 6453:", e)
        return None
    
def set_processed_status_for_article(conn, article_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE articles SET is_processed = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {}").format(sql.Literal(True),sql.Literal(article_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Article ID {article_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 125:", e)

def set_not_found_status_for_article(conn, article_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE articles SET is_found = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {}").format(sql.Literal(False),sql.Literal(article_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Article ID {article_id} bulunamadı olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 24439:", e)


def get_first_unprocessed_2_article(conn, tek_cift):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL("SELECT * FROM articles WHERE is_found = {} and is_processed = {} and is_processed_2 = {} LIMIT 1").format( sql.Literal(True), sql.Literal(True), sql.Literal(False))
        if tek_cift == "tek":
            query = sql.SQL("SELECT * FROM articles WHERE is_found = {} and is_processed = {} and is_processed_2 = {} and id % 2 = 1 LIMIT 1").format( sql.Literal(True), sql.Literal(True), sql.Literal(False))
        if tek_cift == "cift":
            query = sql.SQL("SELECT * FROM articles WHERE is_found = {} and is_processed = {} and is_processed_2 = {} and id % 2 = 0 LIMIT 1").format( sql.Literal(True), sql.Literal(True), sql.Literal(False))
            
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 62453:", e)
        return None
    

def get_first_unprocessed_2_articl_by_uni(conn, uni):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()
        # Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
        query = sql.SQL(
            """SELECT articles.* 
            FROM articles 
            JOIN user_articles ON articles.id = user_articles.article_id
            JOIN users ON user_articles.user_id = users.id
            WHERE articles.is_found = {} and articles.is_processed_2 = {} and users.university = {}
            LIMIT 1"""
            ).format( sql.Literal(True), sql.Literal(False),sql.Literal(uni) )
      
        cursor.execute(query)
        row = cursor.fetchone()
        # Veritabanı bağlantısını kapat
        cursor.close()
        # İlk kaydı döndür
        return row
    except Exception as e:
        print("Hata oluştu 62453:", e)
        return None
    
def set_processed_2_status_for_article(conn, article_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE articles SET is_processed_2 = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {}").format(sql.Literal(True),sql.Literal(article_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Article ID {article_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 1235:", e)

def update_makale(conn, article_id, article):
    cursor = conn.cursor()

    try:
        query = sql.SQL("UPDATE articles SET makale_kod = {}, alinti_kod = {}, alinti_sayisi = {}, makale_url = {}, alinti_url = {}, name = {}, updated_at = CURRENT_TIMESTAMP WHERE id = {} RETURNING id").format(
                            sql.Literal(article["makale_kod"]),
                            sql.Literal(article["alinti_kod"]),
                            sql.Literal(int(article["alinti_sayisi"])),
                            sql.Literal(article["makale_url"]),
                            sql.Literal(article["alinti_url"]),
                            sql.Literal(article["makale_ismi"]),
                            sql.Literal(article_id)
                        )
        cursor.execute(query)
        updated_article_id = cursor.fetchone()
        cursor.close()

        if updated_article_id:
            return updated_article_id[0], True

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata 33541:", e)
        conn.rollback()
        return None, False

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()


def insert_article_citing_just_div_tag(conn, cited_article_id, div_tag):
    cursor = conn.cursor()
    try:
        query = sql.SQL("INSERT INTO articles_citing (cited_article_id, div_tag) VALUES ({}, {}) RETURNING id").format(
                            sql.Literal(cited_article_id),
                            sql.Literal(div_tag),
                        )
        
        cursor.execute(query)
        new_article_id = cursor.fetchone()
        cursor.close()

        if new_article_id:
            return new_article_id[0], False

        # Değişiklikleri kaydet
    except Exception as e:
        print("Hata 578313:", e)
        conn.rollback()
        return None

    finally:
        # Bağlantıyı kapat
        conn.commit()
        cursor.close()