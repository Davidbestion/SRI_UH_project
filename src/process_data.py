import tqdm
from model import build_model, preprocess_text
from corpora import amazon_data 

from tqdm import tqdm

CANTIDAD = 10000
     
corpus = amazon_data  
    

def get_products():
    products = []
    for i in tqdm(range(0, CANTIDAD), desc="Getting Products"):
        if corpus['product_title'][i] not in products:
            products.append(corpus['product_title'][i])
    return products

def get_sells(products):
    sells = {}
    for product in tqdm(products, desc="Calculating Sells"):
        if product not in sells:
            sells[product] = 0
        for i in tqdm(range(0, CANTIDAD), desc=f"Counting sells for {product}", leave=False):
            if corpus['product_title'][i] == product and corpus['verified_purchase'][i] == 'Y':
                sells[product] += 1
    sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)
    return sells

def most_popular_products(sells, amount):
    # 10 more popular products
    popular_products = sells[:amount]
    return popular_products

def get_ratings(products):
    ratings = {}
    for product in tqdm(products, desc="Getting Ratings"):
        if product not in ratings:
            ratings[product] = []
        for i in tqdm(range(0, CANTIDAD), desc=f"Collecting ratings for {product}", leave=False):
            if corpus['product_title'][i] == product:
                ratings[product].append(corpus['star_rating'][i])
    for product in products:
        ratings[product] = sum(ratings[product]) / len(ratings[product]) if ratings[product] else 0
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    return ratings

def best_rated_products(ratings, amount):
    # 10 best rated products
    best_rated_products = ratings[:amount]
    return best_rated_products

def worst_rated_products(ratings, amount):
    # 10 worst rated products
    worst_rated_products = ratings[-amount:]
    return worst_rated_products

def get_reviews_sentiment(products):
    model_, vectorizer = build_model(evaluate=True)
    reviews = {}
    for product in tqdm(products, desc="Getting Reviews Sentiment"):
        if product not in reviews:
            reviews[product] = []
        for i in tqdm(range(0, CANTIDAD), desc=f"Collecting reviews for {product}", leave=False):
            if corpus['product_title'][i] == product:
                reviews[product].append(preprocess_text(corpus['review_body'][i]))
    for product in products:
        reviews[product] = sum(model_.predict(vectorizer.transform(reviews[product]))) / len(reviews[product]) if reviews[product] else 0
    reviews = sorted(reviews.items(), key=lambda x: x[1], reverse=True)
    return reviews

def positive_reviews(reviews, amount):
    # 10 products with most positive reviews
    positive_reviews = reviews[:amount]
    return positive_reviews

def negative_reviews(reviews, amount):
    # 10 products with most negative reviews
    negative_reviews = reviews[-amount:]
    return negative_reviews

def get_usersxproducts():
    users = {}
    for i in tqdm(range(0, CANTIDAD), desc="Getting Users x Products"):
        if corpus['customer_id'][i] not in users:
            users[corpus['customer_id'][i]] = []
        users[corpus['customer_id'][i]].append(corpus['product_title'][i])
    return users

def get_similar_users(users):
    user_matrix = {}
    for user1 in tqdm(users, desc="Finding Similar Users"):
        user_matrix[user1] = {}  # Initialize dictionary for each user1
        for user2 in users:
            if user1 != user2:
                # If all the buys of user1 are in the buys of user2 or vice versa
                set1 = set(users[user1])
                set2 = set(users[user2])
                cant_products = len(set1.intersection(set2))
                user_matrix[user1][user2] = cant_products
    similar_users = sorted(user_matrix.items(), key=lambda x: x[1], reverse=True)
    return similar_users, user_matrix

def get_users_alike(users):
    '''
    For each user, get the users that made the same buys.
    '''
    _, user_matrix = get_similar_users(users)
    users_alike = {}
    for user1 in tqdm(users, desc="Getting Users Alike"):
        users_alike_aux = []
        for user2 in users:
            # If user_matrix[user1][user2] > the lowest value of users_alike_aux
            if user1 != user2:
                if len(users_alike_aux) < 10:
                    users_alike_aux.append(user2)
                else:
                    if user_matrix[user1][user2] > min(users_alike_aux):
                        users_alike_aux.remove(min(users_alike_aux))
                        users_alike_aux.append(user2)
        users_alike[user1] = users_alike_aux
    return users_alike

def recommend_products_by_user(users, users_alike):
    '''
    For each user, get the products that the users that made the same buys bought and he didn't.
    '''
    recommended_products = {}
    for user in tqdm(users, desc="Recommending Products by User"):
        recommended_unpurchased_products = []
        for user_alike in users_alike[user]:
            for product in users[user_alike]:
                if product not in users[user]:
                    recommended_unpurchased_products.append(product)
        recommended_products[user] = recommended_unpurchased_products
    return recommended_products

def recommend_products(recommendations, sells, amount):
    '''
    10 recommended products for each user, the ones with more sells.
    '''
    recommend_products = {}
    for user in tqdm(recommendations, desc="Recommending Products"):
        recommend_products[user] = sorted(recommendations[user], key=lambda x: sells[x], reverse=True)[:amount]
    return recommend_products