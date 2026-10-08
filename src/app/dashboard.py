import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Paths based on your config architecture
DB_PATH = Path('data/processed/macroverba.db')
STANCE_PATH = Path('data/processed/policy_stance_index.csv')

st.set_page_config(page_title="MacroVerba", layout="wide")
st.title("MacroVerba: Comparative Monetary Policy")

# Load Data
@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)
    db_df = pd.read_sql_query("SELECT institution, title, url FROM documents", conn)
    conn.close()
    
    if STANCE_PATH.exists():
        stance_df = pd.read_csv(STANCE_PATH)
    else:
        stance_df = pd.DataFrame()
        
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

# Policy Stance Visualization
if not stance_df.empty and selected_banks:
    st.subheader("Hawkish vs. Dovish Policy Stance (2021-2023)")
    st.markdown("*> 0 indicates Hawkish (Tightening), < 0 indicates Dovish (Accommodative)*")
    
    filtered_stance = stance_df[stance_df['Institution'].isin(selected_banks)]
    
    if not filtered_stance.empty:
        chart_data = filtered_stance.pivot_table(
            index='Title', 
            columns='Institution', 
            values='Net_Stance_Score'
        )
        st.bar_chart(chart_data)
        
        with st.expander("View Raw Stance Index Data"):
            st.dataframe(
                filtered_stance[['Institution', 'Title', 'Hawkish_Hits', 'Dovish_Hits', 'Net_Stance_Score']], 
                use_container_width=True
            )

# Raw Document Database
if not db_df.empty and selected_banks:
    st.divider()
    st.subheader("Document Database Explorer")
    st.dataframe(filtered_db, use_container_width=True)