import pandas as pd

# CSV dosyasını oku
data = pd.read_csv('datas/co_authorship/co_authorship_eigenvector_centrality.csv')

# Betweenness Centrality'ye göre sırala ve ilk 5 düğümü al
top_5_nodes = data.sort_values(by='Eigenvector Centrality', ascending=False).head(5)

print("En yüksek Betweenness Centrality değerine sahip ilk 5 node:")
print(top_5_nodes)


# CSV dosyasını oku
data = pd.read_csv('datas/co_authorship/co_authorship_betweenness_centrality.csv')

# Betweenness Centrality'ye göre sırala ve ilk 5 düğümü al
top_5_nodes = data.sort_values(by='Betweenness Centrality', ascending=False).head(5)

print("En yüksek Betweenness Centrality değerine sahip ilk 5 node:")
print(top_5_nodes)



# CSV dosyasını oku
data = pd.read_csv('datas/co_authorship/co_authorship_closeness_centrality.csv')

# Betweenness Centrality'ye göre sırala ve ilk 5 düğümü al
top_5_nodes = data.sort_values(by='Closeness Centrality', ascending=False).head(5)

print("En yüksek Betweenness Centrality değerine sahip ilk 5 node:")
print(top_5_nodes)
