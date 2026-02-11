import os
import pandas as pd
from google.cloud import bigquery
from pathlib import Path

# Paths 
# Now we save data inside the package folder or a specific 'data' folder
# Be careful: inside Docker, files saved to non-mounted paths disappear on restart
BASE_DIR = Path(__file__).resolve().parent
LOCAL_FILE = BASE_DIR / "data_cache.csv"

def get_data(brand="Louis Vuitton"):
    if LOCAL_FILE.exists():
        print(f"Loading from local file {LOCAL_FILE}...")
        return pd.read_csv(LOCAL_FILE)

    print("Local file missing. Connecting to BigQuery...")
    
    # 2. AUTO-AUTHENTICATION
    try:
        client = bigquery.Client() 
    except Exception as e:
        print("❌ Auth failed. Did you mount the secrets in Docker?")
        raise e

    query = f"""
        SELECT *
        FROM `edhec-01.luxurydata2502.price-monitoring-2022`
        WHERE brand = '{brand}'
    """
    
    df = client.query(query).to_dataframe()
    
    # 3. Save copy
    print(f"Saving to {LOCAL_FILE}...")
    df.to_csv(LOCAL_FILE, index=False)
    
    return df

if __name__ == "__main__":
    df = get_data()
    print(df.head())