# ui.py

import streamlit as st
import ast
from recommender import fetch_poster

def set_professional_dark_theme():
    """
    Sets a professional dark theme with corrected text colors and modern card styles.
    """
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

        /* --- Base App Styling --- */
        .stApp {{
            background-color: #121212;
            font-family: 'Lato', sans-serif;
        }}

        /* --- Animated Title Text --- */
        @keyframes glow {{
            0% {{ text-shadow: 0 0 5px #00aaff, 0 0 10px #00aaff; }}
            50% {{ text-shadow: 0 0 10px #00aaff, 0 0 20px #00aaff; }}
            100% {{ text-shadow: 0 0 5px #00aaff, 0 0 10px #00aaff; }}
        }}

        .stTitle, .stHeader {{
            animation: glow 3s ease-in-out infinite;
            color: #FFFFFF !important;
        }}

        /* --- Card Styling --- */
        .featured-movie-container, .grid-card {{
            background: #1E1E1E;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #2F2F2F;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            transition: all 0.3s ease;
            /* ** THE FIX IS HERE ** */
            color: #E0E0E0; /* Forces all text inside the card to be light gray */
        }}

        .featured-movie-container:hover, .grid-card:hover {{
            border-color: #00aaff;
            box-shadow: 0 12px 24px rgba(0, 170, 255, 0.2);
        }}

        .featured-title {{
            font-size: 2.2rem;
            font-weight: 700;
            color: #FFFFFF; /* White for featured title */
        }}

        .grid-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #FFFFFF; /* White for grid titles */
            margin-bottom: 0.5rem;
        }}

        .genres-text {{
            color: #AAAAAA;
            font-style: italic;
            margin-bottom: 1rem;
        }}

        .overview-text {{
            color: #BDBDBD;
            font-size: 0.9rem;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def display_recommendations_featured(recs_df):
    """
    Displays recommendations with one featured movie and a detailed grid for the rest.
    """
    if recs_df.empty:
        st.warning("No recommendations to display.")
        return

    # --- FEATURED RECOMMENDATION ---
    featured_movie = recs_df.iloc[0]
    poster_url = fetch_poster(featured_movie['title'])

    st.markdown("<div class='featured-movie-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster_url, use_container_width=True)
    with col2:
        st.markdown(f"<h1 class='featured-title'>{featured_movie['title']}</h1>", unsafe_allow_html=True)
        try:
            genres_list = ast.literal_eval(featured_movie['genres'])
            st.markdown(f"<p class='genres-text'>{', '.join(genres_list)}</p>", unsafe_allow_html=True)
        except:
            pass 
        st.write(f"<p class='overview-text'>{featured_movie['overview']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- GRID OF OTHER RECOMMENDATIONS ---
    other_recs = recs_df.iloc[1:]
    if not other_recs.empty:
        st.subheader("More Suggestions For You")
        
        num_columns = 3
        cols = st.columns(num_columns)
        
        for i, row in enumerate(other_recs.iterrows()):
            index, data = row
            with cols[i % num_columns]:
                poster_url = fetch_poster(data['title'])
                
                # We can build the entire card's HTML for better control
                genres_html = ""
                try:
                    genres_list = ast.literal_eval(data['genres'])
                    genres_html = f"<p class='genres-text' style='font-size:0.8rem; margin-bottom: 0.5rem;'>{', '.join(genres_list)}</p>"
                except:
                    pass
                
                overview_text = (data['overview'][:120] + '...') if len(data['overview']) > 120 else data['overview']
                
                st.markdown(f"""
                <div class='grid-card'>
                    <img src="{poster_url}" style="width: 100%; border-radius: 7px;">
                    <p class='grid-title'>{data['title']}</p>
                    {genres_html}
                    <p class='overview-text'>{overview_text}</p>
                </div>
                """, unsafe_allow_html=True)