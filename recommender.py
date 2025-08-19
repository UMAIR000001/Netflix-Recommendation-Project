# recommender.py

import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import constants from the config file
from config import API_KEY, PLACEHOLDER_IMAGE_URL

@st.cache_resource
def load_data_and_model():
    """Loads the dataset, trains the model, and returns them."""
    df = pd.read_csv('cleaned_movies_with_details.csv')
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['tags'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return df, cosine_sim

def get_recommendations(title, cosine_sim_matrix, dataframe, num_recommendations=10):
    """Gets similarity-based movie recommendations."""
    idx = dataframe.index[dataframe['title'] == title][0]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return dataframe.iloc[movie_indices]

def fetch_poster(title):
    """Fetches a movie poster URL from the TMDb API."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.exceptions.RequestException:
        return PLACEHOLDER_IMAGE_URL
    return PLACEHOLDER_IMAGE_URL