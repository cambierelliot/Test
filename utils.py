"""
utils.py — Logique métier de l'application A/B Test Text-to-SQL
Contient les fonctions d'appel aux agents et la récupération du contrat sémantique.

MODE MOCK : USE_MOCK = True
  → Les agents retournent des réponses SQL simulées.
  → Le contrat sémantique est chargé depuis un fichier YAML local.

MODE PRODUCTION (futur) : USE_MOCK = False
  → call_agent_1 / call_agent_2 : appels HTTP vers un endpoint IA.
  → fetch_all_contracts           : requête BigQuery sur _table_contract.
"""

import time
import os
import streamlit as st
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import google.auth

# Import de la configuration centralisée
from config import (
    USE_MOCK,
    PROJECT_ID,
    LOCATION,
    REASONING_ENGINE_ID,
    REASONING_ENGINE_ENDPOINT,
    MOCK_YAML_PATH,
    API_TIMEOUT,
    CACHE_TTL,
    BIGQUERY_DATASET,
)

# Pour différencier les agents, on peut utiliser des paramètres différents
# Agent 1 : sans contrat sémantique
# Agent 2 : avec contrat sémantique
AGENT_1_ENDPOINT = REASONING_ENGINE_ENDPOINT
AGENT_2_ENDPOINT = REASONING_ENGINE_ENDPOINT


# ─────────────────────────────────────────────────────────────────────────────
# Authentification Google Cloud
# ─────────────────────────────────────────────────────────────────────────────

def get_access_token() -> str:
    """
    Récupère un token d'accès pour l'authentification Google Cloud.
    Utilise les credentials par défaut (ADC - Application Default Credentials).
    """
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    credentials.refresh(Request())
    return credentials.token


# ─────────────────────────────────────────────────────────────────────────────
# Agent 1 — Schémas uniquement
# ─────────────────────────────────────────────────────────────────────────────

def call_agent_1(query: str) -> str:
    """
    Appelle l'Agent 1 (schémas uniquement).
    
    En mode production, interroge le Reasoning Engine sans contrat sémantique.
    """
    if USE_MOCK:
        time.sleep(2)
        return _mock_agent_1(query)

    # ── Production ──
    try:
                token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Payload pour l'agent 1 : format ADK
        payload = {
            "appName": "text_to_sql_agent",
            "userId": "streamlit_user",
            "sessionId": f"session_{int(time.time())}",
            "newMessage": {
                "role": "user",
                "parts": [
                    {"text": query}
                ]
            }
        }
        
        response = requests.post(
            AGENT_1_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        return _format_agent_response(query, result, agent_name="Agent 1")
        
    except Exception as e:
        return f"**Erreur lors de l'appel à l'Agent 1**\n\n```\n{str(e)}\n```"


def _mock_agent_1(query: str) -> str:
    """Réponse simulée de l'Agent 1 — SQL littéral basé sur les noms de colonnes bruts."""
    return f"""\
**Question :** {query}

**Requête SQL générée**

```sql
-- Agent 1 : traduction directe des noms de colonnes physiques
SELECT
    Year,
    County_of_Residence,
    SUM(Births)                       AS total_births,
    AVG(Ave_Age_of_Mother)            AS avg_mother_age,
    AVG(Ave_Birth_Weight_gms)         AS avg_birth_weight
FROM `nxs-tes-nxhmr-sbx-11462292.test_agent.county_natality`
GROUP BY Year, County_of_Residence
ORDER BY total_births DESC
LIMIT 20;
```

> Les colonnes sont utilisées telles que définies dans le schéma physique. \
Aucune règle métier (exclusions, aliases sémantiques) n'a été appliquée.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Agent 2 — Schémas + Couche sémantique
# ─────────────────────────────────────────────────────────────────────────────

def call_agent_2(query: str) -> str:
    """
    Appelle l'Agent 2 (schémas + couche sémantique).
    
    En mode production, interroge le Reasoning Engine avec contrat sémantique.
    """
    if USE_MOCK:
        time.sleep(2)
        return _mock_agent_2(query)

    # ── Production ──
    try:
                token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Payload pour l'agent 2 : format ADK
        payload = {
            "appName": "text_to_sql_agent_semantic",
            "userId": "streamlit_user",
            "sessionId": f"session_{int(time.time())}",
            "newMessage": {
                "role": "user",
                "parts": [
                    {"text": query}
                ]
            }
        }
        
        response = requests.post(
            AGENT_2_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        return _format_agent_response(query, result, agent_name="Agent 2")
        
    except Exception as e:
        return f"**Erreur lors de l'appel à l'Agent 2**\n\n```\n{str(e)}\n```"


def _mock_agent_2(query: str) -> str:
    """Réponse simulée de l'Agent 2 — SQL enrichi par les noms métier et le glossaire."""
    return f"""\
**Question :** {query}

**Requête SQL générée**

```sql
-- Agent 2 : enrichi par le contrat sémantique (noms métier, règles glossaire)
SELECT
    -- "Année de Naissance" (businessName de Year)
    EXTRACT(YEAR FROM Year)                  AS annee_naissance,

    -- "Comté de Résidence" (businessName de County_of_Residence)
    County_of_Residence                      AS comte_residence,

    -- "Naissances vivantes" : exclut mortinaissances per business rule
    SUM(Births)                              AS naissances_vivantes,

    -- "Âge Moyen de la Mère" (businessName de Ave_Age_of_Mother)
    ROUND(AVG(Ave_Age_of_Mother), 1)         AS age_moyen_mere,

    -- "Poids Moyen à la Naissance" en grammes (businessName de Ave_Birth_Weight_gms)
    ROUND(AVG(Ave_Birth_Weight_gms), 0)      AS poids_moyen_naissance_gms,

    -- "Âge Gestationnel Moyen (Estimation Obstétricale)" — méthode OE préférée au LMP
    ROUND(AVG(Ave_OE_Gestational_Age_Wks), 1) AS age_gestationnel_oe_semaines
FROM
    `nxs-tes-nxhmr-sbx-11462292.test_agent.county_natality`
GROUP BY
    annee_naissance,
    comte_residence
ORDER BY
    naissances_vivantes DESC
LIMIT 20;
```

> Les alias utilisent les **noms métier** définis dans le contrat sémantique. \
L'âge gestationnel est systématiquement calculé via la méthode OE (plus précise que LMP, \
conformément au glossaire Dataplex).
"""


def _format_agent_response(query: str, result: dict, agent_name: str) -> str:
    """
    Formate la réponse du Reasoning Engine pour l'affichage dans Streamlit.
    
    Args:
        query: La question posée par l'utilisateur
        result: La réponse JSON du Reasoning Engine
        agent_name: Nom de l'agent (pour le contexte)
    
    Returns:
        Réponse formatée en Markdown
    """
    # Adapter selon la structure réelle de la réponse du Reasoning Engine
    # Voici un exemple de structure possible :
    
    output = f"**Question :** {query}\n\n"
    
    # Extraire la requête SQL si disponible
    if "output" in result:
        response_data = result["output"]
        
        if isinstance(response_data, dict):
            sql_query = response_data.get("sql", response_data.get("query", ""))
            explanation = response_data.get("explanation", "")
            
            if sql_query:
                output += "**Requête SQL générée**\n\n"
                output += f"```sql\n{sql_query}\n```\n\n"
            
            if explanation:
                output += f"> {explanation}\n"
        else:
            # Si la réponse est une chaîne simple
            output += str(response_data)
    else:
        # Fallback : afficher toute la réponse
        output += f"```json\n{result}\n```"
    
    return output


# ─────────────────────────────────────────────────────────────────────────────
# Contrat sémantique — chargement (mis en cache)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=CACHE_TTL, show_spinner="Chargement du contrat sémantique…")
def fetch_all_contracts() -> list[dict]:
    """
    Renvoie la liste des contrats sémantiques parsés (un par table du dataset).

    En mode mock  : charge county_natality.yaml depuis le disque.
    En production : requête BigQuery sur la table _table_contract pour chaque table
                    du dataset, puis parse chaque YAML retourné.

    Structure de retour :
        [
          { "table": "county_natality", "yaml_str": "...", "contract": {...} },
          ...
        ]

    Production (à implémenter) :
        from google.cloud import bigquery
        client = bigquery.Client(project="nxs-tes-nxhmr-sbx-11462292")
        sql = '''
            SELECT table_name, contract_yaml
            FROM `nxs-tes-nxhmr-sbx-11462292.test_agent._table_contract`
        '''
        rows = list(client.query(sql))
        contracts = []
        for row in rows:
            import yaml
            contracts.append({
                "table": row["table_name"],
                "yaml_str": row["contract_yaml"],
                "contract": yaml.safe_load(row["contract_yaml"]),
            })
                return contracts
    """
    import yaml

    if USE_MOCK:
        time.sleep(0.5)  # latence simulée
        with open(MOCK_YAML_PATH, "r", encoding="utf-8") as f:
            yaml_str = f.read()
        contract = yaml.safe_load(yaml_str)
        return [
            {
                "table": "county_natality",
                "yaml_str": yaml_str,
                "contract": contract,
            }
        ]

    # ── Production ──
    try:
        from google.cloud import bigquery
        
        client = bigquery.Client(project=PROJECT_ID)
        sql = f'''
            SELECT table_name, contract_yaml
            FROM `{PROJECT_ID}.{BIGQUERY_DATASET}._table_contract`
        '''
        
        rows = list(client.query(sql))
        contracts = []
        
        for row in rows:
            import yaml
            contracts.append({
                "table": row["table_name"],
                "yaml_str": row["contract_yaml"],
                "contract": yaml.safe_load(row["contract_yaml"]),
            })
        
        return contracts
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des contrats depuis BigQuery : {e}")
        return []
