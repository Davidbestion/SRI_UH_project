from corpora import amazon_data, amazon_polarity
# from utils import save_sentence, load_sentences
from model import build_model
from similarity import search
from process_data import Data

#Test similarity
data = Data()
games = {}
for game in data.games:
    games[game.name] = game.description
corpus = list(games.values())
query = 'A game with a lot of action and shooting'
texts = search(corpus, query)
print(texts)
    
# build_model(evaluate=True)
# # Example: Print the first review
# print(amazon_data['train'][0])

# # Example: Print the first review
# print(amazon_data['test'][0])


    