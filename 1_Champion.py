"""
pages/1_Champion.py — Chat standard avec l'Agent Champion (Agent 2 — Sémantique)
"""

import streamlit as st
from utils import call_agent_2
from style import inject_css, agent2_header, status_badge

# ─────────────────────────────────────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agent Sémantique",
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

    # Métriques de session
    nb_messages = len([m for m in st.session_state.get("messages_champion", []) if m["role"] == "user"])
    st.metric("Questions posées", nb_messages)

    st.divider()

    if st.button("Effacer l'historique", use_container_width=True):
        st.session_state.messages_champion = []
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Initialisation de l'historique dédié
# ─────────────────────────────────────────────────────────────────────────────
if "messages_champion" not in st.session_state:
    st.session_state.messages_champion = []

# ─────────────────────────────────────────────────────────────────────────────
# En-tête
# ─────────────────────────────────────────────────────────────────────────────
agent2_header()
st.markdown("&nbsp;", unsafe_allow_html=True)
st.title("Agent Sémantique")
st.markdown(
    '<p class="page-subtitle">Cet agent exploite le contrat sémantique complet : '
    'noms métier, glossaire Dataplex, règles d\'exclusion et exemples de requêtes.</p>',
    unsafe_allow_html=True,
)
status_badge("Production Ready")
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Historique de conversation
# ─────────────────────────────────────────────────────────────────────────────
for msg in st.session_state.messages_champion:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────────────────────────
# Input utilisateur
# ─────────────────────────────────────────────────────────────────────────────
user_query = st.chat_input("Posez votre question en langage naturel…")

if user_query:
    st.session_state.messages_champion.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Génération de la requête…"):
            response = call_agent_2(user_query)
        st.markdown(response)

    st.session_state.messages_champion.append({"role": "assistant", "content": response})
