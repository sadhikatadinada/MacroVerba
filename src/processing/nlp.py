import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.core.database import get_db_connection

TOPIC_NAMES = {
    0: "Liquidity & Money Markets (VRRR/Repo)",
    1: "Debt Management & Auctions (T-Bills/Securities)",
    2: "Central Bank Operations & Regulations"
}

def get_clustered_documents(n_clusters: int = 3) -> pd.DataFrame:
    """
    Loads documents from SQLite, applies TF-IDF and K-Means,
    and returns a DataFrame enriched with topic classifications.
    """
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT institution, title, url, content, scraped_at FROM documents WHERE content IS NOT NULL",
        conn
    )
    conn.close()

    if df.empty:
        return pd.DataFrame()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.85,
        token_pattern=r"(?u)\b[a-zA-Z]+\b"
    )
    tfidf_matrix = vectorizer.fit_transform(df["content"])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster_id"] = kmeans.fit_predict(tfidf_matrix)
    df["topic"] = df["cluster_id"].map(TOPIC_NAMES)

    return df