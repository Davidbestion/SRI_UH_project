# Description: Download datasets from Hugging Face Datasets, nltk and Kaggle
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

#----------------------------------------Amazon_Polarity_dataset----------------------------------------

from datasets import load_dataset

# Load the Amazon Customer Reviews dataset
amazon_polarity = load_dataset('amazon_polarity')
amazon_polarity.save_to_disk("datasets/Amazon_Reviews/amazon_polarity")

#----------------------------------------Amazon_US_customer_reviews_dataset----------------------------------------
# ATTENTION: 
# Uncomment to download the dataset
import kaggle

# # Check if there is enough space in disc to download (22 gb)
# print(kaggle.api.dataset_list_files("cynthiarempel/amazon-us-customer-reviews-dataset").files[9].size)
# kaggle.api.dataset_download_file("cynthiarempel/amazon-us-customer-reviews-dataset", "amazon_reviews_us_Digital_Software_v1_00.tsv", path="datasets/Amazon_Reviews")
kaggle.api.dataset_download_files("andrewmvd/steam-reviews", path="datasets/Steam/Steam_Reviews", unzip=True)
kaggle.api.dataset_download_files("nikdavis/steam-store-games", path="datasets/Steam/Steam_Store_Games", unzip=True)
kaggle.api.dataset_download_files("piyushagni5/sentiment-analysis-for-steam-reviews", path="datasets/Steam/Sentiment_Analysis_for_Steam_Reviews", unzip=True)

# # Unzip file
# import os
# import zipfile
# with zipfile.ZipFile("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv.zip", 'r') as zip_ref:
#     zip_ref.extractall("datasets/Amazon_Reviews")
# os.remove("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv.zip")

# Descomentar para bajar todo el dataset de Amazon
# Advertir que son 22 GB comprimido, mas de 50 GB descomprimido
# kaggle.api.dataset_download_files("cynthiarempel/amazon-us-customer-reviews-dataset", path="datasets/Amazon_Reviews", unzip=True)

# # Unzip file
# import os
# import zipfile
# with zipfile.ZipFile("datasets/Amazon_Reviews/amazon-us-customer-reviews-dataset.zip", 'r') as zip_ref:
#     zip_ref.extractall("datasets/Amazon_Reviews")
# os.remove("datasets/Amazon_Reviews/amazon-us-customer-reviews-dataset.zip")