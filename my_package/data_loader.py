import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path

# Paths
PATH = script_dir = Path(__file__).resolve()
ROOT = PATH.parent.parent

# Configuration
DATASET_ID = "luxurydata2502"
TABLE_ID = "price-monitoring-2022"
BRAND = "Louis Vuitton"

# Le fichier où on va sauvegarder une copie pour aller vite
LOCAL_FILE = f"data_{BRAND}.csv"

def get_data():
    if os.path.exists(LOCAL_FILE):
        print(f"Chargement depuis le fichier local {LOCAL_FILE}...")
        return pd.read_csv(LOCAL_FILE)

    print("Fichier local absent. Connexion à BigQuery...")
    
    key_path = ROOT / "gcp-key.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials)

    # La requête SQL pour ne prendre QUE ta marque
    query = f"""
        SELECT *
        FROM `edhec-01.luxurydata2502.price-monitoring-2022`
        WHERE brand = '{BRAND}'
    """
    
    # On télécharge et on convertit en DataFrame
    df = client.query(query).to_dataframe()
    
    # 3. On sauvegarde une copie pour la prochaine fois
    print(f"Sauvegarde dans {LOCAL_FILE}...")
    df.to_csv(LOCAL_FILE, index=False)
    
    return df

# --- Utilisation ---
df = get_data()
print(df.head())