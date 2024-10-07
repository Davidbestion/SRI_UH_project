import tqdm
import time
from utils import save_sentence, load_sentences

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from corpora import amazon_polarity

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

CANTIDAD = 10000

def build_model(evaluate=False):
    timer = time.time()
    timer1 = time.time()
    
    print('Loading data...')
    corpus_train, corpus_test = get_corpus()
    
    print('Preprocessing text...')
    timer1 = time.time()
    # Split the data into training and test sets
    # X_train, X_test, y_train, y_test = train_test_split(train_texts, train_labels, test_size=0.2)
    train_texts, train_labels = prepare_data(corpus_train)
    test_texts, test_labels = prepare_data(corpus_test)
    print('Preprocessing time:', time.time()-timer1)
    
    # Train the model
    print('Training model...')
    timer1 = time.time()
    model, vectorizer = train_model(train_texts, train_labels)
    print('Training time:', time.time()-timer1)
    
    # Evaluate the model
    
    if evaluate:
        print('Evaluating model...')
        accuracy = evaluate_model(model, vectorizer, test_texts, test_labels)
        print('Accuracy:', accuracy)
    
    print('Elapsed time:', time.time()-timer)
    return model, vectorizer

def get_corpus():
    #De querer cargar todo el corpus, descomentar las siguientes lineas
    # corpus_train = amazon_polarity['train']--------------------------
    # corpus_test = amazon_polarity['test']----------------------------
    # hasta aqui
    # y comentar las siguientes
    corpus_train = []
    corpus_test = []
    for i in tqdm.tqdm(range(0,CANTIDAD)):
        corpus_train.append(amazon_polarity['train'][i])
        corpus_test.append(amazon_polarity['test'][i])
    # hasta aqui
    return corpus_train, corpus_test

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

# Prepare the data
def prepare_data(corpus):
    # Preprocess the text
    for i in tqdm.tqdm(range(0,CANTIDAD)):
        corpus[i]['content'] = preprocess_text(corpus[i]['content'])
    # Extract the text and labels from the data
    texts = [item['content'] for item in corpus]
    labels = [item['label'] for item in corpus]
    return texts, labels

def train_model(train_texts, train_labels):
    # Convert text data to TF-IDF features
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(train_texts)
    # Train a logistic regression model
    model = DecisionTreeClassifier()
    model.fit(X_train_tfidf, train_labels)
    return model, vectorizer

def evaluate_model(model, vectorizer, test_texts, test_labels):
    # Predict and evaluate the model
    y_pred = model.predict(vectorizer.transform(test_texts))
    accuracy = accuracy_score(test_labels, y_pred)
    return accuracy
