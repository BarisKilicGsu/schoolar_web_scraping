import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain

# Örnek bir graf oluşturalım
G = nx.karate_club_graph()

communs_1 = nx.community.louvain_communities(G, resolution=2 )

print(nx.community.modularity(G=G, communities=communs_1))