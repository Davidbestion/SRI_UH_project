import string 
from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
# from nltk.tokenize import word_tokenize

from gensim.corpora import Dictionary

from gensim.models import LsiModel
from gensim.models import LdaModel

import spacy
nlp = spacy.load('es_core_news_sm')

def normalize_corpus(corpus):
    normalized_corpus = []
    for doc in corpus:
        doc = unidecode(doc)
        doc = doc.lower()
        # Take care of punctuation and digits
        doc = doc.translate(str.maketrans('', '', string.punctuation))
        doc = doc.translate(str.maketrans('', '', string.digits))
        # Remove stopwords
        doc = ' '.join([token for token in doc.split() if token not in stopwords.words('spanish')])
        # Lemmatize
        doc = nlp(doc)
        doc = ' '.join([token.lemma_ for token in doc])
        # # Tokenize
        # tokens = word_tokenize(doc, language='spanish')
        # normalized_corpus.append(tokens)
        normalized_corpus.append(doc.split())
    return normalized_corpus

# Creating document-term matrix 
def create_document_term_matrix(corpus):
    dictionary = Dictionary(corpus)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus]
    return dictionary, doc_term_matrix

# LSA model
def create_lsa_model(doc_term_matrix, dictionary, num_topics):
    lsa_model = LsiModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary)
    return lsa_model

# LDA model
def create_lda_model(doc_term_matrix, dictionary, num_topics):
    lda_model = LdaModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary)
    return lda_model

# Function to get the dominant topic for each sentence
def get_dominant_topics(model, corpus, texts):
    dominant_topics = {}
    for i, row in enumerate(model[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the dominant topic, its percentage contribution, and keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                dominant_topics[texts[i]] = {'Dominant_Topic': int(topic_num), 'Perc_Contribution': round(prop_topic,4), 'Topic_Keywords': topic_keywords}
    return dominant_topics

#=========================================PRUEBA=============================================
# Oraciones de prueba:
oracion1 = "El clima en Madrid es muy agradable en primavera."
oracion2 = "La gastronomía española es famosa por sus tapas."
oracion3 = "El Museo del Prado es uno de los más importantes de España."

corpus = [oracion1, oracion2, oracion3]
normalized_corpus = normalize_corpus(corpus)
dictionary, doc_term_matrix = create_document_term_matrix(normalized_corpus)
LSA = create_lsa_model(doc_term_matrix, dictionary, 3)
LDA = create_lda_model(doc_term_matrix, dictionary, 3)

# Get dominant topics for each sentence
dominant_topics_lda = get_dominant_topics(LDA, doc_term_matrix, corpus)
dominant_topics_lsa = get_dominant_topics(LSA, doc_term_matrix, corpus)

# Print the dominant topic for each sentence
print("LDA Model:")
for sentence, topics in dominant_topics_lda.items():
    print(f"Sentence: {sentence}\nTopic: {topics['Dominant_Topic']}, Keywords: {topics['Topic_Keywords']}\n")

print("LSA Model:")
for sentence, topics in dominant_topics_lsa.items():
    print(f"Sentence: {sentence}\nTopic: {topics['Dominant_Topic']}, Keywords: {topics['Topic_Keywords']}\n")
    