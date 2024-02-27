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

def set_processed_status_for_user(conn, user_id):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed_2 = {} WHERE id = {}").format(sql.Literal(True),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
        print(f"Kullanıcı ID {user_id} işlenmiş olarak işaretlendi.")
    except Exception as e:
        print("Hata oluştu 245:", e)

def set_metric_user(conn, user_id, h_endeksi, h_endeksi_2019_sonrası, i10_endeksi, i10_endeksi_2019_sonrası, alinti_sayısı, alinti_sayısı_2019_sonrası):
    try:
        # Veritabanı bağlantısı oluştur
        cursor = conn.cursor()

        # Belirli bir id ile kullanıcıyı işlenmiş olarak işaretle
        query = sql.SQL("UPDATE users SET is_processed_2 = {}, h_endeksi = {}, h_endeksi_2019_sonrası = {}, i10_endeksi = {}, i10_endeksi_2019_sonrası = {}, alinti_sayısı = {}, alinti_sayısı_2019_sonrası = {} WHERE id = {}").format(
            sql.Literal(True),sql.Literal(h_endeksi),sql.Literal(h_endeksi_2019_sonrası),sql.Literal(i10_endeksi),sql.Literal(i10_endeksi_2019_sonrası),sql.Literal(alinti_sayısı),sql.Literal(alinti_sayısı_2019_sonrası),sql.Literal(user_id))
        cursor.execute(query)
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        # Veritabanı bağlantısını kapat
        cursor.close()
    except Exception as e:
        print("Hata oluştu 245:", e)

def extract_metrics(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if cols:
                metric_name = cols[0].get_text(strip=True)
                all_value = cols[1].get_text(strip=True)
                recent_value = cols[2].get_text(strip=True)
                data[metric_name] = {"Hepsi": all_value, "2019 yılından bugüne": recent_value}

    return data

conn = postgres_connect("cities","admin","admin","localhost","5433")


cursor = conn.cursor()
# Users tablosundan is_processed değeri FALSE olan ilk kaydı çek
query = sql.SQL("SELECT * FROM users WHERE  is_processed_2 = {}").format( sql.Literal(False))
cursor.execute(query)
users = cursor.fetchall()
cursor.close()
for user in users:
    profil_detay_2_tag = user[8]

    if profil_detay_2_tag == '[]':
        # işlendi olarak işaretler
        set_metric_user(conn, user[0], 0,0,0,0,0,0)
        continue
    
    metrics_data = extract_metrics(profil_detay_2_tag)
    print(user[0])
    print(metrics_data)
    if len(metrics_data) == 0:
        set_metric_user(conn, user[0], 0,0,0,0,0,0)
        continue
    set_metric_user(conn, user[0], int(metrics_data["h-endeksi"]["Hepsi"]), int(metrics_data["h-endeksi"]["2019 yılından bugüne"]),int(metrics_data["i10-endeksi"]["Hepsi"]), int(metrics_data["i10-endeksi"]["2019 yılından bugüne"]),int(metrics_data["Alıntılar"]["Hepsi"]), int(metrics_data["Alıntılar"]["2019 yılından bugüne"]))
       



