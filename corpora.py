import nltk

# nltk.download('stopwords')
# nltk.download('wordnet')

from datasets import load_dataset
import pandas as pd
# Load the Amazon Customer Reviews dataset
amazon_polarity = load_dataset('amazon_polarity')

amazon_data = pd.read_csv("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv", sep='\t')


