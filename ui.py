# ui.py

import streamlit as st
import ast
import base64
from recommender import fetch_poster

def set_video_background(video_file):
    """
    Sets a local video as the background, ensuring it covers the full screen.
    """
    try:
        with open(video_file, "rb") as f:
            video_bytes = f.read()
        
        video_b64 = base64.b64encode(video_bytes).decode()
        
        safe_video_id = video_file.replace('.', '-')
        
        st.markdown(
            f"""
            <style>
            #bg-video-{safe_video_id} {{
                position: fixed;
                top: 50%;
                left: 50%;
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                z-index: -2;
                transform: translateX(-50%) translateY(-50%);
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background-color: rgba(0,0,0,0.7);
                z-index: -1;
            }}
            .stApp > div {{
                z-index: 1;
            }}
            [data-testid="stAppViewContainer"] > .main {{
                background-color: transparent;
            }}
            </style>
            
            <video autoplay loop muted id="bg-video-{safe_video_id}">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Video file '{video_file}' not found.")

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

    st.markdown("### Top Recommendation")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster_url, use_container_width=True)
    with col2:
        st.markdown(f"**{featured_movie['title']}**")
        try:
            genres_list = ast.literal_eval(featured_movie['genres'])
            st.markdown(f"*{', '.join(genres_list)}*")
        except: pass
        st.write(featured_movie['overview']) # Full overview for featured

    # --- GRID OF OTHER RECOMMENDATIONS ---
    other_recs = recs_df.iloc[1:]
    if not other_recs.empty:
        st.markdown("---")
        st.subheader("More Suggestions")
        
        num_columns = 3
        cols = st.columns(num_columns)
        
        for i, row in enumerate(other_recs.iterrows()):
            index, data = row
            with cols[i % num_columns]:
                st.image(fetch_poster(data['title']), use_container_width=True)
                st.markdown(f"**{data['title']}**")
                
                # --- NEW: ADDING DESCRIPTION TO GRID CARDS ---
                # Truncate overview for the grid view to keep it neat
                overview_text = (data['overview'][:100] + '...') if len(data['overview']) > 100 else data['overview']
                st.write(overview_text)