# Review Rating System

## Author

David Sanchez Iglesias

## Problem

This review rating system is a program that processes the reviews of a web page to gather information about whatever is in the page. For example, a virtual store, a web page made for buying and selling stuff. It's common to find reviews in this kind of sites. Those reviews contain information useful to promote certain products for example or making better and personalized ads. This project is intended to gather and organize such information, it does not make recommendations or select ads but give the programmer or the owner of the site the information he/she needs to improve the quality of his/her site.

## Requirements

This project uses python and certain libraries of this language. Those libraries are in the ```requirements.txt``` file. To install those libraries you can open the console/command prompt and use pip: ```pip install -r requirements```.
This project uses as database a fragment of the **Amazon US Customer Reviews Dataset** (<https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset>), specifically the **amazon_reviews_us_Digital_Software_v1_00** at Kaggle (<https://www.kaggle.com>) and the `amazon_polarity` database of the Python library ```databases```. The first dataset can be downloaded with the `download.py` in the `datasets` folder. For that, the API of Kaggle is used only to download that specific dataset. That API can be installed using pip too ('pip install Kaggle').

## How to use the project

On Linux, execute the `startup.sh` file. If you want to download the amazon_reviews_us_Digital_Software_v1_00 using the `download.py` file you'll have to run this file using a code editor of your choice or using the console/command prompt to navigate to the `datasets` folder and using the command: `python3 download.py`.
