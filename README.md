# Review Rating System

## Members

1. David Sanchez Iglesias
2. Yoel Enriquez Sena

## Problem

This review rating system is a program that processes the reviews of a web page to gather information about whatever is in the page. For example, a virtual store, a web page maded for bying and selling stuff. It's common to find reviews in this kind of sites. Those reviews contains information usefull to promote certaing products for eexample or making better and personalized ads. This project is intended to gather and organize such information, it does not make recomendations or select ads but give the programer or the owner of the site the information he/she needs to inprouve the quality of his/her site.

## Requirements

This project uses python and certain libraries of this language. Those libraries are in the 'requirements.txt' file. To install those libraries one can open the console/command prompt and use pip: 'pip install -r requirements'.
This project uses as database a fragment of the **Amazon US Customer Reviews Dataset** (https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset), specificly the **amazon_reviews_us_Digital_Software_v1_00** at Kaggle (https://www.kaggle.com) and the 'amazon_polarity' database of the pyhton library 'databases'. The first dataset can be downloaded with the 'download.py' in the 'datasets' folder. For that, the apy of kaggle is used only to download that specific dataset. That API can be installed using pip too ('pip install kaggle').