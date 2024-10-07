import kaggle

# Check if there is enough space in disc to download (22 gb)
print(kaggle.api.dataset_list_files("cynthiarempel/amazon-us-customer-reviews-dataset").files[9].size)
kaggle.api.dataset_download_file("cynthiarempel/amazon-us-customer-reviews-dataset", "amazon_reviews_us_Digital_Software_v1_00.tsv", path="datasets/Amazon_Reviews")

# Unzip file
import os
import zipfile
with zipfile.ZipFile("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv.zip", 'r') as zip_ref:
    zip_ref.extractall("datasets/Amazon_Reviews")
os.remove("datasets/Amazon_Reviews/amazon_reviews_us_Digital_Software_v1_00.tsv.zip")

# Descomentar para bajar todo el dataset de Amazon
# Advertir que son 22 GB comprimido, mas de 50 GB descomprimido
# kaggle.api.dataset_download_files("cynthiarempel/amazon-us-customer-reviews-dataset", path="datasets/Amazon_Reviews", unzip=True)

# # Unzip file
# import os
# import zipfile
# with zipfile.ZipFile("datasets/Amazon_Reviews/amazon-us-customer-reviews-dataset.zip", 'r') as zip_ref:
#     zip_ref.extractall("datasets/Amazon_Reviews")
# os.remove("datasets/Amazon_Reviews/amazon-us-customer-reviews-dataset.zip")