import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.core.database import get_db_connection

def analyze_rbi_vocabulary():
    """Calculates TF-IDF to extract the most uniquely important terms per document."""
    print("Loading documents from database...")
    conn = get_db_connection()
    
    df = pd.read_sql_query("SELECT title, content FROM documents WHERE content IS NOT NULL", conn)
    conn.close()

    if df.empty:
        print("No documents found in the database.")
        return

    print(f"Analyzing {len(df)} documents with TF-IDF...\n")

    # Initialize TF-IDF Vectorizer
    # stop_words='english' removes 'the', 'is', 'at'
    # max_df=0.85 mathematically ignores words appearing in >85% of documents (e.g., "Reserve", "Bank")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.85)
    
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    feature_names = vectorizer.get_feature_names_out()
    
    for i in range(min(3, len(df))):
        print(f"Title: {df.iloc[i]['title']}")
        
        doc_vector = tfidf_matrix[i].tocoo()
        term_scores = list(zip(doc_vector.col, doc_vector.data))
        term_scores.sort(key=lambda x: x[1], reverse=True)
        
        print("Top Keywords:")
        for col, score in term_scores[:5]:
            print(f" - {feature_names[col]} (Score: {score:.3f})")
        print("-" * 40)
        
def cluster_rbi_documents(num_clusters=3):
    """Uses K-Means ML to automatically classify documents into economic topics."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT title, content FROM documents WHERE content IS NOT NULL", conn)
    conn.close()

    if df.empty:
        return

    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.85, token_pattern=r'(?u)\b[a-zA-Z]+\b')
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(tfidf_matrix)
    
    print(f"Successfully clustered {len(df)} documents into {num_clusters} topics.\n")
    for i in range(num_clusters):
        print(f"=== CLUSTER {i} ===")
        samples = df[df['cluster'] == i]['title'].head(5).tolist()
        for title in samples:
            print(f" - {title}")
        print()