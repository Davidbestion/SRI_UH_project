from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.matutils import corpus2dense

# from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from numpy import dot
from numpy.linalg import norm

from src.model import preprocess_text


def search(corpus, query, variance=0.95, n_clusters=10, alpha=0.1, cant_docs=10, cant_centroids=3):
    """Searches for the most similar texts to the query in the corpus

    Args:
    - corpus : [[str]]
        List of texts to search in.
    - query : str
        Text to search for.
        
    Return:
    - texts : [str]
        List of tuples with the index of the text in the corpus and the text itself.
    """
    
    print("Running similarity search...")
    texts = {}
    
    for i in range(len(corpus)):
        texts[i] = preprocess_text(corpus[i], False)
    
    # diccionario de los terminos indexados
    dict = Dictionary(texts.values())
    vocab = list(dict.token2id.keys())
    corpus_bow = [dict.doc2bow(doc) for doc in texts.values()] # corpus en formato BoW
    tf_idf = TfidfModel(corpus_bow)
    
    # modelo tf-idf
    corpus_tfidf_dense = corpus2dense(tf_idf[corpus_bow], len(vocab), len(texts)).T
    
    #PROCESS QUERY
    query = prepare_query(query, dict, vocab, tf_idf)
    
    pca = PCA(n_components=variance)
    corpus_pca_fit = pca.fit(corpus_tfidf_dense)
    corpus_pca = corpus_pca_fit.transform(corpus_tfidf_dense)
    query_pca = corpus_pca_fit.transform(query)
    
    #Get centroids
    centroids, kmeans = get_centroids(corpus_pca, query_pca, n_clusters, alpha, cant_centroids)
    if not centroids:
        return []
    
    cluster_docs = []
    for i in centroids:
        # Extraer los documentos que pertenecen a ese cluster
        cluster_docs = cluster_docs + [j for j, x in enumerate(kmeans.labels_) if x == i]
    
    # Calcular la similitud entre la consulta y los documentos del cluster usando 'retreieve_documents'
    # Crear nuevo corpus con los documentos del cluster
    corpus_cluster = corpus_pca[cluster_docs]
    new_docs = retrieve_texts(corpus_cluster, query_pca[0])[0:cant_docs]
    if not new_docs:
        return []

    texts_return = [(i, sim, corpus[i]) for i, sim in new_docs]
    return texts_return

#n_clusters=5, alpha=0.5, cant_docs=10, cant_centroids=5
def get_centroids(corpus_pca, query_pca, n_clusters, alpha, cant_centroids): #cant_docs=10):
    """Get the centroids of the clusters of the corpus and the query

    Args:
    - corpus_pca : [[float]]
        Matrix with the tf-idf representation of the corpus.
    - query_pca : [float]
        tf-idf representation of the query.
    - n_clusters : int
        Number of clusters to generate.
    - alpha : float
        Weight of the query in the clustering.
    - cant_docs : int
        Number of documents to return.
        
    Return:
    - centroids : [[float]]
        List of the centroids of the clusters.  
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(corpus_pca)
    centroids = kmeans.cluster_centers_

    # Obteniendo los centroides mas cercanos a la consulta (ordenados por similitud)
    query_centroids = []
    for i, centroid in enumerate(centroids):
        if cosine_similarity(centroid, query_pca[0]) >= alpha:
            query_centroids.append(i)
        if len(query_centroids) == cant_centroids:
            break
        
    return query_centroids, kmeans
    
    

def prepare_query(query, dictionary, vocab, tfidf):
    """Prepares the query to be compared with the corpus

    Args:
    - query : str
        Text to search for.
    - dictionary : gensim.corpora.Dictionary
        Dictionary of the corpus.
    - tfidf : gensim.models.TfidfModel
        Tf-idf model of the corpus.

    Returns:
    - query : [float]
        Tf-idf representation of the query.
    """
    query = preprocess_text(query, False)
    
    query_dict = dictionary.doc2bow(query)
    query_tfidf = tfidf[query_dict]
    
    # Se convierte la consulta a matriz densa
    query = corpus2dense([query_tfidf], len(vocab), 1).T
    
    return query

def retrieve_texts(corpus_matrix, vector_query):
    """
    Gets the similarity between the corpus and a query
    
    Args:
    - corpus_matriz : [[float]]
        tf-idf representation of the query. Each row is considered a document.
    - vector_query : [float]
        tf-idf representation of the query.
        
    Return:
    - simils : [(int, float)]

    """
    simils = []
    for i, text in enumerate(corpus_matrix):
        simils.append((i, cosine_similarity(vector_query, text)))
    #Ordenarlos por similitud
    simils.sort(key=lambda x: x[1], reverse=True)
    return simils

def cosine_similarity(a, b):
    """
    Calculates the cosine distance between two vectors. Both vectors are expected to have the same dimension.
    
    Args:
    - a : [Number]
        Vector.
    - b : [Number]
        Vector.

    Return:
    - float
    
    """
    return dot(a, b)/(norm(a) * norm(b))