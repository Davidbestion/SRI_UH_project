from src import process_data
class Data:
    def __init__(self):
        print('Loading products...')    
        self.products = process_data.get_products()
        print('Loading sells...')
        self.sells = process_data.get_sells(self.products)
        print('Loading ratings...')
        self.ratings = process_data.get_ratings(self.products)
        print('Loading reviews...')
        self.reviews = process_data.get_reviews_sentiment(self.products)
        print('Loading users_products...')
        self.users_products = process_data.get_usersxproducts()
        print('Loading users alike...')
        self.users_alike = process_data.get_users_alike(self.users_products)
        print('Loading recommendations...')
        self.recommendations = process_data.recommend_products_by_user(self.users_products, self.users_alike)

    def get_most_popular_products(self, n):
        return process_data.most_popular_products(self.sells, n)
    
    def get_best_rated_products(self, n):
        return process_data.best_rated_products(self.ratings, n)
    
    def get_worst_rated_products(self, n):
        return process_data.worst_rated_products(self.ratings, n)
    
    def get_positive_reviews(self, n):
        return process_data.positive_reviews(self.reviews, n)
    
    def get_negative_reviews(self, n):
        return process_data.negative_reviews(self.reviews, n)
    
    def get_recommend_products(self, n):
        return process_data.recommend_products(self.recommendations, n)
    
    def get_products(self):
        return self.products

    def get_sells(self):
        return self.sells

    def get_ratings(self):
        return self.ratings

    def get_reviews(self):
        return self.reviews

    def get_users_products(self):
        return self.users_products

    def get_users_alike(self):
        return self.users_alike

    def get_recommendations(self):
        return self.recommendations

    def get_products(self):
        return self.products

    def get_sells(self):
        return self.sells

    def get_ratings(self):
        return self.ratings

    def get_reviews(self):
        return self.reviews

    def get_users_products(self):
        return self.users_products

    def get_users_alike(self):
        return self.users_alike

    def get_recommendations(self):
        return self.recommendations

    def get_products(self):
        return self.products

    def get_sells(self):
        return self.sells

def main():

    data = Data()
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
                
        
        
                
                    

    
            