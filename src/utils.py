import pandas as pd
import base64
import os

def ensure_directories():
    """Ensure data and outputs directories exist."""
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)

def get_table_download_link(df, filename="data.csv", text="Download CSV"):
    """Generates a link allowing the data in a given panda dataframe to be downloaded."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" target="_blank">{text}</a>'
    return href