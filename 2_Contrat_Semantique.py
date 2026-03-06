"""
pages/2_Contrat_Semantique.py — Vue globale des contrats sémantiques par table
Liste toutes les tables du dataset ; chaque ligne se déploie pour afficher le contrat complet.
Note : Streamlit interdit les expanders imbriqués → on utilise st.tabs à l'intérieur.
"""

import streamlit as st
import yaml

from utils import fetch_all_contracts
from style import inject_css, status_badge

# ─────────────────────────────────────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Contrat sémantique",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — navigation
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    st.page_link("app.py",                             label="Arène")
    st.page_link("pages/1_Champion.py",                label="Agent Sémantique")
    st.page_link("pages/2_Contrat_Semantique.py",      label="Contrat sémantique")

# ─────────────────────────────────────────────────────────────────────────────
# En-tête
# ─────────────────────────────────────────────────────────────────────────────
st.title("Contrat sémantique")
st.markdown(
    '<p class="page-subtitle">Liste des tables du dataset. '
    'Cliquez sur une table pour afficher son contrat complet.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Chargement des contrats
# ─────────────────────────────────────────────────────────────────────────────
try:
    contracts = fetch_all_contracts()
except Exception as e:
    st.error(f"Impossible de charger les contrats : {e}")
    st.stop()

if not contracts:
    st.warning("Aucun contrat disponible.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Métriques globales du dataset
# ─────────────────────────────────────────────────────────────────────────────
total_rows = sum(
    e["contract"].get("customProperties", {}).get("bigquery", {}).get("numRows", 0) or 0
    for e in contracts
)
first_srv = next(iter((contracts[0]["contract"].get("servers") or {}).values()), {})

m1, m2, m3, m4 = st.columns(4)
m1.metric("Projet",         first_srv.get("project", "—"))
m2.metric("Région",         first_srv.get("location", "—"))
m3.metric("Tables",         len(contracts))
m4.metric("Lignes totales", f"{total_rows:,}" if total_rows else "—")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Liste des tables — expander par table, tabs à l'intérieur
# ─────────────────────────────────────────────────────────────────────────────
for entry in contracts:
    contract = entry["contract"]
    yaml_str = entry["yaml_str"]
    info     = contract.get("info", {})
    servers  = contract.get("servers") or {}
    bq_srv   = next(iter(servers.values()), {})
    bq_props = contract.get("customProperties", {}).get("bigquery", {})
    sla_def  = contract.get("sla", {})
    status   = contract.get("status", "active")

    nb_rows  = bq_props.get("numRows")
    all_cols = [c for t in contract.get("schema", {}).get("tables", []) for c in t.get("columns", [])]
    nb_cols  = len(all_cols)
    freshness = sla_def.get("freshness", {}).get("threshold", "—")

    # Label de l'expander
    rows_label = f"{nb_rows:,} lignes" if isinstance(nb_rows, int) else ""
    expander_label = "  ·  ".join(filter(None, [
        info.get("title", entry["table"]),
        bq_srv.get("dataset", ""),
        f"{nb_cols} colonnes",
        rows_label,
    ]))

    with st.expander(expander_label, expanded=False):

        # En-tête de la table
        col_h, col_b = st.columns([5, 1])
        with col_h:
            st.markdown(
                f"**`{bq_srv.get('project', '')}`**.**`{bq_srv.get('dataset', '')}`**.**`{entry['table']}`**"
            )
            st.markdown(
                f'<p class="page-subtitle">{info.get("description", "")}</p>',
                unsafe_allow_html=True,
            )
        with col_b:
            status_badge(status.upper())

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Lignes",      f"{nb_rows:,}" if isinstance(nb_rows, int) else "—")
        mc2.metric("Colonnes",    nb_cols)
        mc3.metric("Fraîcheur",   freshness)
        mc4.metric("Mise à jour", (bq_props.get("modified") or "—")[:10])

        st.markdown("---")

        # Déterminer les onglets disponibles
        glossary = (
            contract.get("customProperties", {})
                    .get("dataplex", {})
                    .get("glossary", [])
        )
        sample_queries = (
            contract.get("customProperties", {})
                    .get("ai", {})
                    .get("sampleQueries", [])
        )
        quality_spec = contract.get("quality", {}).get("specification", "")

        tab_labels = ["Colonnes"]
        if glossary:       tab_labels.append("Glossaire")
        if sample_queries: tab_labels.append(f"Requêtes ({len(sample_queries)})")
        if quality_spec or sla_def: tab_labels.append("Qualité & SLA")
        tab_labels.append("YAML brut")

        tabs = st.tabs(tab_labels)
        tab_idx = 0

        # ── Tab : Colonnes ───────────────────────────────────────────────
        with tabs[tab_idx]:
            tab_idx += 1
            if all_cols:
                rows_data = [
                    {
                        "Nom physique": c.get("name", ""),
                        "Nom métier":   c.get("businessName", "—"),
                        "Type":         c.get("physicalType", c.get("type", "")),
                        "Nullable":     "Oui" if c.get("isNullable") else "Non",
                        "Description":  c.get("description", ""),
                    }
                    for c in all_cols
                ]
                st.dataframe(rows_data, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune colonne définie.")

        # ── Tab : Glossaire ──────────────────────────────────────────────
        if glossary:
            with tabs[tab_idx]:
                tab_idx += 1
                for term_entry in glossary:
                    term       = term_entry.get("term", "")
                    definition = term_entry.get("definition", "")
                    synonyms   = term_entry.get("synonyms", [])
                    related    = term_entry.get("relatedTerms", [])
                    category   = term_entry.get("category", "")
                    examples   = term_entry.get("examples", [])

                    # Titre du terme
                    cat_label = f"  —  {category.capitalize()}" if category else ""
                    st.markdown(f"**{term}**{cat_label}")
                    st.markdown(definition)

                    col_syn, col_rel = st.columns(2)
                    with col_syn:
                        if synonyms:
                            st.markdown('<p class="section-label">Synonymes</p>', unsafe_allow_html=True)
                            st.markdown("  ·  ".join(f"`{s}`" for s in synonyms))
                    with col_rel:
                        if related:
                            st.markdown('<p class="section-label">Termes associés</p>', unsafe_allow_html=True)
                            st.markdown("  ·  ".join(f"`{r}`" for r in related))
                    if examples:
                        st.markdown('<p class="section-label">Exemples</p>', unsafe_allow_html=True)
                        st.markdown("  ·  ".join(str(e) for e in examples))

                    st.markdown("---")

        # ── Tab : Requêtes SQL ───────────────────────────────────────────
        if sample_queries:
            with tabs[tab_idx]:
                tab_idx += 1
                for i, sq in enumerate(sample_queries, start=1):
                    question    = sq.get("question", "")
                    sql         = sq.get("sql", "")
                    explanation = sq.get("explanation", "")
                    terms_used  = sq.get("glossaryTermsUsed", [])

                    st.markdown(f"**Exemple {i}**")
                    st.markdown(question)
                    st.code(sql, language="sql")
                    if explanation:
                        st.markdown(
                            f'<p class="section-label">Explication</p><p>{explanation}</p>',
                            unsafe_allow_html=True,
                        )
                    if terms_used:
                        st.markdown('<p class="section-label">Termes utilisés</p>', unsafe_allow_html=True)
                        st.markdown("  ·  ".join(f"`{t}`" for t in terms_used))
                    st.markdown("---")

        # ── Tab : Qualité & SLA ──────────────────────────────────────────
        if quality_spec or sla_def:
            with tabs[tab_idx]:
                tab_idx += 1
                col_q, col_s = st.columns(2)
                with col_q:
                    if quality_spec:
                        st.markdown('<p class="section-label">Qualité (SodaCL)</p>', unsafe_allow_html=True)
                        st.code(quality_spec, language="yaml")
                with col_s:
                    if sla_def:
                        st.markdown('<p class="section-label">SLA</p>', unsafe_allow_html=True)
                        s1, s2 = st.columns(2)
                        s1.metric("Intervalle",    sla_def.get("interval", "—").capitalize())
                        s2.metric("Disponibilité", f"{sla_def.get('availability', {}).get('percentage', '—')} %")
                        st.markdown(
                            f'<p class="page-subtitle">'
                            f'{sla_def.get("freshness", {}).get("description", "")}</p>',
                            unsafe_allow_html=True,
                        )

        # ── Tab : YAML brut ──────────────────────────────────────────────
        with tabs[tab_idx]:
            st.code(yaml_str, language="yaml")
