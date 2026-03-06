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

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — basculer ici pour passer en mode production
# ─────────────────────────────────────────────────────────────────────────────

USE_MOCK = True  # True = données simulées | False = vrais appels (à implémenter)

# Chemin du fichier YAML de test (relatif à l'emplacement de utils.py)
_YAML_MOCK_PATH = os.path.join(os.path.dirname(__file__), "county_natality.yaml")

# URL de l'endpoint IA (sera utilisé quand USE_MOCK = False)
AGENT_1_ENDPOINT = "https://your-agent1-endpoint/v1/query"
AGENT_2_ENDPOINT = "https://your-agent2-endpoint/v1/query"


# ─────────────────────────────────────────────────────────────────────────────
# Agent 1 — Schémas uniquement
# ─────────────────────────────────────────────────────────────────────────────

def call_agent_1(query: str) -> str:
    """
    Appelle l'Agent 1 (schémas uniquement).

    En production, remplacer le bloc mock par :
        import requests
        response = requests.post(AGENT_1_ENDPOINT, json={"query": query}, timeout=30)
        return response.json()["sql"]
    """
    if USE_MOCK:
        time.sleep(2)
        return _mock_agent_1(query)

    # ── Production (à décommenter) ──
    # import requests
    # resp = requests.post(AGENT_1_ENDPOINT, json={"query": query}, timeout=30)
    # resp.raise_for_status()
    # return resp.json().get("answer", "")
    raise NotImplementedError("Mode production non configuré.")


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

    En production, remplacer le bloc mock par :
        import requests
        response = requests.post(AGENT_2_ENDPOINT, json={"query": query}, timeout=30)
        return response.json()["sql"]
    """
    if USE_MOCK:
        time.sleep(2)
        return _mock_agent_2(query)

    # ── Production (à décommenter) ──
    # import requests
    # resp = requests.post(AGENT_2_ENDPOINT, json={"query": query}, timeout=30)
    # resp.raise_for_status()
    # return resp.json().get("answer", "")
    raise NotImplementedError("Mode production non configuré.")


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


# ─────────────────────────────────────────────────────────────────────────────
# Contrat sémantique — chargement (mis en cache)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner="Chargement du contrat sémantique…")
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
        with open(_YAML_MOCK_PATH, "r", encoding="utf-8") as f:
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
    raise NotImplementedError("Mode production non configuré.")
