from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# --- CONFIGURATION ---
# Le fichier est juste à côté du script, donc on met juste le nom
key_path = "gcp-key.json"

print(f"1. Lecture de la clé : {key_path}")

try:
    # On s'authentifie avec TA clé
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # On crée le client (Ton projet 'BDSM' paie la facture de la requête)
    # Remplace 'ton-id-de-projet-bdsm' par l'ID exact qu'il y a dans ton fichier JSON (champ "project_id")
    # ou laisse le client le deviner depuis les credentials :
    client = bigquery.Client(credentials=credentials)
    
    print(f"2. Authentification réussie sur le projet : {client.project}")

    # --- LE TEST ---
    # On essaie de lire la table du PROF (Projet: edhec-01)
    query = """
        SELECT brand, count(*) as count
        FROM `edhec-01.luxurydata2502.price-monitoring-2022`
        GROUP BY brand
        LIMIT 20
    """
    
    print("3. Envoi de la requête au serveur...")
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    
    print("\n--- SUCCÈS ! VOICI DES DONNÉES ---")
    print(results)

except Exception as e:
    print("\n--- ERREUR ---")
    print(e)