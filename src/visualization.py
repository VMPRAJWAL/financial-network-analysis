import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np

def plot_network_2d(G, title="Financial Transaction Network"):
    """Plots a 2D interactive network graph using Plotly."""
    # FIX: Prevent crash if graph is completely empty
    if G.number_of_nodes() == 0:
        return go.Figure()

    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    node_names = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        deg = G.degree(node)
        node_color.append(deg)
        
        in_edges = G.in_edges(node, data=True)
        in_deg = sum([d.get('weight', 0) for u, v, d in in_edges])
        
        node_text.append(f"{str(node)}<br>Connections: {deg}<br>Inflow: ₹{in_deg:,.2f}")
        
        name_parts = str(node).split()
        node_names.append(name_parts[0] if name_parts else str(node))
        
        size = deg * 2
        node_size.append(max(size, 10))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_names,
        textposition="bottom center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_size,
            color=node_color,
            # FIX: Updated Plotly 6.x syntax for colorbar
            colorbar=dict(thickness=15, title='Node Connections'), 
            line_width=2))
            
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
             )
    return fig

def plot_geospatial_network(G, meta_df):
    """Plots the network over a geographical map of Mysuru."""
    # Create lookup dictionaries for lat/lon
    lat_map = pd.Series(meta_df.lat.values, index=meta_df.name).to_dict()
    lon_map = pd.Series(meta_df.lon.values, index=meta_df.name).to_dict()
    
    edge_lats = []
    edge_lons = []
    
    for u, v in G.edges():
        if u in lat_map and v in lat_map:
            edge_lats.extend([lat_map[u], lat_map[v], None])
            edge_lons.extend([lon_map[u], lon_map[v], None])
            
    edge_trace = go.Scattermapbox(
        lat=edge_lats,
        lon=edge_lons,
        mode='lines',
        line=dict(width=1, color='rgba(150, 150, 150, 0.6)'),
        hoverinfo='none'
    )
    
    node_lats = []
    node_lons = []
    node_texts = []
    node_sizes = []
    
    degrees = dict(G.degree())
    
    for node in G.nodes():
        if node in lat_map:
            node_lats.append(lat_map[node])
            node_lons.append(lon_map[node])
            node_texts.append(f"{node}<br>Degree: {degrees[node]}")
            node_sizes.append(max(degrees[node] * 1.5, 8))
            
    node_trace = go.Scattermapbox(
        lat=node_lats,
        lon=node_lons,
        mode='markers',
        hoverinfo='text',
        text=node_texts,
        marker=dict(
            size=node_sizes,
            color=list(degrees.values()),
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Connections")
        )
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='Mysuru Financial Network (Geospatial View)',
        mapbox=dict(
            style="open-street-map",
            zoom=11.5,
            center=dict(lat=12.3100, lon=76.6400) # Mysuru center
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig