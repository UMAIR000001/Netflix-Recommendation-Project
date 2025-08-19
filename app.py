# app.py

import streamlit as st

# Import functions from our other files
from config import ALL_GENRES
from recommender import load_data_and_model, get_recommendations
# Updated function names are imported here
from ui import set_professional_dark_theme, display_recommendations_featured

# --- PAGE CONFIG AND INITIALIZATION ---
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)
# Call the new background function
set_professional_dark_theme()
df, cosine_sim = load_data_and_model()

# --- SIDEBAR (No changes here) ---
st.sidebar.header("Find Your Next Movie 🍿")
# Similarity Recommender
st.sidebar.subheader("Find Similar Movies")
movie_titles = df['title'].tolist()
selected_movie_sim = st.sidebar.selectbox("Choose a movie you like:", movie_titles)
if st.sidebar.button("Recommend Similar"):
    st.session_state['recs_df'] = get_recommendations(selected_movie_sim, cosine_sim, df)
    st.session_state['header'] = f"Because you liked '{selected_movie_sim}':"
# Genre Discovery
st.sidebar.subheader("Discover by Genre")
selected_genre = st.sidebar.selectbox("Choose a genre:", ALL_GENRES)
if st.sidebar.button("Find by Genre"):
    genre_recs = df[df['tags'].str.contains(selected_genre.replace(" ",""))].sample(n=9, replace=True) 
    st.session_state['header'] = f"Top picks in '{selected_genre}':"
    st.session_state['recs_df'] = genre_recs

# --- MAIN PAGE (No changes here) ---
st.title("Movie Recommender")
if 'header' in st.session_state:
    st.header(st.session_state['header'])
    display_recommendations_featured(st.session_state['recs_df'])
else:
    st.info("Select a movie or genre from the sidebar to get started!")