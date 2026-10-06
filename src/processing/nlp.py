import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
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
    
    # Convert our text into a mathematical matrix
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