import streamlit as st
import pandas as pd
import os
import networkx as nx

# Import custom modules
from src.data_generator import generate_financial_data
from src.network_builder import build_network, get_network_stats
from src.visualization import plot_network_2d, plot_geospatial_network
from src.analysis import calculate_centrality, detect_communities
from src.risk_analysis import simulate_bank_failure
from src.utils import ensure_directories, get_table_download_link

# Set Page Config
st.set_page_config(page_title="Financial Network Analysis", layout="wide", page_icon="🏦")
ensure_directories()

# Initialize data paths
TX_DATA_PATH = "data/mysuru_financial_transactions.csv"
META_DATA_PATH = "data/mysuru_banks_meta.csv"

@st.cache_data
def load_data():
    if not os.path.exists(TX_DATA_PATH) or not os.path.exists(META_DATA_PATH):
        df, meta = generate_financial_data()
    else:
        df = pd.read_csv(TX_DATA_PATH)
        meta = pd.read_csv(META_DATA_PATH)
    return df, meta

# Sidebar Navigation
st.sidebar.title("🏦 Navigation")
app_mode = st.sidebar.radio("Select Module:", [
    "1. Home / Overview",
    "2. Dataset & Analytics",
    "3. Network Visualization",
    "4. Centrality Analysis",
    "5. Community Detection",
    "6. Systemic Risk Simulation",
    "7. Export Results"
])

# Load data to be used across pages
df, meta_df = load_data()
G = build_network(df)

if app_mode == "1. Home / Overview":
    st.title("Financial Network Analysis System")
    st.markdown("""
    Welcome to the **Financial Network Analysis System**. 
    
    This application simulates and analyzes the financial inter-bank transaction network for banking branches in **Mysuru, Karnataka**. 
    
    ### Features
    *   **Data Simulation:** Creates synthetic realistic banking transaction dependencies.
    *   **Network Visualization:** Interactive topological and geographical maps.
    *   **Centrality Metrics:** Identifies the "too big to fail" institutions (PageRank, Betweenness).
    *   **Systemic Risk Simulator:** Simulates economic collapse and cascading bank failures.
    *   **Community Detection:** Uses AI/Graph algorithms to find tightly clustered financial ecosystems.
    """)
    st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=1200&auto=format&fit=crop", caption="Banking Network Architecture")

elif app_mode == "2. Dataset & Analytics":
    st.title("Dataset & Ecosystem Dashboard")
    
    if st.button("Regenerate Synthetic Data"):
        generate_financial_data()
        st.success("New synthetic dataset generated for Mysuru branches!")
        st.cache_data.clear()
        st.rerun()

    # Dashboard Metrics
    stats = get_network_stats(G)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Banks", stats["Total Banks (Nodes)"])
    col2.metric("Total Transactions", df['Transaction_Count'].sum())
    col3.metric("Avg Transaction Volume", f"₹{df['Transaction_Amount'].mean():,.0f}")
    col4.metric("Network Density", stats["Network Density"])
    
    st.subheader("Raw Transaction Data")
    st.dataframe(df.head(100))
    st.markdown(get_table_download_link(df, "transactions.csv"), unsafe_allow_html=True)

elif app_mode == "3. Network Visualization":
    st.title("Network Visualization")
    tab1, tab2 = st.tabs(["2D Topological Network", "Mysuru Geographical Map"])
    
    with tab1:
        st.markdown("This view abstracts geographical constraints to show structural dependencies.")
        fig_2d = plot_network_2d(G)
        st.plotly_chart(fig_2d, use_container_width=True)
        
    with tab2:
        st.markdown("This map plots the actual geographical coordinates of the simulated Mysuru branches.")
        fig_map = plot_geospatial_network(G, meta_df)
        st.plotly_chart(fig_map, use_container_width=True)

elif app_mode == "4. Centrality Analysis":
    st.title("Centrality Analysis")
    st.markdown("""
    **Metrics Explained:**
    *   **Degree:** How many direct connections a bank has.
    *   **Betweenness:** The influence a bank has over the flow of money between others (the "bridge").
    *   **PageRank:** The overall importance of a bank based on the importance of banks connected to it.
    """)
    
    cent_df = calculate_centrality(G)
    st.dataframe(cent_df.style.background_gradient(cmap='Blues'))
    
    st.subheader("Top 5 Most Critical Institutions (PageRank)")
    st.bar_chart(cent_df.set_index('Bank')['PageRank Score'].head(5))

elif app_mode == "5. Community Detection":
    st.title("Community Detection (Clustering)")
    st.markdown("Identifies dense sub-groups of banks that trade heavily with each other using the Girvan-Newman / Modularity algorithm.")
    
    comm_df, communities = detect_communities(G)
    st.write(f"Detected **{len(communities)}** distinct financial communities.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(comm_df)
    with col2:
        # Pie chart of communities
        comm_counts = comm_df['Community'].value_counts()
        st.bar_chart(comm_counts)

elif app_mode == "6. Systemic Risk Simulation":
    st.title("Systemic Risk Simulation (Stress Testing)")
    st.markdown("Simulate the collapse of a specific bank and observe the cascading impact on the Mysuru financial ecosystem.")
    
    nodes = list(G.nodes())
    target_bank = st.selectbox("Select a Bank to Simulate Failure:", nodes)
    threshold = st.slider("Capital Loss Tolerance (%)", 10, 80, 30, help="If a bank loses this % of its inflow, it fails too.") / 100.0
    
    if st.button("Simulate Cascade Failure"):
        G_sim, failed_nodes = simulate_bank_failure(G, target_bank, capital_threshold=threshold)
        
        st.error(f"⚠️ Initial Failure: {target_bank}")
        if len(failed_nodes) > 1:
            st.warning(f"Cascading Effect: {len(failed_nodes) - 1} additional institutions collapsed due to dependency.")
            st.write(", ".join(failed_nodes[1:]))
        else:
            st.success("The network absorbed the shock. No cascading failures occurred.")
            
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Network Before Failure")
            st.plotly_chart(plot_network_2d(G, title="Original"), use_container_width=True)
        with col2:
            st.subheader("Network After Cascade")
            st.plotly_chart(plot_network_2d(G_sim, title="Post-Collapse"), use_container_width=True)

elif app_mode == "7. Export Results":
    st.title("Export Analysis & Reports")
    st.markdown("Download generated intelligence and tables.")
    
    cent_df = calculate_centrality(G)
    comm_df, _ = detect_communities(G)
    
    st.markdown(get_table_download_link(cent_df, "centrality_report.csv", "📥 Download Centrality Rankings CSV"), unsafe_allow_html=True)
    st.markdown(get_table_download_link(comm_df, "community_report.csv", "📥 Download Community Clusters CSV"), unsafe_allow_html=True)
    st.markdown(get_table_download_link(df, "raw_transactions.csv", "📥 Download Raw Transactions CSV"), unsafe_allow_html=True)