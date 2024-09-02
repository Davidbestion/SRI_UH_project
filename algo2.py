import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# from algo import preprocess_text
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

corpus = pd.read_csv('https://raw.githubusercontent.com/pycaret/pycaret/master/datasets/amazon.csv')

corpus['reviewText'] = corpus['reviewText'].apply(preprocess_text)

#Select some of the reviews randomly (as if a person writted those reviews)
random_reviews = corpus.sample(n=50, random_state=1)['reviewText']

video_games = ['angry birds', 'farmville', 'bad piggies']
chosen_game = video_games[0]

#Let's say the random_reviews are reviews of the chosen_game
#The client just buoght the chosen_game and we want to know by their reviews what other games he likes
#To achieve this we will search for al games mentioned in his reviews and see what of those games he likes the most making a sentiment analysis of the reviews where this game appears.

def find_chosen_game_reviews(reviews, chosen_game):
    return [review for review in reviews if chosen_game in review]
    
# test_corpus = ['I love angry birds', 'I hate farmville', 'I like bad piggies', 'I love angry birds and farmville', 'I hate angry birds and farmville', 'I like bad piggies and farmville', 'I love angry birds and bad piggies', 'I hate angry birds and bad piggies', 'I like bad piggies and angry birds', 'I love angry birds, farmville and bad piggies', 'I hate angry birds, farmville and bad piggies', 'I like bad piggies, farmville and angry birds']
# print(find_chosen_game_reviews(test_corpus, 'angry birds'))

chosen_reviews = find_chosen_game_reviews(random_reviews, chosen_game)

# initialize NLTK sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    sentiment = 1 if scores['pos'] > 0 else 0
    return sentiment

corpus['sentiment'] = corpus['reviewText'].apply(get_sentiment)

# def get_sentiment_score(text):
#     scores = analyzer.polarity_scores(text)
#     return scores['compound']
    
from sklearn.metrics import confusion_matrix
print(confusion_matrix(corpus['Positive'], corpus['sentiment']))

from sklearn.metrics import classification_report
print(classification_report(corpus['Positive'], corpus['sentiment']))
            