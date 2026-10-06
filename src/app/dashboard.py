import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(project_root)

import sqlite3
import pandas as pd
import streamlit as st
from config import PROCESSED_DATA_DIR

st.set_page_config(page_title="MacroVerba", page_icon="🏛️", layout="wide")
st.title("MacroVerba: Central Bank Intelligence")
st.markdown("An automated pipeline for standardizing and analyzing macroeconomic communication.")

@st.cache_data
def load_data():
    db_path = PROCESSED_DATA_DIR / "macroverba.db"
    if not db_path.exists():
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT institution, title, url, scraped_at FROM documents", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No documents found. Please run your web scraper first!")
else:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.metric(label="Total Documents", value=len(df))
        st.metric(label="Institutions Tracked", value=df['institution'].nunique())
        
    with col2:
        search_query = st.text_input("🔍 Search press releases by keyword (e.g., 'Auction', 'Repo', 'Bulletin'):")
        
        if search_query:
            filtered_df = df[df['title'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_df = df
            
        st.dataframe(
            filtered_df,
            column_config={
                "url": st.column_config.LinkColumn("Document Link")
            },
            hide_index=True,
            use_container_width=True
        )