import networkx as nx
from common import postgres_connect, execute_sql_query, create_centrality_files
import json
import numpy as np
import matplotlib.pyplot as plt



file_name = "user_to_user"


conn = postgres_connect("cities","admin","admin","localhost","5433")

# betweenness     closeness    eigenvector
# Betweenness     Closeness    Eigenvector


# ------------------------------------

query = """
SELECT DISTINCT ON (comun_id) comun_id, betweenness
FROM user_to_user_centrality
ORDER BY comun_id, betweenness DESC;
"""

data = execute_sql_query(conn, query )

eigenvector_values = [row[1] for row in data]

# Histogram oluşturma
plt.hist(eigenvector_values, bins=20, color='blue', alpha=0.7)
plt.xlabel('Betweenness Value')
plt.ylabel('Frequency')
plt.title('Histogram of Betweenness Values')
plt.grid(True)
plt.savefig(f'datas/{file_name}/{file_name}_betweenness_plot.png')
plt.show()

# Quartiles ve Quantiles değerlerini hesaplama
quartiles = np.percentile(eigenvector_values, [25, 50, 75])

print("Betweenness Quartiles:")
print("25th Percentile (Q1):", quartiles[0])
print("50th Percentile (Median, Q2):", quartiles[1])
print("75th Percentile (Q3):", quartiles[2])

# Veri setinin Q1 ve Q3 değerlerini hesaplayalım
Q1 = np.percentile(eigenvector_values, 25)
Q3 = np.percentile(eigenvector_values, 75)
# Interquartile Range (IQR) hesaplama
IQR = Q3 - Q1
# Aykırı değerlerin alt ve üst sınırlarını belirleme
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


# ------------------------------------

query = """
SELECT DISTINCT ON (comun_id) comun_id, closeness
FROM user_to_user_centrality
ORDER BY comun_id, closeness DESC;
"""

data = execute_sql_query(conn, query )

eigenvector_values = [row[1] for row in data]

# Histogram oluşturma
plt.hist(eigenvector_values, bins=20, color='blue', alpha=0.7)
plt.xlabel('Closeness Value')
plt.ylabel('Frequency')
plt.title('Histogram of Closeness Values')
plt.grid(True)
plt.savefig(f'datas/{file_name}/{file_name}_closeness_plot.png')
plt.show()

# Quartiles ve Quantiles değerlerini hesaplama
quartiles2 = np.percentile(eigenvector_values, [25, 50, 75])

print("Closeness Quartiles:")
print("25th Percentile (Q1):", quartiles2[0])
print("50th Percentile (Median, Q2):", quartiles2[1])
print("75th Percentile (Q3):", quartiles2[2])

# Veri setinin Q1 ve Q3 değerlerini hesaplayalım
Q1 = np.percentile(eigenvector_values, 25)
Q3 = np.percentile(eigenvector_values, 75)
# Interquartile Range (IQR) hesaplama
IQR = Q3 - Q1
# Aykırı değerlerin alt ve üst sınırlarını belirleme
lower_bound2 = Q1 - 1.5 * IQR
upper_bound2 = Q3 + 1.5 * IQR

# ------------------------------------

query = """
SELECT DISTINCT ON (comun_id) comun_id, eigenvector
FROM user_to_user_centrality
ORDER BY comun_id, eigenvector DESC;
"""

data = execute_sql_query(conn, query )

eigenvector_values = [row[1] for row in data]

# Histogram oluşturma
plt.hist(eigenvector_values, bins=20, color='blue', alpha=0.7)
plt.xlabel('Eigenvector Value')
plt.ylabel('Frequency')
plt.title('Histogram of Eigenvector Values')
plt.grid(True)
plt.savefig(f'datas/{file_name}/{file_name}_eigenvector_plot.png')
plt.show()

# Quartiles ve Quantiles değerlerini hesaplama
quartiles3 = np.percentile(eigenvector_values, [25, 50, 75])

print("Eigenvector Quartiles:")
print("25th Percentile (Q1):", quartiles3[0])
print("50th Percentile (Median, Q2):", quartiles3[1])
print("75th Percentile (Q3):", quartiles3[2])

# Veri setinin Q1 ve Q3 değerlerini hesaplayalım
Q1 = np.percentile(eigenvector_values, 25)
Q3 = np.percentile(eigenvector_values, 75)
# Interquartile Range (IQR) hesaplama
IQR = Q3 - Q1
# Aykırı değerlerin alt ve üst sınırlarını belirleme
lower_bound3 = Q1 - 1.5 * IQR
upper_bound3 = Q3 + 1.5 * IQR

# ------------------------------------



with open(f'datas/{file_name}/{file_name}_centrality.txt', 'w') as f:
    f.write("Betweenness Quartiles:\n")
    f.write("25th Percentile (Q1): {}\n".format( quartiles[0]))
    f.write("50th Percentile (Median, Q2): {}\n".format( quartiles[1]))
    f.write("75th Percentile (Q3): {}\n".format( quartiles[2]))
    f.write("Lower Bound (Q1 - 1.5 * IQR): {}\n".format(lower_bound))
    f.write("Upper Bound (Q3 + 1.5 * IQR): {}\n".format(upper_bound))
    f.write("Closeness Quartiles:\n")
    f.write("25th Percentile (Q1): {}\n".format( quartiles2[0]))
    f.write("50th Percentile (Median, Q2): {}\n".format( quartiles2[1]))
    f.write("75th Percentile (Q3): {}\n".format( quartiles2[2]))
    f.write("Lower Bound (Q1 - 1.5 * IQR): {}\n".format(lower_bound2))
    f.write("Upper Bound (Q3 + 1.5 * IQR): {}\n".format(upper_bound2))
    f.write("Eigenvector Quartiles:\n")
    f.write("25th Percentile (Q1): {}\n".format( quartiles3[0]))
    f.write("50th Percentile (Median, Q2): {}\n".format( quartiles3[1]))
    f.write("75th Percentile (Q3): {}\n".format( quartiles3[2]))
    f.write("Lower Bound (Q1 - 1.5 * IQR): {}\n".format(lower_bound3))
    f.write("Upper Bound (Q3 + 1.5 * IQR): {}\n".format(upper_bound3))

conn.close()
