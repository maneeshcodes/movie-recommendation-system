import streamlit as st
import pickle
import pandas as pd

# ---------------- Load Data ----------------
# Since app.py is inside src/, go one level up to access saved/
movies = pickle.load(open('saved/movies.pkl', 'rb'))
similarity = pickle.load(open('saved/similarity.pkl', 'rb'))

# If movies was saved as a dict, convert to DataFrame
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# ---------------- Recommend Function ----------------
def recommend(movie):
    """
    Given a movie title, return 5 recommended movie titles.
    """
    # Find index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get similarity scores for that movie
    distances = similarity[movie_index]
    
    # Sort movies by similarity score (descending) and skip the first (itself)
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]
    
    # Get movie titles
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    
    return recommended_movies

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("🎬 Movie Recommendation System")
st.write("Select a movie and get 5 similar movie recommendations.")

# Dropdown menu for movies
selected_movie = st.selectbox(
    "Choose a movie:",
    movies['title'].values
)

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0066ff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Recommend button
if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    
    st.subheader("Recommended Movies:")
    for i, movie in enumerate(recommendations, start=1):
        st.write(f"{i}. {movie}")
