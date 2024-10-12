# Facilita el trabajo con los términos indexados del corpus
from gensim.corpora import Dictionary

# Facilita la obtención de los valores tf-idf de los documentos 
from gensim.models import TfidfModel

# Para generar la matriz densa de tf-idf
from gensim.matutils import corpus2dense

# Para realizar el proceso de reduccion de dimensiones
from sklearn.decomposition import PCA

# Para preprocesar el texto
from model import preprocess_text

# Para calcular la similitud coseno
from sklearn.metrics.pairwise import cosine_similarity

def prepare_data(corpus, query):
    
    texts = []
    for i in range(len(corpus)):
        texts[i] = preprocess_text(corpus[i])
    
    # Se crea el diccionario de los terminos indexados
    dict = Dictionary(corpus)
    
    vocab = list(dict.token2id.keys())
    
    corpus = [dict.doc2bow(doc) for doc in corpus]
    
    tf_idf = TfidfModel(corpus)
    
    # Se crea el modelo tf-idf
    corpus_tfidf_dense = corpus2dense(corpus, len(vocab), len(texts))
    
    #PROCESS QUERY
    query = prepare_query(query, dict, tf_idf)
    
    variance = 0.95
    pca = PCA(n_components=variance)
    
    corpus_pca_fit = pca.fit(corpus_tfidf_dense)
    
    corpus_pca = corpus_pca_fit.transform(corpus_tfidf_dense)
    
    query_pca = corpus_pca_fit.transform(query)
    
    chosen_texts = retrieve_texts(corpus_pca, query_pca)
    
    texts = [texts[i] for i, _ in chosen_texts]
    
    return texts
    
    

def prepare_query(query, dictionary, tfidf):
    # Se tokeniza la consulta
    query = preprocess_text(query)
    
    # Se convierte la consulta a terminos indexados
    query = dictionary.doc2bow(query)
    
    # Se convierte la consulta a tf-idf
    query = tfidf[query]
    
    # Se convierte la consulta a matriz densa
    query = corpus2dense([query], len(dictionary), 1)
    
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
    
    return simils.sort(key=lambda x: x[1], reverse=True)