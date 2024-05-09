import networkx as nx
from common import postgres_connect, execute_sql_query, create_centrality_files
import json
import numpy as np
import matplotlib.pyplot as plt



file_name = "co_authorship"


conn = postgres_connect("cities","admin","admin","localhost","5433")

cursor = conn.cursor()

# Her bir comun_id için ölçümleri alıp varyans hesaplamak için fonksiyon
def calculate_variance(comun_id):
    cursor.execute("SELECT betweenness, closeness, eigenvector FROM co_authorship_centrality WHERE comun_id = %s", (comun_id,))
    rows = cursor.fetchall()
    data = np.array(rows)

    # Varyans hesaplama
    betweenness_variance = np.var(data[:, 0])
    closeness_variance = np.var(data[:, 1])
    eigenvector_variance = np.var(data[:, 2])

    return betweenness_variance, closeness_variance, eigenvector_variance

# Her bir comun_id için varyansları hesaplayıp histogram çizme
cursor.execute("SELECT DISTINCT comun_id FROM co_authorship_centrality")
comun_ids = cursor.fetchall()

betweenness_variance = []
closeness_variance = []
eigenvector_variance = []

for comun_id in comun_ids:
    betweenness_varianc, closeness_varianc, eigenvector_varianc = calculate_variance(comun_id[0])
    betweenness_variance.append(betweenness_varianc)
    closeness_variance.append(closeness_varianc)
    eigenvector_variance.append(eigenvector_varianc)

# Histogram çizme
plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 1)
plt.hist(betweenness_variance, bins=10, color='blue', alpha=0.7)
plt.title('Betweenness Varyansı Histogramı')

plt.subplot(1, 3, 2)
plt.hist(closeness_variance, bins=10, color='green', alpha=0.7)
plt.title('Closeness Varyansı Histogramı')

plt.subplot(1, 3, 3)
plt.hist(eigenvector_variance, bins=10, color='red', alpha=0.7)
plt.title('Eigenvector Varyansı Histogramı')

plt.tight_layout()
plt.savefig(f'datas/{file_name}/{file_name}_variance_plot.png')
plt.show()

# Her bir comun_id için alt ve üst sınırları hesaplayıp yazdırma
def calculate_bounds(variance):
    # 1.5 * IQR
    lower_bound = np.percentile(variance, 25) - 1.5 * (np.percentile(variance, 75) - np.percentile(variance, 25))
    upper_bound = np.percentile(variance, 75) + 1.5 * (np.percentile(variance, 75) - np.percentile(variance, 25))
    return lower_bound, upper_bound


betweenness_lower_bound, betweenness_upper_bound = calculate_bounds(betweenness_variance)
closeness_lower_bound, closeness_upper_bound = calculate_bounds(closeness_variance)
eigenvector_lower_bound, eigenvector_upper_bound = calculate_bounds(eigenvector_variance)

print(f"Betweenness Varyansı Alt Sınırı: {betweenness_lower_bound}, Üst Sınırı: {betweenness_upper_bound}")
print(f"Closeness Varyansı Alt Sınırı: {closeness_lower_bound}, Üst Sınırı: {closeness_upper_bound}")
print(f"Eigenvector Varyansı Alt Sınırı: {eigenvector_lower_bound}, Üst Sınırı: {eigenvector_upper_bound}")

# Veritabanı bağlantısını kapatma
cursor.close()
conn.close()



