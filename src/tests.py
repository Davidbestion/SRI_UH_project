from corpora import amazon_data, amazon_polarity
# from utils import save_sentence, load_sentences
from model import build_model

build_model(evaluate=True)
# # Example: Print the first review
# print(amazon_data['train'][0])

# # Example: Print the first review
# print(amazon_data['test'][0])


    