"""
app.py — Page principale : Arène A/B Test (Agent 1 vs Agent 2)
Lance l'application avec : streamlit run app.py
"""

import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import call_agent_1, call_agent_2
from style import inject_css, agent1_header, agent2_header

# ─────────────────────────────────────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A/B Test — Text-to-SQL",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    st.page_link("app.py",                             label="Arène")
    st.page_link("pages/1_Champion.py",                label="Agent Sémantique")
    st.page_link("pages/2_Contrat_Semantique.py",      label="Contrat sémantique")

    st.divider()

    st.markdown("### Agents")
    st.markdown(
        """
        **Agent 1 — Schémas**  
        Contexte : schéma physique des tables BigQuery uniquement.

        **Agent 2 — Sémantique**  
        Contexte : schémas + contrat sémantique (noms métier, glossaire, règles).
        """
    )

    st.divider()

    if st.button("Réinitialiser l'arène", use_container_width=True):
        st.session_state.messages_agent1 = []
        st.session_state.messages_agent2 = []
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Initialisation de l'état de session
# ─────────────────────────────────────────────────────────────────────────────
if "messages_agent1" not in st.session_state:
    st.session_state.messages_agent1 = []
if "messages_agent2" not in st.session_state:
    st.session_state.messages_agent2 = []

# ─────────────────────────────────────────────────────────────────────────────
# En-tête
# ─────────────────────────────────────────────────────────────────────────────
st.title("Arène — A/B Test Text-to-SQL")
st.markdown(
    '<p class="page-subtitle">Comparez en temps réel les deux agents sur la même question. '
    'Les requêtes sont exécutées en parallèle.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Colonnes et affichage de l'historique
# ─────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    agent1_header()
    st.markdown('<p class="section-label">Schéma physique uniquement</p>', unsafe_allow_html=True)
    for msg in st.session_state.messages_agent1:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

with col2:
    agent2_header()
    st.markdown('<p class="section-label">Schéma + contrat sémantique</p>', unsafe_allow_html=True)
    for msg in st.session_state.messages_agent2:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────────────────────────
# Input utilisateur
# ─────────────────────────────────────────────────────────────────────────────
user_query = st.chat_input("Posez votre question en langage naturel…")

if user_query:
    # Ajout de la question aux deux historiques
    st.session_state.messages_agent1.append({"role": "user", "content": user_query})
    st.session_state.messages_agent2.append({"role": "user", "content": user_query})

    with col1:
        with st.chat_message("user"):
            st.markdown(user_query)

    with col2:
        with st.chat_message("user"):
            st.markdown(user_query)

    # Appels parallèles — temps total = max(t1, t2) au lieu de t1 + t2
    results = {}
    with st.spinner("Les deux agents génèrent leur réponse…"):
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_a1 = executor.submit(call_agent_1, user_query)
            future_a2 = executor.submit(call_agent_2, user_query)
            for future in as_completed([future_a1, future_a2]):
                if future is future_a1:
                    results["agent1"] = future.result()
                else:
                    results["agent2"] = future.result()

    # Sauvegarde et affichage des réponses
    st.session_state.messages_agent1.append({"role": "assistant", "content": results["agent1"]})
    st.session_state.messages_agent2.append({"role": "assistant", "content": results["agent2"]})

    with col1:
        with st.chat_message("assistant"):
            st.markdown(results["agent1"])

    with col2:
        with st.chat_message("assistant"):
            st.markdown(results["agent2"])
