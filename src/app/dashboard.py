import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd
import sqlite3

# Local project imports
from src.visualization.charts import (
    plot_boe_2021_2023_trajectory, 
    plot_cross_institution_comparison,
    get_communication_narrative_table,
    plot_inflation_shock,
    plot_nominal_rates,
    plot_real_rates
)

DB_PATH = Path('data/processed/macroverba.db')
STANCE_PATH = Path('data/processed/policy_stance_index.csv')
MACRO_PATH = Path('data/processed/macro_indicators_2020_2024.csv')

st.set_page_config(page_title="MacroVerba", layout="wide")
st.title("MacroVerba: Comparative Monetary Policy")

# Data
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    db_df = pd.read_sql_query("SELECT institution, title, url FROM documents", conn)
    conn.close()
    
    stance_df = pd.read_csv(STANCE_PATH) if STANCE_PATH.exists() else pd.DataFrame()
    macro_df = pd.read_csv(MACRO_PATH) if MACRO_PATH.exists() else pd.DataFrame()
    
    if not macro_df.empty:
        macro_df['Date'] = pd.to_datetime(macro_df['Date'])
        
    return db_df, stance_df, macro_df

db_df, stance_df, macro_df = load_data()

# Sidebar Filters
st.sidebar.header("Filter by Institution")
if not db_df.empty:
    banks = db_df['institution'].unique().tolist()
    selected_banks = st.sidebar.multiselect("Select Central Banks", banks, default=banks)
    filtered_db = db_df[db_df['institution'].isin(selected_banks)]
    st.sidebar.metric("Total Documents Tracked", len(filtered_db))
else:
    st.warning("Database is empty. Run the scrapers first.")
    selected_banks = []

# 2021-2023 RESEARCH NOTE UI
st.header("The 2021–23 Inflation Episode")
st.markdown("A comparative analysis of macroeconomic shocks and central bank communication responses.")

# Macroeconomic Reality
if not macro_df.empty and selected_banks:
    # Map institutions to countries for filtering
    inst_to_country = {"Fed": "United States", "BoE": "United Kingdom", "RBI": "India"}
    selected_countries = [inst_to_country[b] for b in selected_banks if b in inst_to_country]
    
    filtered_macro = macro_df[macro_df['Institution'].isin(selected_banks)]
    
    tab1, tab2, tab3 = st.tabs(["1. The Common Shock", "2. Divergent Responses", "3. The Real Policy Stance"])
    
    with tab1:
        st.plotly_chart(plot_inflation_shock(macro_df[macro_df['Country'].isin(selected_countries)]), use_container_width=True)
    with tab2:
        st.plotly_chart(plot_nominal_rates(filtered_macro), use_container_width=True)
    with tab3:
        st.plotly_chart(plot_real_rates(filtered_macro), use_container_width=True)
        st.markdown("*Note: Negative real rates indicate highly accommodative monetary policy despite rising inflation.*")

st.divider()

# Central Bank Communication
if not stance_df.empty and selected_banks:
    filtered_stance = stance_df[stance_df['Institution'].isin(selected_banks)]
    
    st.subheader("4 & 5. Central Bank Communication & Stance")
    st.markdown("Quantifying the shift in monetary policy rhetoric. *(> 0 indicates Hawkish, < 0 indicates Dovish)*")
    
    # Interactive Plotly Visualizations
    col1, col2 = st.columns(2)
    with col1:
        boe_fig = plot_boe_2021_2023_trajectory(filtered_stance)
        if boe_fig:
            st.plotly_chart(boe_fig, use_container_width=True)
    with col2:
        comp_fig = plot_cross_institution_comparison(filtered_stance)
        if comp_fig:
            st.plotly_chart(comp_fig, use_container_width=True)

    # Comparative Timeline Matrix
    st.markdown("#### Comparative Communication Matrix (2021–2023)")
    narrative_df = get_communication_narrative_table()
    
    active_bank_names = []
    if "RBI" in selected_banks: active_bank_names.append("Reserve Bank of India (RBI)")
    if "Fed" in selected_banks: active_bank_names.append("US Federal Reserve")
    if "BoE" in selected_banks: active_bank_names.append("Bank of England (BoE)")
        
    filtered_narrative = narrative_df[narrative_df["Central Bank"].isin(active_bank_names)]
    st.dataframe(filtered_narrative, use_container_width=True, hide_index=True)

# Document Database Explorer
if not db_df.empty and selected_banks:
    st.divider()
    with st.expander("Explore Raw Database Documents & Metadata"):
        st.dataframe(filtered_db, use_container_width=True, hide_index=True)