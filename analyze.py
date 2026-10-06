from src.processing.nlp import analyze_rbi_vocabulary, cluster_rbi_documents

if __name__ == "__main__":
    cluster_rbi_documents(num_clusters=3)