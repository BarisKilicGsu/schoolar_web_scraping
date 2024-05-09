import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
from scipy.stats import pearsonr
import numpy as np
import pandas as pd


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
    
def execute_sql_query_without_response(conn, query, params=None):
    try:
        # Veritabanına bağlan
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()

        # Sonuçları döndür
        return "ok"
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return None
    

def calculate_topologic_analiz_for_directed_graph(G, file_name):

    # Node sayısı
    node_count = G.number_of_nodes()

    # Link sayısı
    link_count = G.number_of_edges()

    # Density
    density = nx.density(G)

    # Ortalama derece
    average_degree = sum(dict(G.degree()).values()) / node_count

    # Maksimum derece
    max_degree = max(dict(G.degree()).values())

    # Minimum derece
    min_degree = min(dict(G.degree()).values())

    # İzole düğüm sayısı
    isolated_nodes_count = len(list(nx.isolates(G)))

    # Bağlı bileşen sayısı
    connected_components_count = nx.number_weakly_connected_components(G)

    # Transitivity (küresellik katsayısı)
    transitivity = nx.transitivity(G)

    # Diameter
    #diameter = max([max(j.values()) for (i,j) in nx.shortest_path_length(G)])

    # En büyük dereceye sahip ilk 5 düğümü seçelim
    degree_dict = dict(G.degree())
    sorted_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)
    top_5_nodes = sorted_nodes[:5]

    # louvain algoritması 
    communs_1 = nx.community.louvain_communities(G, resolution=1 )
    max_len_1 = 0
    for each in communs_1:
        if len(each) > max_len_1:
            max_len_1 = len(each)
    communs_1_modularity = nx.community.modularity(G=G, communities=communs_1)

    communs_1_5 = nx.community.louvain_communities(G, resolution=3 )
    max_len_1_5 = 0
    for each in communs_1_5:
        if len(each) > max_len_1_5:
            max_len_1_5 = len(each)
    communs_1_5_modularity = nx.community.modularity(G=G, communities=communs_1_5)

    communs_2 = nx.community.louvain_communities(G, resolution=5 )
    max_len_2 = 0
    for each in communs_2:
        if len(each) > max_len_2:
            max_len_2 = len(each)
    communs_2_modularity = nx.community.modularity(G=G, communities=communs_2)

    print("Node Sayısı:", node_count)
    print("Link Sayısı:", link_count)
    print("Density:", density)
    print("Ortalama Derece:", average_degree)
    print("Maksimum Derece:", max_degree)
    print("Minimum Derece:", min_degree)
    #print("Diameter:", diameter)
    print("İzole Düğüm Sayısı:", isolated_nodes_count)
    print("Bağlı Bileşen Sayısı:", connected_components_count)
    print("Transitivity:", transitivity)
    print("En büyük dereceye sahip ilk 5 düğüm:", top_5_nodes)
    print("Communities sayısı (Resolution = 1):", len(communs_1))
    print("En büyük communities boyutu (Resolution = 1):", max_len_1)
    print("Modularity (Resolution = 1):", communs_1_modularity)
    print("Communities sayısı (Resolution = 3):", len(communs_1_5))
    print("En büyük communities boyutu (Resolution = 3):", max_len_1_5)
    print("Modularity (Resolution = 3):", communs_1_5_modularity)
    print("Communities sayısı (Resolution = 5):", len(communs_2))
    print("En büyük communities boyutu (Resolution = 5):", max_len_2)
    print("Modularity (Resolution = 5):", communs_2_modularity)


    # Dosyaya yazma
    with open(f'datas/{file_name}_topologic_analiz.txt', 'w') as f:
        f.write("Node Sayısı: {}\n".format(node_count))
        f.write("Link Sayısı: {}\n".format(link_count))
        f.write("Density: {}\n".format(density))
        f.write("Ortalama Derece: {}\n".format(average_degree))
        f.write("Maksimum Derece: {}\n".format(max_degree))
        f.write("Minimum Derece: {}\n".format(min_degree))
        #f.write("Diameter: {}\n".format(diameter))
        f.write("İzole Düğüm Sayısı: {}\n".format(isolated_nodes_count))
        f.write("Bağlı Bileşen Sayısı: {}\n".format(connected_components_count))
        f.write("Transitivity: {}\n".format(transitivity))
        f.write("En büyük dereceye sahip ilk 5 düğüm: {}\n".format(top_5_nodes))
        f.write("Communities sayısı (Resolution = 1): {}\n".format(len(communs_1)))
        f.write("En büyük communities boyutu (Resolution = 1): {}\n".format(max_len_1))
        f.write("Communities sayısı (Resolution = 3): {}\n".format(len(communs_1_5)))
        f.write("En büyük communities boyutu (Resolution = 3): {}\n".format(max_len_1_5))
        f.write("Communities sayısı (Resolution = 5): {}\n".format(len(communs_2)))
        f.write("En büyük communities boyutu (Resolution = 5): {}\n".format(max_len_2))



def calculate_topologic_analiz_for_undirected_graph(G, file_name):

    # Node sayısı
    node_count = G.number_of_nodes()

    # Link sayısı
    link_count = G.number_of_edges()

    # Density
    density = nx.density(G)

    # Ortalama derece
    average_degree = sum(dict(G.degree()).values()) / node_count

    # Maksimum derece
    max_degree = max(dict(G.degree()).values())

    # Minimum derece
    min_degree = min(dict(G.degree()).values())

    # İzole düğüm sayısı
    isolated_nodes_count = len(list(nx.isolates(G)))

    # Bağlı bileşen sayısı
    connected_components_count = nx.number_connected_components(G)

    # Transitivity (küresellik katsayısı)
    transitivity = nx.transitivity(G)

    # Diameter 
    #diameter = max([max(j.values()) for (i,j) in nx.shortest_path_length(G)])


    # En büyük dereceye sahip ilk 5 düğümü seçelim
    degree_dict = dict(G.degree())
    sorted_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)
    top_5_nodes = sorted_nodes[:5]

    # louvain algoritması 
    communs_1 = nx.community.louvain_communities(G, resolution=1 )
    max_len_1 = 0
    for each in communs_1:
        if len(each) > max_len_1:
            max_len_1 = len(each)
    communs_1_modularity = nx.community.modularity(G=G, communities=communs_1)

    communs_1_5 = nx.community.louvain_communities(G, resolution=3 )
    max_len_1_5 = 0
    for each in communs_1_5:
        if len(each) > max_len_1_5:
            max_len_1_5 = len(each)
    communs_1_5_modularity = nx.community.modularity(G=G, communities=communs_1_5)

    communs_2 = nx.community.louvain_communities(G, resolution=5 )
    max_len_2 = 0
    for each in communs_2:
        if len(each) > max_len_2:
            max_len_2 = len(each)
    communs_2_modularity = nx.community.modularity(G=G, communities=communs_2)
            

    print("Node Sayısı:", node_count)
    print("Link Sayısı:", link_count)
    print("Density:", density)
    print("Ortalama Derece:", average_degree)
    print("Maksimum Derece:", max_degree)
    print("Minimum Derece:", min_degree)
    #print("Diameter:", diameter)
    print("İzole Düğüm Sayısı:", isolated_nodes_count)
    print("Bağlı Bileşen Sayısı:", connected_components_count)
    print("Transitivity:", transitivity)
    print("En büyük dereceye sahip ilk 5 düğüm:", top_5_nodes)
    print("Communities sayısı (Resolution = 1):", len(communs_1))
    print("En büyük communities boyutu (Resolution = 1):", max_len_1)
    print("Modularity (Resolution = 1):", communs_1_modularity)
    print("Communities sayısı (Resolution = 3):", len(communs_1_5))
    print("En büyük communities boyutu (Resolution = 3):", max_len_1_5)
    print("Modularity (Resolution = 3):", communs_1_5_modularity)
    print("Communities sayısı (Resolution = 5):", len(communs_2))
    print("En büyük communities boyutu (Resolution = 5):", max_len_2)
    print("Modularity (Resolution = 5):", communs_2_modularity)

    # Dosyaya yazma
    with open(f'datas/{file_name}_topologic_analiz.txt', 'w') as f:
        f.write("Node Sayısı: {}\n".format(node_count))
        f.write("Link Sayısı: {}\n".format(link_count))
        f.write("Density: {}\n".format(density))
        f.write("Ortalama Derece: {}\n".format(average_degree))
        f.write("Maksimum Derece: {}\n".format(max_degree))
        f.write("Minimum Derece: {}\n".format(min_degree))
        #f.write("Diameter: {}\n".format(diameter))
        f.write("İzole Düğüm Sayısı: {}\n".format(isolated_nodes_count))
        f.write("Bağlı Bileşen Sayısı: {}\n".format(connected_components_count))
        f.write("Transitivity: {}\n".format(transitivity))
        f.write("En büyük dereceye sahip ilk 5 düğüm: {}\n".format(top_5_nodes))
        f.write("Communities sayısı (Resolution = 1): {}\n".format(len(communs_1)))
        f.write("En büyük communities boyutu (Resolution = 1): {}\n".format(max_len_1))
        f.write("Communities sayısı (Resolution = 3): {}\n".format(len(communs_1_5)))
        f.write("En büyük communities boyutu (Resolution = 3): {}\n".format(max_len_1_5))
        f.write("Communities sayısı (Resolution = 5): {}\n".format(len(communs_2)))
        f.write("En büyük communities boyutu (Resolution = 5): {}\n".format(max_len_2))




def drawe_graph_plots(G, file_name, graph_name):
    # louvain algoritması 
    communs_1 = nx.community.louvain_communities(G, resolution=1 )
    communs_1_5 = nx.community.louvain_communities(G, resolution=3 )
    communs_2 = nx.community.louvain_communities(G, resolution=5 )
    community_sizes_1 = [len(community) for community in communs_1]
    community_sizes_1_5 = [len(community) for community in communs_1_5]
    community_sizes_2 = [len(community) for community in communs_2]

    # Degree distribution hesaplayalım
    degrees = list(dict(G.degree()).values())

    # Degree Histogram
    plt.figure(figsize=(33, 7))

    plt.subplot(1, 3, 1)
    plt.hist(degrees, bins=np.arange(min(degrees), max(degrees) + 1, 1) / 2, edgecolor='skyblue')  
    plt.title(f'{graph_name}, Degree Distribution (Histogram)')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')

    # Degree Logaritmik ölçekte histogram
    plt.subplot(1, 3, 2)
    plt.hist(degrees, bins=np.arange(min(degrees), max(degrees) + 1, 1) / 2, edgecolor='skyblue')  
    plt.yscale('log')
    plt.xscale('log')
    plt.title(f'{graph_name}, Degree Distribution (Histogram)')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')

    # Degree Logaritmik ölçekte olasılık yoğunluk plotu
    plt.subplot(1, 3, 3)
    sns.distplot(degrees, hist = False, kde = True, rug = False,
                color = 'darkblue')
    plt.title(f'{graph_name}, Degree Distribution (Probability Density Plot)')
    plt.xlabel('Degree')
    plt.ylabel('Probability Density')

    plt.savefig(f'datas/{file_name}_degree_plot.png')
    plt.tight_layout()
    plt.show()


    # Louvain commun Histogram
    plt.figure(figsize=(33, 7))

    plt.subplot(1, 3, 1)
    plt.hist(community_sizes_1,  edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 1)')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    plt.hist(community_sizes_1_5,  edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 3)')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)
    plt.hist(community_sizes_2,  edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 5)')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.savefig(f'datas/{file_name}_louvain_commun_size_histogram_plot.png')
    plt.tight_layout()
    plt.show()


    # Louvain commun Histogram log scale
    plt.figure(figsize=(33, 7))

    plt.subplot(1, 3, 1)
    plt.hist(community_sizes_1, edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 1)')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    plt.hist(community_sizes_1_5, edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 3)')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)
    plt.hist(community_sizes_2,  edgecolor='skyblue')  
    plt.title('Louvain Commun Size Distribution (Resolution = 5)')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Size')
    plt.ylabel('Frequency')

    plt.savefig(f'datas/{file_name}_louvain_commun_size_histogram_scale_plot.png')
    plt.tight_layout()
    plt.show()


def find_sub_graph_with_louvain_communities(G, resolution=1 ):
    # Louvain algoritması ile toplulukları bul
    communs = nx.community.louvain_communities(G, resolution=resolution )
    modularity = nx.community.modularity(G=G, communities=communs)
    
    # Her topluluk için alt graf oluştur ve betweenness centrality hesapla
    community_subgraphs = []
    for  commun in communs:

        # Topluluğa ait alt grafi oluştur
        community_subgraph = G.subgraph(commun)
        community_subgraphs.append(community_subgraph)
    return community_subgraphs, modularity


def create_centrality_files(G, file_name):

    # Betweenness centrality'yi hesaplayın
    betweenness = nx.betweenness_centrality(G, normalized=True, endpoints=False)
    betweenness_dict = {}
    # Sonucu bir dosyaya kaydet
    with open(f'datas/{file_name}_betweenness_centrality.csv', 'w', newline='') as csvfile:
        fieldnames = ['Node', 'Betweenness Centrality']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for node, centrality in betweenness.items():
            writer.writerow({'Node': node, 'Betweenness Centrality': centrality})
            betweenness_dict[node] = centrality

    # Closeness centrality'yi hesaplayın
    closeness = nx.closeness_centrality(G)
    closeness_dict = {}
    # Sonucu bir dosyaya kaydet
    with open(f'datas/{file_name}_closeness_centrality.csv', 'w', newline='') as csvfile:
        fieldnames = ['Node', 'Closeness Centrality']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for node, centrality in closeness.items():
            writer.writerow({'Node': node, 'Closeness Centrality': centrality})
            closeness_dict[node] = centrality

    # Eigenvector centrality'yi hesaplayın
    eigenvector_centrality = nx.eigenvector_centrality(G)
    eigenvector_dict = {}
    # Sonucu bir dosyaya kaydet
    with open(f'datas/{file_name}_eigenvector_centrality.csv', 'w', newline='') as csvfile:
        fieldnames = ['Node', 'Eigenvector Centrality']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for node, centrality in eigenvector_centrality.items():
            writer.writerow({'Node': node, 'Eigenvector Centrality': centrality})
            eigenvector_dict[node] = centrality
    
    return {"betweenness": betweenness_dict, "closeness":closeness_dict, "eigenvector":eigenvector_dict}

def create_centrality(G):

    # Betweenness centrality'yi hesaplayın
    betweenness = nx.betweenness_centrality(G, normalized=True, endpoints=False)
    betweenness_dict = {}
    # Sonucu bir dosyaya kaydet
    for node, centrality in betweenness.items():
        betweenness_dict[node] = centrality

    # Closeness centrality'yi hesaplayın
    closeness = nx.closeness_centrality(G)
    closeness_dict = {}
    for node, centrality in closeness.items():
        closeness_dict[node] = centrality

    # Eigenvector centrality'yi hesaplayın
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=10000)
    eigenvector_dict = {}
    for node, centrality in eigenvector_centrality.items():
        eigenvector_dict[node] = centrality

    return {"betweenness": betweenness_dict, "closeness":closeness_dict, "eigenvector":eigenvector_dict}


def calculate_pearsonr_with_csv(degree_csv_file_name, colum_1_name, colum_2_name ,souce_vector, target_vector):
    # CSV dosyasını oku
    df = pd.read_csv(degree_csv_file_name)

    # Node ve Eigenvector Centrality sütunlarını al
    node_sutun = df[colum_1_name]
    eigenvector_sutun = df[colum_2_name]

    # Node ve Eigenvector Centrality değerlerini birleştirerek bir sözlük oluştur
    node_eigenvector_map = dict(zip(node_sutun, eigenvector_sutun))

    degre_souce_vector = np.array([])
    degre_target_vector = np.array([])

    for souce in souce_vector:
        degre_souce_vector = np.append(degre_souce_vector, node_eigenvector_map[souce])

    for target in target_vector:
        degre_target_vector = np.append(degre_target_vector, node_eigenvector_map[target])

    korelasyon_katsayisi, p_degeri = pearsonr(degre_souce_vector, degre_target_vector)

    return(korelasyon_katsayisi, p_degeri)


def calculate_pearsonr_with_map(degre_map, souce_vector, target_vector):

    degre_souce_vector = np.array([])
    degre_target_vector = np.array([])
    
    for souce in souce_vector:
        degre_souce_vector = np.append(degre_souce_vector, degre_map[souce])

    for target in target_vector:
        degre_target_vector = np.append(degre_target_vector, degre_map[target])

    korelasyon_katsayisi, p_degeri = pearsonr(degre_souce_vector, degre_target_vector)

    return(korelasyon_katsayisi, p_degeri)

