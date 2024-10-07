from corpora import amazon_data, amazon_polarity
from gensim.corpora import Dictionary
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import tqdm

CANTIDAD = 400000

# Tokenizacion
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

# Seleccionar el corpus a utilizar (de amazon_polarity, la cantidad establecida en CANTIDAD)
corpus = []
for i in tqdm.tqdm(range(0,CANTIDAD)):
    corpus.append(amazon_polarity['test'][i])

# Preparacion de datos
# Preprocesamiento de texto
print('Preprocessing text...')
for i in tqdm.tqdm(range(0,CANTIDAD)):
    corpus[i]['content'] = preprocess_text(corpus[i]['content'])

# Representacion
# Creacion de diccionario
# dictionary = Dictionary(corpus['content'])

# Entrenar el modelo de analisis de sentimientos
# Inicializar el analizador de sentimientos de NLTK
analyzer = SentimentIntensityAnalyzer()

# Obtener el sentimiento de un texto
def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    sentiment = 1 if scores['pos'] > 0 else 0
    return sentiment

# Obtener el sentimiento de cada review
print('Getting sentiment...')
for i in tqdm.tqdm(range(len(corpus))):
    corpus[i]['sentiment'] = get_sentiment(corpus[i]['content'])

# Evaluacion
from sklearn.metrics import confusion_matrix
sentiment = []
labels = []
for i in tqdm.tqdm(range(len(corpus))):
    sentiment.append(corpus[i]['sentiment'])
    labels.append(corpus[i]['label'])
    
print(confusion_matrix(sentiment, labels))

from sklearn.metrics import classification_report
print(classification_report(sentiment, labels))

# Porcentaje de aciertos
accuracy = 0
for i in range(len(corpus)):
    if corpus[i]['sentiment'] == corpus[i]['label']:
        accuracy += 1
print(f'Accuracy: {accuracy/len(corpus)}')
