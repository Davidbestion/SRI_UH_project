import tqdm
from src.model import build_model, preprocess_text
# from model import build_model, preprocess_text
from src.corpora import amazon_data, user_reviews, descriptions, games_info, CANT_REVIEWS
# from corpora import amazon_data, user_reviews, descriptions, games_info
# import similarity
import src.similarity as similarity

from tqdm import tqdm

CANTIDAD = 1000
# CANT_REVIEWS = 10000
     
corpus = amazon_data 

#NOTE: Revisar el analisis de sentimiento.
class Game:
    def __init__(self, app_id, name, developer, platforms, description, categories, genres, tags, price):
        self.id = app_id
        self.name = name
        self.developer = developer
        self.platforms = platforms
        self.description = description
        self.categories = categories
        self.genres = genres
        self.tags = tags
        self.price = price
    
class Review:
    def __init__(self, user_id, game, rating, review, adquired, hours_played):
        self.user_id = user_id
        self.game = game
        self.voted_up = rating
        self.review = review if review else ''
        self.game_adquired = adquired
        self.bougth = adquired if adquired and game.price > 0.0 else False
        self.hours_played = hours_played if hours_played else 0
        
def load_info():
    games = []
    for i in tqdm(range(0, CANTIDAD), desc="Loading Games"):
        game_id = games_info['appid'][i]
        game_name = games_info['name'][i]
        developer = games_info['developer'][i]
        platforms = games_info['platforms'][i].split(';')
        for i in range(0, len(descriptions['steam_appid'])):
            if descriptions['steam_appid'][i] == game_id:
                info = descriptions['detailed_description'][i]
                break
        description = info
        categories = games_info['categories'][i].split(';')
        genres = games_info['genres'][i].split(';')
        tags = games_info['steamspy_tags'][i].split(';')
        price = games_info['price'][i]
        games.append(Game(game_id, game_name, developer, platforms, description, categories, genres, tags, price))
    reviews = []
    for i in tqdm(range(0, CANT_REVIEWS), desc="Loading Reviews"):
        chosen_game = None
        for game in games:
            if game.id == user_reviews['appid'][i]:
                chosen_game = game
                break
        if chosen_game == None:
            continue
        user_id = user_reviews['steamid'][i]
        rating = user_reviews['voted_up'][i]
        review = user_reviews['review'][i] if user_reviews['review'][i] else ''
        hours_played = user_reviews['playtime_forever'][i]
        adquired = hours_played > 0
        reviews.append(Review(user_id, chosen_game, rating, review, adquired, hours_played))
    return games, reviews
    

class Data:
    def __init__(self):
        self.games, self.reviews = load_info()
        self.model, self.vectorizer = build_model(evaluate=True)
        self.set_all_users()#self.users
        self.review_sentiment = self.get_review_sentiment(self.reviews)
        self.game_corpus = {game.name: game.description for game in self.games}
    
    def set_all_users(self):
        users = {}
        for review in tqdm(self.reviews, desc="Setting Users"):
            if review.user_id not in users:
                users[review.user_id] = []
            users[review.user_id].append(review)
        self.users = users
    
    def get_game(self, game_name):
        '''
        Get the game with the given name.
        
        Args:
            game_name (str): Name of the game to get.
            
        Returns:
            Game: Game with the given name.
        '''
        for game in self.games:
            if game.name == game_name:
                return game
        return None

    def get_most_adquired_games(self, n):
        '''
        Get the n most adquired games (games free or bought that have been played at least once).
        
        Args:
            n (int): Amount of games to return.
            
        Returns:
            list: List of tuples with the game name and the amount of users that have adquired it (for free or bought).
        '''
        most_adquired_games = {}
        for game in tqdm(self.games, desc="Getting Most Adquired Games"):
            adquired = 0
            for review in self.reviews:
                if review.game.name == game.name and review.game_adquired:
                    adquired += 1
            most_adquired_games[game.name] = adquired
        most_adquired_games = sorted(most_adquired_games.items(), key=lambda x: x[1], reverse=True)
        return most_adquired_games[:n]
    
    def total_adquired_games(self):
        '''
        Get the total amount of adquired games.
        
        Returns:
            int: Total amount of adquired games.
        '''
        adquired_games = self.get_most_adquired_games(len(self.games))
        return len(adquired_games)
    
    def most_bought_games(self, n):
        '''
        Get the n most bought games.
        
        Args:
            n (int): Amount of games to return.
            
        Returns:
            list: List of tuples with the game name, the amount of users that have bought it and the total of money earned by the game.
        '''
        print(f"Getting the {n} most bought games...")
        most_bought_games = []
        users = []
        for game in tqdm(self.games, desc="Getting Most Bought Games"): 
            bought = 0
            for review in self.reviews:
                if review.game.name == game.name and review.bougth and review.user_id not in users:
                    bought += 1
                    users.append(review.user_id)
            most_bought_games.append((game.name, bought, bought * game.price))
        most_bought_games = sorted(most_bought_games.items(), key=lambda x: x[1], reverse=True)
        print("Complete!!")
        return most_bought_games[:n]
    
    def total_bought_games(self):
        '''
        Get the total amount of bought games.
        
        Returns:
            int: Total amount of bought games.
        '''
        bought_games = self.most_bought_games(len(self.games))
        return len(bought_games)
    
    def most_played_games(self, n):
        '''
        Get the games with more hours played in total.
        
        Args:
            n (int): Amount of games to return.
            
        Returns:
            list: List of tuples with the game name and the amount of hours played
        
        '''
        most_played_games = {}
        for game in tqdm(self.games, desc="Getting Most Played Games"):
            hours_played = 0
            for review in self.reviews:
                if review.game.name == game.name:
                    hours_played += review.hours_played
            most_played_games[game.name] = hours_played
        most_played_games = sorted(most_played_games.items(), key=lambda x: x[1], reverse=True)
        return most_played_games[:n]
    
    def total_hours_played(self):
        '''
        Get the total amount of hours played.
        
        Returns:
            int: Total amount of hours played.
        '''
        most_played_games = self.most_played_games(len(self.games))
        return sum([game[1] for game in most_played_games])
    
    def get_most_popular_tags(self, n=None):
        '''
        Get the n most popular tags.
        
        Args:
            n (int): Amount of tags to return.
            
        Returns:
            list: List of tuples with the tag name and the amount of games that have it.
        '''
        tags = {}
        for review in tqdm(self.reviews, desc="Getting Most Popular Tags"):
            for tag in review.game.tags:
                if tag not in tags:
                    tags[tag] = 0
                tags[tag] += 1
        tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
        return tags[:n] if n else tags
    
    def get_most_popular_genres(self, n=None):
        '''
        Get the n most popular genres.
        
        Args:
            n (int): Amount of genres to return.
            
        Returns:
            list: List of tuples with the genre name and the amount of games that have it.
        '''
        genres = {}
        for review in tqdm(self.reviews, desc="Getting Most Popular Genres"):
            for genre in review.game.genres:
                if genre not in genres:
                    genres[genre] = 0
                genres[genre] += 1
        genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
        return genres[:n] if n else genres
    
    def get_review_sentiment(self, review):
        '''
        Get the sentiment of the reviews for each game.
        
        Args:
            review (str): Review to analyze.
            
        Returns:
            int: Sentiment of the review.
        '''
        games = {}
        for review in tqdm(self.reviews, desc="Getting Review Sentiment"):
            if review.review:
                games[review.game.name] = []
            try:
                games[review.game.name].append(preprocess_text(review.review))
            except:
                #Existe la review pero no el juego. Se debe borrar las reviews de ese juego para evitar errores.
                #Eliminar la actual review de self.reviews
                self.reviews.remove(review)
        games = {game: sum(self.model.predict(self.vectorizer.transform(reviews))) / len(reviews) for game, reviews in games.items()}
        games = sorted(games.items(), key=lambda x: x[1], reverse=True)
        return games
                
    
    def games_with_most_positive_reviews(self, n):
        '''
        Get the games with the most positive reviews.
        
        Args:
            n (int): Amount of games to return.
            
        Returns:
            list: List of tuples with the game name and the average sentiment of the reviews.
        '''
        try:
            reviews = self.review_sentiment[:n] if n else self.review_sentiment
        except:
            reviews = self.get_review_sentiment(self.reviews)
        return reviews[:n] if n else reviews
    
    def games_with_most_negative_reviews(self, n):
        '''
        Get the games with the most negative reviews.
        
        Args:
            n (int): Amount of games to return.
            
        Returns:
            list: List of tuples with the game name and the average sentiment of the reviews.
        '''
        try:
            reviews = self.review_sentiment[-n:] if n else self.review_sentiment
        except:
            reviews = self.get_review_sentiment(self.reviews)
        return reviews[-n:] if n else reviews
    
    def get_most_similar_games(self, game_name, n=None):
        '''
        Get the n most similar games to the given game.
        
        Args:
            game_name (str): Name of the game to compare.
            n (int): Amount of games to return.
        
        Returns:
            list: List of tuples with the game name, similarity and the description.
        '''
        corpus = list(self.game_corpus.values())
        query = self.game_corpus[game_name]
        
        if n:
            texts = similarity.search(corpus, query, cant_docs=n)
        else:
            texts = similarity.search(corpus, query)# default cant_docs=10
        
        result = []
        for i, sim, desc in texts:
            result.append((list(self.game_corpus.keys())[i], sim, desc))
        
        return result
            
    # def get_users_alike_by_tags(self, user_id, n=10):
    #     '''
    #     Get the users that have made the same buys as the given user.
        
    #     Args:
    #         user_id (str): Id of the user to compare.
            
    #     Returns:
    #         list: List of users that have made the same buys.
    #     '''
    #     users_alike = []
    #     game_tags = []
    #     reviews = self.users[user_id]
    #     for review in reviews:
    #         game = self.get_game(review.game)
    #         for tag in game.tags:
    #             if tag not in game_tags:
    #                 game_tags.append(tag)
            
    #     for user in self.users:
    #         if user.user_id != user_id:
    #             user_tags = []
    #             for review in self.users[user]:
    #                 game = self.get_game(review.game)
    #                 for tag in game.tags:
    #                     if tag not in user_tags:
    #                         user_tags.append(tag)
    #                 inter = len(set(game_tags).intersection(user_tags))
    #             if inter > 0:
    #                 users_alike.append(user)

    #     users_alike = sorted(users_alike, key=lambda x: x.user_id, reverse=True)
                    
    #     return users_alike
    
    def get_users_alike_by_bought_games(self, user_id, n=10):
        '''
        Get the users that have made the same buys as the given user.
        
        Args:
            user_id (str): Id of the user to compare.
            
        Returns:
            list: List of users that have made the same buys.
        '''
        users_alike = []
        games = []
        reviews = self.users[user_id]
        for review in reviews:
            if review.bougth:
                games.append(review.game)
            
        for user in self.users:
            if user != user_id:
                user_games = []
                for review in self.users[user]:
                    if review.game_adquired:
                        user_games.append(review.game)
                inter = len(set(games).intersection(user_games))
                if inter > 0:
                    users_alike.append(user)

        users_alike = sorted(users_alike, key=lambda x: x, reverse=True)
                    
        if n:
            return users_alike[:n]
        return users_alike
    
    def recommend_games_using_users_alike(self, user_id, users_alike=None, n=10):
        '''
        Recommend games to the given user based on the games that the users that have made the same buys as him have bought.
        
        Args:
            user_id (str): Id of the user to recommend games.
            n (int): Amount of games to return.
            
        Returns:
            list: List of games recommended.
        '''
        if not users_alike:
            users_alike = self.get_users_alike_by_bought_games(user_id)
        user_games = []
        for review in self.users[user_id]:
            if review.game_adquired:
                user_games.append(review.game)
        
        # De los juegos q los users_alike tienen y el user_id no, recomendar los q mas se han comprado.
        recommended_games = {}
        for user in users_alike:
            for review in self.users[user]:
                if review.game_adquired and review.game not in user_games:
                    if review.game not in recommended_games:
                        recommended_games[review.game] = 0
                    recommended_games[review.game] += 1
        recommended_games = sorted(recommended_games.items(), key=lambda x: x[1], reverse=True)
        
        return recommended_games[:n]
        
        #Tnego los usuarios que han comprado los mismos juegos que el usuario_id
        #y los juegos que han comprado que el usuario_id no ha comprado.
        #Ordenar estos juegos segun la cantidad de users_alike q lo han adquirido.
        
        
        
        
        
    
        
         

def get_products():
    products = []
    for i in tqdm(range(0, CANTIDAD), desc="Getting Products"):
        if corpus['product_title'][i] not in products:
            products.append(corpus['product_title'][i])
    return products

def get_products_info(products):
    sells = {}
    ratings = {}
    reviews = {}
    model, vectorizer = build_model(evaluate=True)
    for product in tqdm(products, desc="Getting Products Info"):
        if product not in ratings:
            ratings[product] = []
        if product not in sells:
            sells[product] = 0
        if product not in reviews:
            reviews[product] = []
        for i in tqdm(range(0, CANTIDAD), desc=f"Collecting data for {product}", leave=False):
            if corpus['product_title'][i] == product and corpus['verified_purchase'][i] == 'Y':
                sells[product] += 1
            if corpus['product_title'][i] == product:
                ratings[product].append(corpus['star_rating'][i])
            if corpus['product_title'][i] == product and corpus['review_body'][i]:
                reviews[product].append(preprocess_text(corpus['review_body'][i]))
    for product in products:
        ratings[product] = sum(ratings[product]) / len(ratings[product]) if ratings[product] else 0
        reviews[product] = sum(model.predict(vectorizer.transform(reviews[product]))) / len(reviews[product]) if reviews[product] else 0
    sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    reviews = sorted(reviews.items(), key=lambda x: x[1], reverse=True)
    return sells, ratings, reviews

# def get_sells(products):
#     sells = {}
#     for product in tqdm(products, desc="Calculating Sells"):
#         if product not in sells:
#             sells[product] = 0
#         for i in tqdm(range(0, CANTIDAD), desc=f"Counting sells for {product}", leave=False):
#             if corpus['product_title'][i] == product and corpus['verified_purchase'][i] == 'Y':
#                 sells[product] += 1
#     sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)
#     return sells

def most_popular_products(sells, amount):
    # 10 more popular products
    popular_products = sells[:amount]
    return popular_products

# def get_ratings(products):
#     ratings = {}
#     for product in tqdm(products, desc="Getting Ratings"):
#         if product not in ratings:
#             ratings[product] = []
#         for i in tqdm(range(0, CANTIDAD), desc=f"Collecting ratings for {product}", leave=False):
#             if corpus['product_title'][i] == product:
#                 ratings[product].append(corpus['star_rating'][i])
#     for product in products:
#         ratings[product] = sum(ratings[product]) / len(ratings[product]) if ratings[product] else 0
#     ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
#     return ratings

def best_rated_products(ratings, amount):
    # 10 best rated products
    best_rated_products = ratings[:amount]
    return best_rated_products

def worst_rated_products(ratings, amount):
    # 10 worst rated products
    worst_rated_products = ratings[-amount:]
    return worst_rated_products

# def get_reviews_sentiment(products):
#     model_, vectorizer = build_model(evaluate=True)
#     reviews = {}
#     for product in tqdm(products, desc="Getting Reviews Sentiment"):
#         if product not in reviews:
#             reviews[product] = []
#         for i in tqdm(range(0, CANTIDAD), desc=f"Collecting reviews for {product}", leave=False):
#             if corpus['product_title'][i] == product:
#                 reviews[product].append(preprocess_text(corpus['review_body'][i]))
#     for product in products:
#         reviews[product] = sum(model_.predict(vectorizer.transform(reviews[product]))) / len(reviews[product]) if reviews[product] else 0
#     reviews = sorted(reviews.items(), key=lambda x: x[1], reverse=True)
#     return reviews

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