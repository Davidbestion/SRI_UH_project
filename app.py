import streamlit as st
import pandas as pd
# import src.similarity   # from similarity.py
from main import main

# Cache the main function
@st.cache_data
def get_data():
    with st.spinner('Cargando datos...'):
        data = main()
        return data
    
data = get_data()


st.title("Proyecto de SRI")
st.markdown("**Autor**: David Sanchez Iglesias")

search_query = st.text_input('Introduzca un juego o un codigo de usuario de Steam')

if search_query:
    if search_query.isnumeric():
        user_id = search_query
        if user_id and user_id in data.users:
            users_alike = data.get_users_alike_by_bought_games(user_id)#, n=10)
            if users_alike:
                st.write("Usuarios que han comprado los mismos juegos que", user_id)
                for u in users_alike:
                    st.write(u)
            recommended_games = data.recommend_games_using_users_alike(user_id, users_alike)
            if recommended_games:
                st.write("Juegos recomendados para", user_id)
                for g in recommended_games:
                    st.write(g)
    else:
        game = data.get_game(search_query)
        if game:
            games = data.get_most_similar_games(game.name)#, n=10)
            if games:
                st.write("Juegos similares a", game)
                for g in games:
                    st.write(g)
        else:
            st.write("No se ha encontrado el juego")
# st.markdown("## Cuantas personas de entre todas las qie hicieron reseñas, adquirieron cada juego.")
# acquisitions = data.get_most_adquired_games(10)
# #acquisitions es una tupla de la forma (nombre_juego, numero_ventas)
# # games = []
# # values = []
# # for element in acquisitions:
# #     games.append(element[0])
# #     values.append(element[1])
# df = pd.DataFrame(list(acquisitions), columns=['Juego', 'Adquisiciones'])
# st.dataframe(df)

# st.markdown("De los juegos anteriores, algunos tienen que ser comprados para poder jugarlos. De estos ultimos, cuales son los que mas se han adquirido (los juegos mas comprados teniendo como referencia las re)")
# # Sells es un diccionario de la forma {nombre_juego: numero_ventas}
# sells = data.most_bought_games(10)
# # games = []
# # values = []
# # money = []
# # for element in sells:
# #     games.append(element[0])
# #     values.append(element[1])
# #     money.append(element[2])
# df = pd.DataFrame(list(sells), columns=['Juego', 'Ventas', 'Dinero'])
# st.dataframe(df)

# st.markdown("## Tags mas populares")
# tags = data.get_most_popular_tags(10)
# df = pd.DataFrame(list(tags), columns=['Tag', 'Popularidad'])
# st.dataframe(df)

# st.markdown("## Generos mas populares")
# genres = data.get_most_popular_genres(10)
# df = pd.DataFrame(list(genres), columns=['Genero', 'Popularidad'])
# st.dataframe(df)

st.markdown("## Juegos con las resenas mas positivas")
games_reviews = data.games_with_most_positive_reviews(10)
df = pd.DataFrame(list(games_reviews), columns=['Juego', 'Resenas positivas'])
st.dataframe(df)

st.markdown("## Juegos con las resenas mas negativas")
games_reviews = data.games_with_most_negative_reviews(10)
df = pd.DataFrame(list(games_reviews), columns=['Juego', 'Resenas negativas'])
st.dataframe(df)




