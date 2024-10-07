from model import build_model, preprocess_text
from corpora import amazon_data     

def main():
    corpus = amazon_data
    products = {}
    # More popular products
    for element in corpus:
        if element['product_title'] in products:
            products.append(element['product_title'])
    
    sells = {}
    for product in products:
        if product not in sells:
            sells[product] = 0
        for element in corpus:
            if element['product_title'] == product and element['verified_purchase'] == 'Y':
                sells[product] += 1
    
    # More popular products
    sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)
    # 10 more popular products
    popular_products = sells[:10]
    
    # Best rated products
    ratings = {}
    for product in products:
        if product not in ratings:
            ratings[product] = []
        for element in corpus:
            if element['product_title'] == product:
                ratings[product].append(element['star_rating'])

    for product in products:
        ratings[product] = sum(ratings[product])/len(ratings[product])
    
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    # 10 best rated products
    best_rated_products = ratings[:10]
    
    # Worst rated products
    worst_rated_products = ratings[-10:]
        
    # Products with most positive reviews
    model_, vectorizer = build_model(evaluate=True)
    reviews = {}
    for product in products:
        if product not in reviews:
            reviews[product] = []
        for element in corpus:
            if element['product_title'] == product:
                reviews[product].append(preprocess_text(element['review_body']))
    
    for product in products:
        reviews[product] = sum(model_.predict(vectorizer.transform(reviews[product])))/len(reviews[product])
        
    reviews = sorted(reviews.items(), key=lambda x: x[1], reverse=True)
    # 10 products with most positive reviews
    positive_reviews = reviews[:10]
    
    # Products with most negative reviews
    negative_reviews = reviews[-10:]
    
    # For each user, get the users tha maded the same buys
    users = {}
    for element in corpus:
        if element['customer_id'] not in users:
            users[element['customer_id']] = []
        users[element['customer_id']].append(element['product_title'])
    
    # For each user, get the users that maded the same buys
    user_matrix = {}
    for user1 in users:
        for user2 in users:
            if user1 != user2:
                #If all the buys of user1 are in the buys of user2 or viceversa
                set1 = set(users[user1])
                set2 = set(users[user2])
                cant_products = len(set1.intersection(set2))
                user_matrix[user1][user2] = cant_products
    # 10 users with most similar buys
    similar_users = sorted(user_matrix.items(), key=lambda x: x[1], reverse=True)
    
    users_alike = {}
    for user1 in users:
        users_alike_aux = []
        for user2 in users:
            #If user_matrix[user1][user2] > the lowest value of users_alike_aux
            if user1 != user2:
                if len(users_alike) < 10:
                    users_alike_aux.append(user2)
                else:
                    if user_matrix[user1][user2] > min(users_alike_aux):
                        users_alike_aux.remove(min(users_alike))
                        users_alike_aux.append(user2)
        users_alike[user1] = users_alike_aux
    
    # For each user, get the products that the users that maded the same buys bought and he didn't
    recommended_products = {}
    for user in users:
        recommended_unpurchased_products = []
        for user_alike in users_alike[user]:
            for product in users[user_alike]:
                if product not in users[user]:
                    recommended_unpurchased_products.append(product)
        recommended_products[user] = recommended_unpurchased_products
        
    # 10 recommended products for each user, the ones with more sells
    for user in recommended_products:
        recommended_products[user] = sorted(recommended_products[user], key=lambda x: sells[x], reverse=True)[:10]
    
    # # Another strategy could be to recommend the products with the best ratings
    # for user in recommended_products:
    #     recommended_products[user] = sorted(recommended_products[user], key=lambda x: ratings[x], reverse=True)[:10]
        
    # # Another strategy could be to recommend the products with the most positive reviews
    # for user in recommended_products:
    #     recommended_products[user] = sorted(recommended_products[user], key=lambda x: reviews[x], reverse=True)[:10]
        
    # # Another strategy could be to recommend the products that the most quantity of users that maded the same buys bought
    # for user in recommended_products:
    #     recommended_products[user] = sorted(recommended_products[user], key=lambda x: user_matrix[user][x], reverse=True)[:10]
    
                
        
        
                
                    

    
            