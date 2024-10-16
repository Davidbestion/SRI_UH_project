import tqdm
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src.corpora import amazon_polarity
# from corpora import amazon_polarity

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

CANTIDAD = 1000

def build_model(evaluate=False):
    timer = time.time()
    timer1 = time.time()
    
    print()
    print('Preparing model...')
    corpus_train, corpus_test = get_corpus()
    
    print('Preprocessing text for model...')
    timer1 = time.time()
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
    print('Model prepared.')
    return model, vectorizer

def get_corpus():
    #De querer cargar todo el corpus, descomentar las siguientes lineas
    # corpus_train = amazon_polarity['train']--------------------------
    # corpus_test = amazon_polarity['test']----------------------------
    # hasta aqui
    # y comentar las siguientes
    corpus_train = []
    corpus_test = []
    for i in tqdm.tqdm(range(0,CANTIDAD), desc='Loading data'):
        corpus_train.append(amazon_polarity['train'][i])
        corpus_test.append(amazon_polarity['test'][i])
    # hasta aqui
    return corpus_train, corpus_test

def preprocess_text(text, return_as_text=True):
    if text is None:
        return ''
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    if return_as_text:
        # Join the tokens back into a string
        processed_text = ' '.join(lemmatized_tokens)
        return processed_text
    return lemmatized_tokens

# Prepare the data
def prepare_data(corpus):
    # Preprocess the text
    for i in tqdm.tqdm(range(0,CANTIDAD), desc='Preprocessing text'):
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
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, train_labels)
    return model, vectorizer

def evaluate_model(model, vectorizer, test_texts, test_labels):
    # Predict and evaluate the model
    y_pred = model.predict(vectorizer.transform(test_texts))
    accuracy = accuracy_score(test_labels, y_pred)
    return accuracy
