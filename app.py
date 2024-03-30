import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3ec9006733e8f33d8399b889223e27b3"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w342/{poster_path}"  # Adjusted poster size to w342
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('E:\PycharmProjects\Movie_recommender_system\movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('E:\PycharmProjects\Movie_recommender_system\similarity.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie from the dropdown:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    max_length = max(len(movie) for movie in recommendations)
    col_width = max_length * 12  # Adjust this multiplier based on your preference

    st.write("Recommended Movies and Posters:")
    container = st.container()
    with container:
        for movie, poster in zip(recommendations, posters):
            st.write(movie)
            st.image(poster, width=150)  # Adjust the width of each poster
