import networkx as nx
import pandas as pd

def build_network(df):
    """Builds a Directed Graph from the transaction DataFrame."""
    G = nx.DiGraph()
    
    # Group transactions by Source and Destination to aggregate amounts
    aggregated_df = df.groupby(['Source_Bank', 'Destination_Bank']).agg({
        'Transaction_Amount': 'sum',
        'Transaction_Count': 'sum',
        'Dependency_Score': 'mean',
        'Risk_Level': lambda x: pd.Series.mode(x)[0] if not x.empty else 'Low'
    }).reset_index()
    
    for _, row in aggregated_df.iterrows():
        G.add_edge(
            row['Source_Bank'], 
            row['Destination_Bank'], 
            weight=row['Transaction_Amount'],
            count=row['Transaction_Count'],
            dependency=row['Dependency_Score'],
            risk=row['Risk_Level']
        )
    return G

def get_network_stats(G):
    """Returns basic network statistics."""
    return {
        "Total Banks (Nodes)": G.number_of_nodes(),
        "Total Connections (Edges)": G.number_of_edges(),
        "Network Density": round(nx.density(G), 4),
        "Average Degree": round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2) if G.number_of_nodes() > 0 else 0
    }