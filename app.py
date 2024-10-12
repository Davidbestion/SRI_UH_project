import streamlit as st
import pandas as pd
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

st.markdown("## Generos mas populares")
genres = data.get_most_popular_genres(10)
df = pd.DataFrame(list(genres), columns=['Genero', 'Popularidad'])
st.dataframe(df)

st.markdown("## Juegos con las resenas mas positivas")
games_reviews = data.games_with_most_positive_reviews(10)
df = pd.DataFrame(list(games_reviews), columns=['Juego', 'Resenas positivas'])
st.dataframe(df)

st.markdown("## Juegos con las resenas mas negativas")
games_reviews = data.games_with_most_negative_reviews(10)
df = pd.DataFrame(list(games_reviews), columns=['Juego', 'Resenas negativas'])
st.dataframe(df)


