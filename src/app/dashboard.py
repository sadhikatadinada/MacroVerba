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
    get_communication_narrative_table
)

DB_PATH = Path('data/processed/macroverba.db')
STANCE_PATH = Path('data/processed/policy_stance_index.csv')

st.set_page_config(page_title="MacroVerba", layout="wide")
st.title("MacroVerba: Comparative Monetary Policy")

# Data
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    db_df = pd.read_sql_query("SELECT institution, title, url FROM documents", conn)
    conn.close()
    
    stance_df = pd.read_csv(STANCE_PATH) if STANCE_PATH.exists() else pd.DataFrame()
    return db_df, stance_df

db_df, stance_df = load_data()

# Sidebar Filters
st.sidebar.header("Filter by Institution")
if not db_df.empty:
    banks = db_df['institution'].unique().tolist()
    selected_banks = st.sidebar.multiselect("Select Central Banks", banks, default=banks)
    filtered_db = db_df[db_df['institution'].isin(selected_banks)]
    st.sidebar.metric("Total Documents", len(filtered_db))
else:
    st.warning("Database is empty. Run the scrapers first.")
    selected_banks = []

# Policy Stance Visualizations & Communication Matrix
if not stance_df.empty and selected_banks:
    filtered_stance = stance_df[stance_df['Institution'].isin(selected_banks)]
    
    st.header("The 2021–23 Inflation Episode: Central Bank Communication")
    st.markdown("Quantifying the shift in monetary policy rhetoric in response to the global inflationary shock. *(> 0 indicates Hawkish, < 0 indicates Dovish)*")
    
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

    # Underlying Stance Scores
    with st.expander("View Underlying Communication Index Data"):
        st.dataframe(
            filtered_stance[['Institution', 'Title', 'Hawkish_Hits', 'Dovish_Hits', 'Net_Stance_Score']], 
            use_container_width=True, 
            hide_index=True
        )

    st.divider()

    # Comparative Timeline Table
    st.subheader("Central Bank Comparative Communication Matrix (2021–2023)")
    st.markdown("Side-by-side alignment of primary inflation drivers, policy actions, and rhetorical tone during key inflection points.")
    
    narrative_df = get_communication_narrative_table()
    
    # Filter matrix by selected central banks
    active_bank_names = []
    if "RBI" in selected_banks:
        active_bank_names.append("Reserve Bank of India (RBI)")
    if "Fed" in selected_banks:
        active_bank_names.append("US Federal Reserve")
    if "BoE" in selected_banks:
        active_bank_names.append("Bank of England (BoE)")
        
    filtered_narrative = narrative_df[narrative_df["Central Bank"].isin(active_bank_names)]
    st.dataframe(filtered_narrative, use_container_width=True, hide_index=True)

# Raw Document Database Explorer
if not db_df.empty and selected_banks:
    st.divider()
    st.subheader("Document Database Explorer")
    st.dataframe(filtered_db, use_container_width=True, hide_index=True)