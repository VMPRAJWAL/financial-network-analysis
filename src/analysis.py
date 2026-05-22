import networkx as nx
import pandas as pd

def calculate_centrality(G):
    """Calculates various centrality measures for the network."""
    # Degree Centrality
    deg_cen = nx.degree_centrality(G)
    
    # Betweenness Centrality
    bet_cen = nx.betweenness_centrality(G, weight='weight')
    
    # Closeness Centrality
    clo_cen = nx.closeness_centrality(G)
    
    # PageRank (handles directed well)
    pagerank = nx.pagerank(G, weight='weight')
    
    data = []
    for node in G.nodes():
        data.append({
            "Bank": node,
            "Degree Centrality": round(deg_cen.get(node, 0), 4),
            "Betweenness Centrality": round(bet_cen.get(node, 0), 4),
            "Closeness Centrality": round(clo_cen.get(node, 0), 4),
            "PageRank Score": round(pagerank.get(node, 0), 4)
        })
        
    return pd.DataFrame(data).sort_values(by="PageRank Score", ascending=False)

def detect_communities(G):
    """Detects communities using Girvan-Newman modularity based approach."""
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()
    
    # Using greedy modularity maximization
    communities = list(nx.community.greedy_modularity_communities(G_undirected))
    
    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = f"Community {i+1}"
            
    df = pd.DataFrame(list(community_map.items()), columns=['Bank', 'Community'])
    return df, communities