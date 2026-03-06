"""
style.py — Feuille de style CSS partagée (thème dark professionnel)
Importer inject_css() en tête de chaque page Streamlit.
"""

import streamlit as st


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & variables ─────────────────────────────────────────── */
:root {
    --bg-base:       #0e1117;
    --bg-surface:    #161b27;
    --bg-elevated:   #1e2535;
    --bg-hover:      #252d40;
    --border:        #2a3347;
    --border-subtle: #1e2535;

    --text-primary:  #e8eaf0;
    --text-secondary:#8b95aa;
    --text-muted:    #505a70;

    --accent-blue:   #4f8ef7;
    --accent-violet: #8b5cf6;
    --accent-green:  #34d399;
    --accent-amber:  #f59e0b;

    --agent1-color:  #4f8ef7;
    --agent2-color:  #8b5cf6;

    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;

    --font-sans: 'Inter', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

/* ── Base ──────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-base) !important;
    font-family: var(--font-sans) !important;
}

[data-testid="stHeader"] {
    background-color: var(--bg-base) !important;
    border-bottom: 1px solid var(--border-subtle);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
}

/* ── Typographie ───────────────────────────────────────────────── */
h1 {
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.25rem !important;
}
h2 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
}
h3 {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
p, li, td, th {
    color: var(--text-secondary) !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
}
code {
    font-family: var(--font-mono) !important;
    font-size: 0.83rem !important;
    background: var(--bg-elevated) !important;
    color: var(--accent-blue) !important;
    padding: 2px 6px !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
}

/* ── Divider ───────────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Inputs ────────────────────────────────────────────────────── */
[data-testid="stChatInput"] textarea {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(79,142,247,0.15) !important;
}

/* ── Chat messages ─────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* ── Boutons ────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 1rem !important;
    transition: background 0.15s, border-color 0.15s;
}
[data-testid="stButton"] > button:hover {
    background-color: var(--bg-hover) !important;
    border-color: var(--accent-blue) !important;
}

/* ── Expander ───────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
}
[data-testid="stExpander"] summary {
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    font-size: 0.92rem !important;
}

/* ── Métriques ─────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── DataFrames / Tables ────────────────────────────────────────── */
[data-testid="stDataFrame"], .stDataFrame, .stTable {
    background-color: var(--bg-surface) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}
thead tr th {
    background-color: var(--bg-elevated) !important;
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    border-bottom: 1px solid var(--border) !important;
}
tbody tr td {
    border-bottom: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
}
tbody tr:hover td {
    background-color: var(--bg-hover) !important;
}

/* ── Code blocks ────────────────────────────────────────────────── */
pre, [data-testid="stCode"] {
    background-color: #0d1117 !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.83rem !important;
}

/* ── Alertes / Info ─────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
}

/* ── Navigation auto Streamlit masquée (remplacée par nav custom) ──── */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* ── Scrollbar ──────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Classes utilitaires custom ─────────────────────────────────── */
.agent-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-agent1 {
    background: rgba(79,142,247,0.12);
    color: #4f8ef7;
    border: 1px solid rgba(79,142,247,0.25);
}
.badge-agent2 {
    background: rgba(139,92,246,0.12);
    color: #8b5cf6;
    border: 1px solid rgba(139,92,246,0.25);
}
.badge-status {
    background: rgba(52,211,153,0.1);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.2);
    padding: 2px 10px;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
}
.page-subtitle {
    color: #505a70;
    font-size: 0.9rem;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
}
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #505a70;
    margin-bottom: 0.5rem;
}
.left-border-blue {
    border-left: 3px solid var(--accent-blue);
    padding-left: 1rem;
    margin: 1rem 0;
}
.left-border-violet {
    border-left: 3px solid var(--accent-violet);
    padding-left: 1rem;
    margin: 1rem 0;
}
</style>
"""


def inject_css() -> None:
    """Injecte le CSS dark professionnel dans la page Streamlit courante."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def agent1_header() -> None:
    """Affiche le badge de l'Agent 1."""
    st.markdown(
        '<span class="agent-badge badge-agent1">Agent 1 — Schémas</span>',
        unsafe_allow_html=True,
    )


def agent2_header() -> None:
    """Affiche le badge de l'Agent 2."""
    st.markdown(
        '<span class="agent-badge badge-agent2">Agent 2 — Sémantique</span>',
        unsafe_allow_html=True,
    )


def status_badge(label: str) -> None:
    """Affiche un badge de statut (ex : Active)."""
    st.markdown(
        f'<span class="badge-status">{label}</span>',
        unsafe_allow_html=True,
    )
