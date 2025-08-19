# app.py

import streamlit as st
import pandas as pd

from config import ALL_GENRES
from recommender import load_data_and_model, get_recommendations
from ui import set_video_background, display_recommendations_featured

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# --- STATIC BACKGROUND ---
# This now sets the background to bg.mp4 every time, simplifying the logic.
set_video_background("bg.mp4")

# Initialize session state for recommendations if it doesn't exist
if 'recs_df' not in st.session_state:
    st.session_state.recs_df = pd.DataFrame()

df, cosine_sim = load_data_and_model()

# --- SIDEBAR ---
st.sidebar.header("Find Your Next Movie 🍿")

# Similarity Recommender
st.sidebar.subheader("Find Similar Movies")
movie_titles = df['title'].tolist()
selected_movie_sim = st.sidebar.selectbox("Choose a movie you like:", movie_titles)
if st.sidebar.button("Recommend Similar"):
    st.session_state.recs_df = get_recommendations(selected_movie_sim, cosine_sim, df)

# Genre Discovery
st.sidebar.subheader("Discover by Genre")
selected_genre = st.sidebar.selectbox("Choose a genre:", ALL_GENRES)
if st.sidebar.button("Find by Genre"):
    genre_recs = df[df['tags'].str.contains(selected_genre.replace(" ",""))].sample(n=9, replace=True) 
    st.session_state.recs_df = genre_recs

# --- MAIN PAGE ---
st.title("Movie Recommender")

if not st.session_state.recs_df.empty:
    display_recommendations_featured(st.session_state.recs_df)
else:
    st.info("Select a movie or genre from the sidebar to get started!")