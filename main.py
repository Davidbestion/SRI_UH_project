from src import process_data

def main():

    data = process_data.Data()
    print('Mark...')
    games_reviews = data.games_with_most_negative_reviews(10)
    print("Games with most negative reviews: ready.")
    return data
    # print('Loading products...')    
    # products = process_data.get_products()
    # print('Loading sells...')
    # sells = process_data.get_sells(products)
    # print('Loading ratings...')
    # ratings = process_data.get_ratings(products)
    # print('Loading reviews...')
    # reviews = process_data.get_reviews_sentiment(products)
    # print('Loading users_products...')
    # users_products = process_data.get_usersxproducts()
    # print('Loading users alike...')
    # users_alike = process_data.get_users_alike(users_products)
    # print('Loading recommendations...')
    # recommendations = process_data.recommend_products_by_user(users_products, users_alike)

    
    # # 10 more popular products
    # popular_products = process_data.most_popular_products(sells, 10)
    
    # # Best rated products
    # ratings = process_data.get_ratings()

    # # 10 best rated products
    # best_rated_products = process_data.best_rated_products(ratings, 10)
    
    # # Worst rated products
    # worst_rated_products = process_data.worst_rated_products(ratings, 10)
    
    # # 10 products with most positive reviews
    # positive_reviews = process_data.positive_reviews(reviews, 10)
    
    # # Products with most negative reviews
    # negative_reviews = process_data.negative_reviews(reviews, 10)
    
    # # Recommend products by user
    # recommend_products = process_data.recommend_products(recommendations, 10)
    
    # # # Another strategy could be to recommend the products with the best ratings
    # # for user in recommend_products:
    # #     recommend_products[user] = sorted(recommended_products[user], key=lambda x: ratings[x], reverse=True)[:10]
        
    # # # Another strategy could be to recommend the products with the most positive reviews
    # # for user in recommend_products:
    # #     recommend_products[user] = sorted(recommended_products[user], key=lambda x: reviews[x], reverse=True)[:10]
        
    # # # Another strategy could be to recommend the products that the most quantity of users that maded the same buys bought
    # # for user in recommend_products:
    # #     recommend_products[user] = sorted(recommended_products[user], key=lambda x: user_matrix[user][x], reverse=True)[:10]
   
if __name__ == "__main__":
    main()
                
        
        
                
                    

    
            