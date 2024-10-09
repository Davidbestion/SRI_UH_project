from datasets import load_from_disk
import pandas as pd

#Load amazon polarity from local folder
try:
    amazon_polarity = load_from_disk("datasets/Amazon_Reviews/amazon_polarity", )
except:
    raise Exception("Please download the dataset first. Take a look at datasets/download.py")

amazon_data = pd.read_csv("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv", sep='\t')

user_reviews = pd.read_csv('datasets/Steam/Steam_Reviews_Dataset/reviews-1-115.csv')
descriptions = pd.read_csv('datasets/Steam/Steam-Store-Games/steam_description_data.csv')
games = pd.read_csv('datasets/Steam/Steam-Store-Games/steam.csv')

