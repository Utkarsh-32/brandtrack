from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_texts(texts, k=6):
    if len(texts) < 2:
        return [0] * len(texts)
    
    vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=1,
        stop_words="english"
    )

    X = vectorizer.fit_transform(texts)
    k = min(k, len(texts))
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    return model.labels_.tolist()