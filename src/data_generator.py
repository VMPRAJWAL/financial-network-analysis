import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Mysuru specific bank branches and approximate coordinates (Lat: 12.28 to 12.33, Lon: 76.60 to 76.68)
MYSURU_BANKS = [
    {"name": "SBI Mysore Main Branch", "lat": 12.3051, "lon": 76.6551},
    {"name": "Canara Bank Kuvempunagar", "lat": 12.2865, "lon": 76.6343},
    {"name": "HDFC Bank Vijayanagar", "lat": 12.3278, "lon": 76.6212},
    {"name": "ICICI Bank Nazarbad", "lat": 12.3082, "lon": 76.6668},
    {"name": "Axis Bank JP Nagar", "lat": 12.2750, "lon": 76.6500},
    {"name": "Karnataka Bank KD Road", "lat": 12.3167, "lon": 76.6432},
    {"name": "Union Bank Bannimantap", "lat": 12.3330, "lon": 76.6540},
    {"name": "Kotak Mahindra Gokulam", "lat": 12.3245, "lon": 76.6350},
    {"name": "Bank of Baroda Saraswathipuram", "lat": 12.3015, "lon": 76.6360},
    {"name": "IDFC First Bank Siddartha Layout", "lat": 12.3000, "lon": 76.6750},
    {"name": "Indian Bank Vontikoppal", "lat": 12.3200, "lon": 76.6400},
    {"name": "PNB TK Layout", "lat": 12.3060, "lon": 76.6250},
    {"name": "South Indian Bank KD Road", "lat": 12.3150, "lon": 76.6420},
    {"name": "Federal Bank Mysuru", "lat": 12.3110, "lon": 76.6500},
    {"name": "Yes Bank Saraswathipuram", "lat": 12.2990, "lon": 76.6355},
    {"name": "IndusInd Bank Kuvempunagar", "lat": 12.2850, "lon": 76.6330},
    {"name": "Canara Bank Hebbal", "lat": 12.3480, "lon": 76.6200},
    {"name": "Corporation Bank Jayalakshmipuram", "lat": 12.3190, "lon": 76.6280},
    {"name": "Vijaya Bank Ramakrishnanagar", "lat": 12.2880, "lon": 76.6250},
    {"name": "SBI Metagalli", "lat": 12.3500, "lon": 76.6400},
    {"name": "HDFC Bank Bogadi", "lat": 12.3000, "lon": 76.6100},
    {"name": "ICICI Bank Hunsur Road", "lat": 12.3100, "lon": 76.6150},
    {"name": "Axis Bank RTO Circle", "lat": 12.3030, "lon": 76.6450},
    {"name": "Karnataka Bank Chamundipuram", "lat": 12.2900, "lon": 76.6600},
    {"name": "Canara Bank Ittigegud", "lat": 12.3050, "lon": 76.6650},
    {"name": "SBI VV Mohalla", "lat": 12.3180, "lon": 76.6320},
    {"name": "UBI Rajiv Nagar", "lat": 12.3250, "lon": 76.6800},
    {"name": "BOI Shivarampet", "lat": 12.3090, "lon": 76.6530},
    {"name": "Central Bank Ashoka Road", "lat": 12.3120, "lon": 76.6580},
    {"name": "IOB Jayanagar", "lat": 12.2950, "lon": 76.6450}
]

def generate_financial_data(num_transactions=800, file_path="data/mysuru_financial_transactions.csv"):
    """Generates synthetic inter-bank transaction data for Mysuru banks."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    bank_names = [b["name"] for b in MYSURU_BANKS]
    data = []
    
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(num_transactions):
        source = random.choice(bank_names)
        destination = random.choice(bank_names)
        
        while source == destination:
            destination = random.choice(bank_names)
            
        # Log-normal distribution for realistic transaction amounts
        amount = round(np.random.lognormal(mean=12, sigma=1.5), 2)
        count = random.randint(1, 50)
        risk_score = round(random.uniform(0.1, 1.0), 2)
        
        if risk_score > 0.8:
            risk_level = "High"
        elif risk_score > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        dep_score = round((amount / 1000000) * risk_score, 4)
        tx_date = start_date + timedelta(days=random.randint(0, 365))
        
        data.append([
            source, destination, amount, risk_level, count, dep_score, tx_date.strftime("%Y-%m-%d")
        ])
        
    df = pd.DataFrame(data, columns=[
        "Source_Bank", "Destination_Bank", "Transaction_Amount", 
        "Risk_Level", "Transaction_Count", "Dependency_Score", "Transaction_Date"
    ])
    
    # Save network data
    df.to_csv(file_path, index=False)
    
    # Save node meta-data (coordinates)
    node_df = pd.DataFrame(MYSURU_BANKS)
    node_df.to_csv("data/mysuru_banks_meta.csv", index=False)
    
    return df, node_df