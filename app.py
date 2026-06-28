import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown


# ---------------------- Poster Fetch Function ---------------------- #
def fetch_poster(movie_id):
    try:
        api_key = "d92bb7319efef44fb3d5bf348dd27f3e"

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

        response = requests.get(url, timeout=10)
        data = response.json()

        if "poster_path" in data and data["poster_path"]:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

        return "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"

    except Exception:
        return "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"


# ---------------------- Download Similarity File ---------------------- #
if not os.path.exists("similarity.pkl"):
    with st.spinner("Downloading recommendation model... Please wait (first run only)."):
        file_id = "1ZAmW2_1xK98VcuHywTSVBr6SS0FfFJ_m"
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, "similarity.pkl", quiet=False)


# ---------------------- Load Data ---------------------- #
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


# ---------------------- Recommendation Function ---------------------- #
def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# ---------------------- Streamlit UI ---------------------- #
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])