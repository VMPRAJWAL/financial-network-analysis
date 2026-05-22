import networkx as nx

def simulate_bank_failure(G, failed_bank, capital_threshold=0.3):
    """
    Simulates the cascading effect of a bank failure.
    If a bank fails, institutions heavily reliant on it (losing > capital_threshold of inflow) may also fail.
    """
    G_sim = G.copy()
    initial_nodes = set(G_sim.nodes())
    
    if failed_bank not in G_sim:
        return G_sim, []
        
    failed_nodes = [failed_bank]
    nodes_to_process = [failed_bank]
    
    # Calculate baseline inflows before failure
    baseline_inflow = {}
    for node in G_sim.nodes():
        baseline_inflow[node] = sum([d['weight'] for u, v, d in G_sim.in_edges(node, data=True)])
        
    while nodes_to_process:
        current_failure = nodes_to_process.pop(0)
        
        # Find neighbors that might be affected
        affected_neighbors = list(G_sim.successors(current_failure))
        
        # Remove the failed bank from the network
        G_sim.remove_node(current_failure)
        
        for neighbor in affected_neighbors:
            if neighbor in G_sim.nodes(): # If not already failed
                # Calculate new inflow
                new_inflow = sum([d['weight'] for u, v, d in G_sim.in_edges(neighbor, data=True)])
                
                # If the loss is greater than the threshold of their original inflow, they fail
                loss_ratio = 1.0 - (new_inflow / baseline_inflow[neighbor]) if baseline_inflow[neighbor] > 0 else 0
                
                if loss_ratio >= capital_threshold:
                    failed_nodes.append(neighbor)
                    nodes_to_process.append(neighbor)
                    
    return G_sim, failed_nodes
