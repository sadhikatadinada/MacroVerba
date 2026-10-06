import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(project_root)

import streamlit as st
from src.processing.nlp import get_clustered_documents

st.set_page_config(page_title="MacroVerba", page_icon="🏛️", layout="wide")
st.title("MacroVerba: Central Bank Intelligence")
st.markdown("An automated pipeline for standardizing and analyzing macroeconomic communication.")

@st.cache_data
def load_data():
    return get_clustered_documents()

df = load_data()

if df.empty:
    st.warning("No documents found. Run the scraper and database pipeline first.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", len(df))
    with col2:
        st.metric("Institutions Tracked", df["institution"].nunique())
    with col3:
        st.metric("Identified Topics", df["topic"].nunique())

    st.divider()

    st.subheader("Distribution of Central Bank Communication by Topic")
    topic_counts = df["topic"].value_counts()
    st.bar_chart(topic_counts)

    st.divider()

    st.subheader("Document Explorer")
    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])

    with filter_col1:
        institution_options = ["All Institutions"] + sorted(df["institution"].dropna().unique().tolist())
        selected_institution = st.selectbox("Filter by Institution:", institution_options)

    with filter_col2:
        topic_options = ["All Topics"] + sorted(df["topic"].dropna().unique().tolist())
        selected_topic = st.selectbox("Filter by Economic Topic:", topic_options)

    with filter_col3:
        search_query = st.text_input("Search titles by keyword (e.g., 'FOMC', 'Auction', 'Repo'):")

    filtered_df = df.copy()
    if selected_institution != "All Institutions":
        filtered_df = filtered_df[filtered_df["institution"] == selected_institution]

    if selected_topic != "All Topics":
        filtered_df = filtered_df[filtered_df["topic"] == selected_topic]

    if search_query:
        filtered_df = filtered_df[filtered_df["title"].str.contains(search_query, case=False, na=False)]

    display_cols = ["institution", "title", "topic", "url", "scraped_at"]
    st.dataframe(
        filtered_df[display_cols],
        column_config={
            "url": st.column_config.LinkColumn("Document Link"),
            "topic": st.column_config.TextColumn("Economic Classification"),
            "title": st.column_config.TextColumn("Document Title", width="large")
        },
        hide_index=True,
        use_container_width=True
    )