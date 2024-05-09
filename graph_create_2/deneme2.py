
from common import postgres_connect, execute_sql_query_without_response, execute_sql_query

conn = postgres_connect("cities","admin","admin","localhost","5433")

query = """
SELECT name, COUNT(*), ARRAY_AGG(id) AS duplicate_ids
FROM articles
GROUP BY name
HAVING COUNT(*) > 1;
"""

edges = execute_sql_query(conn, query )

uzunluk = len(edges)
i = 0
for row in edges:
    
    duplicate_ids = row[2]
    max_id = max(duplicate_ids)
    liste_digerleri = [x for x in duplicate_ids if x != max_id]

    query_update = f"""
    UPDATE user_articles
    SET article_id = {max_id} 
    WHERE article_id IN ({', '.join(map(str, duplicate_ids))});
    """

    # Güncelleme sorgusunu çalıştır
    execute_sql_query_without_response(conn, query_update)

    query_update2 = f"""
    UPDATE articles_citing
    SET cited_article_id = {max_id} 
    WHERE cited_article_id IN ({', '.join(map(str, duplicate_ids))});
    """
        
    # Güncelleme sorgusunu çalıştır
    execute_sql_query_without_response(conn, query_update2)

    query_update3 = f"""
    DELETE FROM articles
    WHERE id IN ({', '.join(map(str, liste_digerleri))});
    """
        
    # Güncelleme sorgusunu çalıştır
    execute_sql_query_without_response(conn, query_update3)

    print(f"------------{i}/{uzunluk}----------------")
    i+=1
