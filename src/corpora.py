from datasets import load_from_disk
import pandas as pd

#Load amazon polarity from local folder
try:
    amazon_polarity = load_from_disk("datasets/Amazon_Reviews/amazon_polarity")
except:
    raise Exception("Please download the dataset first. Take a look at datasets/download.py")

amazon_data = pd.read_csv("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv", sep='\t')


