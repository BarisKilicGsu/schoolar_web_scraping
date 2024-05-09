import psycopg2
import matplotlib.pyplot as plt
import csv


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
        return None
    


def execute_sql_query(conn, query, params=None):
    try:
        # Veritabanına bağlan
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Sonuçları al
        results = cursor.fetchall()

        conn.commit()

        # Sonuçları döndür
        return results
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return None
    
all_data = False
show_plot = True
conn = postgres_connect("cities","admin","admin","localhost","5433")
min_year = 2000
max_year = 2024

# ----------------------------------------------------------------------------------------------------
#  toplam yayın sayısı vs yıl
# ----------------------------------------------------------------------------------------------------

def get_articles_per_year():
    query = """
    SELECT year, COUNT(*) AS article_count
    FROM articles
    GROUP BY year
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )
    
    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            article_counts = [row[1] if row[1] is not None else 0 for row in results]
            plt.clf()
            plt.bar(years, article_counts)
            plt.ylim(min(article_counts), max(article_counts) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Number of Articles')
            plt.title('Number of Articles per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Number of Articles per Year - Raw Data.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_article_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_article_counts:
                    years_article_counts[str(row[0])] += row[1]
                else:
                    years_article_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_article_counts:
                    years_article_counts["Unknown"] += row[1]
                else :
                    years_article_counts["Unknown"] = row[1]
            
        years = list(years_article_counts.keys())
        article_counts = list(years_article_counts.values())
        plt.clf()
        plt.bar(years, article_counts)
        plt.ylim(min(article_counts), max(article_counts) * 1.2) 
        plt.xlabel('Year')
        plt.ylabel('Number of Articles')
        plt.title('Number of Articles per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, article_counts[i], " " + str(article_counts[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Number of Articles per Year.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  ortalama yayın sayısı ( toplam yayın sayısı/o yıldaki hoca sayısı ) vs yıl
# ----------------------------------------------------------------------------------------------------

def get_avg_articles_per_year():

    query = """
    SELECT year,
        COUNT(DISTINCT ua.article_id) AS total_articles,
        COUNT(DISTINCT ua.user_id) AS total_users
    FROM articles a
    LEFT JOIN user_articles ua ON a.id = ua.article_id
    GROUP BY year
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )
    
    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            total_articles = [row[1] if row[1] is not None else 0 for row in results]
            total_users = [row[2] if row[2] is not None else 0 for row in results]

            # Ortalama yayın sayısını hesapla
            average_articles_per_user = [total_article / total_user if total_user != 0 else 0 for total_article, total_user in zip(total_articles, total_users)]
            plt.clf()
            plt.bar(years, average_articles_per_user)
            plt.ylim(min(average_articles_per_user), max(average_articles_per_user) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Average Number of Articles per User')
            plt.title('Average Number of Articles per User per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Number of Articles per Year.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_article_counts = {}
        years_user_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_article_counts:
                    years_article_counts[str(row[0])] += row[1]
                    years_user_counts[str(row[0])] += row[2]
                else:
                    years_article_counts[str(row[0])] = row[1]
                    years_user_counts[str(row[0])] = row[2]
            else:
                if "Unknown" in years_article_counts:
                    years_article_counts["Unknown"] += row[1]
                    years_user_counts["Unknown"] += row[2]
                else :
                    years_article_counts["Unknown"] = row[1]
                    years_user_counts["Unknown"] = row[2]
            
        years = list(years_article_counts.keys())
        total_articles = list(years_article_counts.values())
        total_users = list(years_user_counts.values())

        # Ortalama yayın sayısını hesapla
        average_articles_per_user = [total_article / total_user if total_user != 0 else 0 for total_article, total_user in zip(total_articles, total_users)]

        plt.clf()
        plt.bar(years, average_articles_per_user)
        plt.ylim(min(average_articles_per_user), max(average_articles_per_user) * 1.2) 
        plt.xlabel('Year')
        plt.ylabel('Average Number of Articles per User')
        plt.title('Average Number of Articles per User per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, average_articles_per_user[i], " {:.3f}".format(average_articles_per_user[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Average Number of Articles per User per Year.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  bir yılda yapılan makalelerin toplam citiation sayısı vs yıl
# ----------------------------------------------------------------------------------------------------

def get_cite_per_year():
    query = """
    SELECT year,
       SUM(a.alinti_sayisi) AS total_citations
    FROM articles a
    GROUP BY year
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )

    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            article_counts = [row[1] if row[1] is not None else 0 for row in results]
            plt.clf()
            plt.bar(years, article_counts)
            plt.ylim(min(article_counts), max(article_counts) * 1.23) 
            plt.xlabel('Year')
            plt.ylabel('Total Citations')
            plt.title('Total Citations per Year')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Total Citations per Year.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_article_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_article_counts:
                    years_article_counts[str(row[0])] += row[1]
                else:
                    years_article_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_article_counts:
                    years_article_counts["Unknown"] += row[1]
                else :
                    years_article_counts["Unknown"] = row[1]
            
        years = list(years_article_counts.keys())
        article_counts = list(years_article_counts.values())
        plt.clf()
        plt.bar(years, article_counts)
        plt.ylim(min(article_counts), max(article_counts) * 1.22) 
        plt.xlabel('Year')
        plt.ylabel('Total Citations')
        plt.title('Total Citations per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, article_counts[i], " " + str(article_counts[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Total Citations per Year.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")


# ----------------------------------------------------------------------------------------------------
#  ortalama cite sayısı ( bir yılda yapılan makalelerin toplam citiation sayısı/o yıldaki hoca sayısı ) vs yıl
# ----------------------------------------------------------------------------------------------------

def get_avg_cite_per_year():

    query1 = """
    SELECT year,
       SUM(a.alinti_sayisi) AS total_citations
    FROM articles a
    GROUP BY year
    ORDER BY year;
    """

    query2 = """
    SELECT year,
        COUNT(DISTINCT ua.user_id) AS user_count
    FROM articles a
    LEFT JOIN user_articles ua ON a.id = ua.article_id
    GROUP BY year
    ORDER BY year;
    """

    results1 = execute_sql_query(conn, query1 )
    results2 = execute_sql_query(conn, query2 )

    if all_data:
        if results1 and results2:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results1]
            total_articles = [row[1] if row[1] is not None else 0 for row in results1]
            total_users = [row[1] if row[1] is not None else 0 for row in results2]

            # Ortalama yayın sayısını hesapla
            average_articles_per_user = [total_article / total_user if total_user != 0 else 0 for total_article, total_user in zip(total_articles, total_users)]
            plt.clf()
            plt.bar(years, average_articles_per_user)
            plt.ylim(min(average_articles_per_user), max(average_articles_per_user) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Average Number of Cite per User')
            plt.title('Average Number of Cite per User per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Average Number of Cite per User per Year - Raw Data.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results1 and results2:
        years_cite_counts = {}
        years_user_counts = {}

        for row in results1:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_cite_counts:
                    years_cite_counts[str(row[0])] += row[1]
                else:
                    years_cite_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_cite_counts:
                    years_cite_counts["Unknown"] += row[1]
                else :
                    years_cite_counts["Unknown"] = row[1]
        
        for row in results2:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_user_counts:
                    years_user_counts[str(row[0])] += row[1]
                else:
                    years_user_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_user_counts:
                    years_user_counts["Unknown"] += row[1]
                else :
                    years_user_counts["Unknown"] = row[1]

        years = list(years_cite_counts.keys())
        total_articles = list(years_cite_counts.values())
        total_users = list(years_user_counts.values())

        # Ortalama yayın sayısını hesapla
        average_articles_per_user = [total_article / total_user if total_user != 0 else 0 for total_article, total_user in zip(total_articles, total_users)]

        plt.clf()
        plt.bar(years, average_articles_per_user)
        plt.ylim(min(average_articles_per_user), max(average_articles_per_user) * 1.2) 
        plt.xlabel('Year')
        plt.ylabel('Average Number of Cite per User')
        plt.title('Average Number of Cite per User per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, average_articles_per_user[i], " {:.3f}".format(average_articles_per_user[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Average Number of Cite per User per Year - Raw Data.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  o yılda makale yayınlamış hoca sayısı vs yıl
# ----------------------------------------------------------------------------------------------------

def get_users_per_year():
    query = """
    SELECT year,
        COUNT(DISTINCT ua.user_id) AS user_count
    FROM articles a
    LEFT JOIN user_articles ua ON a.id = ua.article_id
    GROUP BY year
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )

    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            users_counts = [row[1] if row[1] is not None else 0 for row in results]
            plt.clf()
            plt.bar(years, users_counts)
            plt.ylim(min(users_counts), max(users_counts) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Number of Users')
            plt.title('Number of Users Contributing to Articles per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Number of Users Contributing to Articles per Year - Raw Data.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_users_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_users_counts:
                    years_users_counts[str(row[0])] += row[1]
                else:
                    years_users_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_users_counts:
                    years_users_counts["Unknown"] += row[1]
                else :
                    years_users_counts["Unknown"] = row[1]
            
        years = list(years_users_counts.keys())
        users_counts = list(years_users_counts.values())
        plt.clf()
        plt.bar(years, users_counts)
        plt.ylim(min(users_counts), max(users_counts) * 1.2) 
        plt.xlabel('Year')
        plt.ylabel('Number of Users')
        plt.title('Number of Users Contributing to Articles per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, users_counts[i], " " + str(users_counts[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Number of Users Contributing to Articles per Year.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  her yıl yayın yapan üniversite sayısı vs yıl
# ----------------------------------------------------------------------------------------------------

def get_uni_per_year():

    query = """
        SELECT a.year,
        COUNT(DISTINCT u.university) AS university
        FROM articles a
        JOIN user_articles ua ON a.id = ua.article_id
        JOIN users u ON ua.user_id = u.id
        GROUP BY a.year
        ORDER BY a.year;
    """

    results = execute_sql_query(conn, query )

    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            unique_universities = [row[1] if row[1] is not None else 0 for row in results]
            plt.clf()
            plt.bar(years, unique_universities)
            plt.ylim(min(unique_universities), max(unique_universities) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Number of Unique Universities')
            plt.title('Number of Unique Universities Publishing Articles per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Number of Unique Universities Publishing Articles per Year - Raw Data.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_uni_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_uni_counts:
                    years_uni_counts[str(row[0])] += row[1]
                else:
                    years_uni_counts[str(row[0])] = row[1]
            else:
                continue
                if "Unknown" in years_uni_counts:
                    years_uni_counts["Unknown"] += row[1]
                else :
                    years_uni_counts["Unknown"] = row[1]
            
        years = list(years_uni_counts.keys())
        total_uni = list(years_uni_counts.values())
        plt.clf()
        plt.bar(years, total_uni)
        plt.ylim(min(total_uni), max(total_uni) * 1.1) 
        plt.xlabel('Year')
        plt.ylabel('Number of Unique Universities')
        plt.title('Number of Unique Universities Publishing Articles per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, total_uni[i], " " + str(total_uni[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Number of Unique Universities Publishing Articles per Year.png') 
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  tüm zamanlarda en çok yayını olan ilk 5 üni
# ----------------------------------------------------------------------------------------------------

def get_uni_pie_chart():

    query = """
        SELECT university,
            COUNT(*) AS article_count
        FROM (
            SELECT u.university AS university
            FROM articles a
            JOIN user_articles ua ON a.id = ua.article_id
            JOIN users u ON ua.user_id = u.id
            WHERE u.university != 'None'
        ) subquery
        GROUP BY university
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """

    results = execute_sql_query(conn, query )

    if results:
        universities = [row[0] for row in results]
        article_counts = [row[1] for row in results]
        plt.clf()
        plt.pie(article_counts, labels=universities, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Daireyi daire olarak çiz
        plt.title('Top 10 Universities with Most Articles')
        plt.savefig('datas/Top 10 Universities with Most Articles.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  her bir yıl için her hocanın yayınladığı makale sayısı ile box plot grafiği 
# ----------------------------------------------------------------------------------------------------

def plot_publications_per_author_boxplot():

    query = """
    SELECT year,
           ua.user_id AS author_id,
           COUNT(*) AS publication_count
    FROM articles a
    JOIN user_articles ua ON a.id = ua.article_id
    GROUP BY year, ua.user_id
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )

    if results:
        years = []
        publication_counts = []

        # Her yıl için hocanın yayınladığı makale sayısını topla
        for year in range(min_year, max_year):
            publications_in_year = [row[2] for row in results if row[0] == year]
            publication_counts.append(publications_in_year)

            # Yılları da kaydet
            if publications_in_year:
                years.append(year)

        # Box plot oluştur
        plt.clf()
        plt.figure(figsize=(10, 6))  # Figure boyutunu belirle
        plt.boxplot(publication_counts)
        plt.xticks(ticks=range(1, len(years) + 1), labels=[str(year) for year in years])  # x ekseninde yılları göster

        plt.xlabel('Year')
        plt.ylabel('Publications per Author')
        plt.title('Publications per Author per Year (Box Plot)')
        plt.xticks(rotation=90) 
        plt.grid(True)
        plt.savefig('datas/Publications per Author per Year (Box Plot).png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  her bir yıl için her hocanın yayınladığı makalenin alıntı sayısı ile box plot grafiği 
# ----------------------------------------------------------------------------------------------------

def plot_cite_per_author_boxplot():

    query = """
    SELECT year,
           ua.user_id AS author_id,
           SUM(a.alinti_sayisi) AS total_citations
    FROM articles a
    JOIN user_articles ua ON a.id = ua.article_id
    GROUP BY year, ua.user_id
    ORDER BY year;
    """

    results = execute_sql_query(conn, query )

    if results:
        years = []
        publication_counts = []

        # Her yıl için hocanın yayınladığı makale sayısını topla
        for year in range(min_year, max_year):
            publications_in_year = [row[2] for row in results if row[0] == year]
            publication_counts.append(publications_in_year)

            # Yılları da kaydet
            if publications_in_year:
                years.append(year)

        # Box plot oluştur
        plt.clf()
        plt.figure(figsize=(10, 6))  # Figure boyutunu belirle
        plt.boxplot(publication_counts)
        plt.xticks(ticks=range(1, len(years) + 1), labels=[str(year) for year in years])  # x ekseninde yılları göster

        plt.xlabel('Year')
        plt.ylabel('Citations per Author')
        plt.title('Citations per Author per Year (Box Plot)')
        plt.xticks(rotation=90) 
        plt.grid(True)
        plt.savefig('datas/Citations per Author per Year (Box Plot).png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  her yıl yayın yapan departman sayısı vs yıl
# ----------------------------------------------------------------------------------------------------

def get_department_per_year():

    query = """
        SELECT a.year,
        COUNT(DISTINCT u.bilim_alani) AS bilim_alani
        FROM articles a
        JOIN user_articles ua ON a.id = ua.article_id
        JOIN users u ON ua.user_id = u.id
        GROUP BY a.year
        ORDER BY a.year;
    """

    results = execute_sql_query(conn, query )

    if all_data:
        if results:
            years = [str(row[0]) if row[0] is not None else 'Unknown' for row in results]
            unique_departments = [row[1] if row[1] is not None else 0 for row in results]
            plt.clf()
            plt.bar(years, unique_departments)
            plt.ylim(min(unique_departments), max(unique_departments) * 1.2) 
            plt.xlabel('Year')
            plt.ylabel('Number of Unique Departments')
            plt.title('Number of Unique Departments Publishing Articles per Year - Raw Data')
            plt.xticks(rotation=90)
            plt.grid(True)
            plt.savefig('datas/Number of Unique Departments Publishing Articles per Year - Raw Data.png')
            if show_plot:
                plt.show()
        else:
            print("No results returned.")

    # yıla göre düzenlenmiş, min_year öncesi ve max_year sonrası unknow olarak işaretlenmiş

    if results:
        years_uni_counts = {}

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_uni_counts:
                    years_uni_counts[str(row[0])] += row[1]
                else:
                    years_uni_counts[str(row[0])] = row[1]
            else:
                continue
                if "Unknown" in years_uni_counts:
                    years_uni_counts["Unknown"] += row[1]
                else :
                    years_uni_counts["Unknown"] = row[1]
            
        years = list(years_uni_counts.keys())
        total_uni = list(years_uni_counts.values())
        plt.clf()
        plt.bar(years, total_uni)
        plt.ylim(min(total_uni), max(total_uni) * 1.1) 
        plt.xlabel('Year')
        plt.ylabel('Number of Unique Departments')
        plt.title('Number of Unique Departments Publishing Articles per Year')

        # Her barın üstünde değerleri yazdır
        for i in range(len(years)):
            plt.text(i, total_uni[i], " " + str(total_uni[i]), ha='center', va='bottom', rotation=90)

        plt.xticks(rotation=90)  # Yılları dikey olarak yazdır
        plt.savefig('datas/Number of Unique Departments Publishing Articles per Year.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")



# ----------------------------------------------------------------------------------------------------
#  tüm zamanlarda en çok yayını olan ilk 5 departman
# ----------------------------------------------------------------------------------------------------

def get_department_pie_chart():

    query = """
        SELECT bilim_alani,
            COUNT(*) AS article_count
        FROM (
            SELECT u.bilim_alani AS bilim_alani
            FROM articles a
            JOIN user_articles ua ON a.id = ua.article_id
            JOIN users u ON ua.user_id = u.id
            WHERE u.bilim_alani != 'None'
        ) subquery
        GROUP BY bilim_alani
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """

    results = execute_sql_query(conn, query )

    if results:
        departments = [row[0] for row in results]
        article_counts = [row[1] for row in results]
        plt.clf()
        plt.pie(article_counts, labels=departments, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Daireyi daire olarak çiz
        plt.title('Top 10 Departments with Most Articles')
        plt.savefig('datas/Top 10 Departments with Most Articles.png')
        if show_plot:
            plt.show()
    else:
        print("No results returned.")




get_articles_per_year()
get_avg_articles_per_year()
get_cite_per_year()
get_avg_cite_per_year()
get_users_per_year()
get_uni_per_year()
get_uni_pie_chart()
plot_publications_per_author_boxplot()
plot_cite_per_author_boxplot()
get_department_per_year()
get_department_pie_chart()




# ----------------------------------------------------------------------------------------------------
#  uni - yıl makale sayısı csv olarak
# ----------------------------------------------------------------------------------------------------


def uni_year_csv():

    uni_query = " SELECT DISTINCT university from users ORDER by university;"
    unis = execute_sql_query(conn, uni_query )

    print(len(unis))
    uni_data = {}
    for uni in unis:
        
       
        query = f"""
            SELECT a.year,
            COUNT(DISTINCT a) AS article_count
            FROM user_articles ua 
            JOIN articles a ON ua.article_id = a.id 
            JOIN users u ON ua.user_id = u.id
            WHERE u.university = '{uni[0]}'
            GROUP BY a.year
            ORDER BY a.year;
        """

        results = execute_sql_query(conn, query )

        years_article_counts = {}
        years_article_counts["Unknown"] = 0
        for y in range(min_year, max_year + 1):
            years_article_counts[str(y)] = 0

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_article_counts:
                    years_article_counts[str(row[0])] += row[1]
                else:
                    years_article_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_article_counts:
                    years_article_counts["Unknown"] += row[1]
                else :
                    years_article_counts["Unknown"] = row[1]

        
        uni_data[uni[0]] = years_article_counts
        

    header = ['Üniversite']
    header.extend(list(uni_data['ABDULLAH GÜL ÜNİVERSİTESİ'].keys()))

    with open('universities_year_makale_sayisi.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for university, values in uni_data.items():
            row = [university]
            row.extend(list(uni_data[university].values()))
            writer.writerow(row)

#uni_year_csv()


def departman_year_csv():

    uni_query = " SELECT DISTINCT bilim_alani from users ORDER by bilim_alani;"
    unis = execute_sql_query(conn, uni_query )

    print(len(unis))
    uni_data = {}
    for uni in unis:
        
       
        query = f"""
            SELECT a.year,
            COUNT(DISTINCT a) AS article_count
            FROM user_articles ua 
            JOIN articles a ON ua.article_id = a.id 
            JOIN users u ON ua.user_id = u.id
            WHERE u.bilim_alani = '{uni[0]}'
            GROUP BY a.year
            ORDER BY a.year;
        """

        results = execute_sql_query(conn, query )

        years_article_counts = {}
        years_article_counts["Unknown"] = 0
        for y in range(min_year, max_year + 1):
            years_article_counts[str(y)] = 0

        for row in results:
            if row[0] is not None and min_year <= row[0] <= max_year:
                if str(row[0]) in years_article_counts:
                    years_article_counts[str(row[0])] += row[1]
                else:
                    years_article_counts[str(row[0])] = row[1]
            else:
                if "Unknown" in years_article_counts:
                    years_article_counts["Unknown"] += row[1]
                else :
                    years_article_counts["Unknown"] = row[1]

        
        uni_data[uni[0]] = years_article_counts
        

    header = ['Bilim Alani']
    header.extend(list(uni_data['Bilgisayar Bilimleri ve Mühendisliği'].keys()))

    with open('departman_year_makale_sayisi.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for university, values in uni_data.items():
            row = [university]
            row.extend(list(uni_data[university].values()))
            writer.writerow(row)

#departman_year_csv()