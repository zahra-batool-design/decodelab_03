import os
os.system("pip install scikit-learn numpy")

import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ... rest of your code remains exactly the same


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Dataset
MOVIES_DATABASE = [
    {"title": "The Matrix", "genres": "Sci-Fi Action Cyberpunk"},
    {"title": "Inception", "genres": "Sci-Fi Thriller Action"},
    {"title": "Die Hard", "genres": "Action Thriller"},
    {"title": "Toy Story", "genres": "Animation Comedy Family"},
    {"title": "The Hangover", "genres": "Comedy"},
    {"title": "Interstellar", "genres": "Sci-Fi Drama Space"},
    {"title": "Superbad", "genres": "Comedy Romance"},
]

# Extract all unique genres for our dropdown menu option
ALL_TAGS = sorted(list(set(" ".join([m["genres"] for m in MOVIES_DATABASE]).split())))

# 2. Recommendation Logic Function
def get_recommendations(user_interests_string, top_n):
    if not user_interests_string:
        return []
        
    movie_genres = [movie["genres"] for movie in MOVIES_DATABASE]
    all_texts = [user_interests_string] + movie_genres
    unique_genres = list(set(" ".join(all_texts).split()))
    
    def text_to_vector(text):
        words = text.split()
        return [1 if genre in words else 0 for genre in unique_genres]
    
    user_vector = np.array(text_to_vector(user_interests_string)).reshape(1, -1)
    movie_vectors = np.array([text_to_vector(mg) for mg in movie_genres])
    
    similarity_scores = cosine_similarity(user_vector, movie_vectors).flatten()
    
    scored_movies = []
    for index, score in enumerate(similarity_scores):
        scored_movies.append({
            "title": MOVIES_DATABASE[index]["title"],
            "genres": MOVIES_DATABASE[index]["genres"],
            "score": round(float(score), 2)
        })
    
    scored_movies.sort(key=lambda x: x["score"], reverse=True)
    return scored_movies[:top_n]


# 3. Streamlit User Interface Configuration
st.set_page_config(page_title="AI Movie Recommender", page_icon="🎬", layout="centered")

# App Header
st.title("🎬 AI Movie Recommendation Engine")
st.markdown("Select your favorite genres below, and our vector-matching AI will find the best movies for you.")
st.write("---")

# Sidebar Controls for a clean user interface layout
st.sidebar.header("Configuration Options")
top_n_slider = st.sidebar.slider("Number of recommendations:", min_value=1, max_value=5, value=3)

# Main input: A beautiful multi-select box
selected_tags = st.multiselect(
    "What elements or genres are you looking for?",
    options=ALL_TAGS,
    placeholder="Choose one or more genres..."
)

# Action Button
if st.button("Generate Recommendations", type="primary"):
    if not selected_tags:
        st.warning("Please select at least one genre tag first!")
    else:
        # Convert list of tags into a single space-separated string for our engine
        user_input_string = " ".join(selected_tags)
        
        with st.spinner("Analyzing profile vectors..."):
            recommendations = get_recommendations(user_input_string, top_n=top_n_slider)
        
        st.success("Analysis complete! Here are your matches:")
        
        # Display results in styled cards
        has_valid_match = False
        for i, rec in enumerate(recommendations, 1):
            if rec['score'] > 0:
                has_valid_match = True
                
                # Visual container for each movie card
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(f"{i}. {rec['title']}")
                        # Convert genres back to individual small badges
                        badges = "".join([f"`{g}` " for g in rec['genres'].split()])
                        st.markdown(f"**Tags:** {badges}")
                    
                    with col2:
                        # Display similarity as a clear percentage statistic metric
                        match_percentage = int(rec['score'] * 100)
                        st.metric(label="Match Score", value=f"{match_percentage}%")
                        
        if not has_valid_match:
            st.info("No explicit matches found for that specific combination. Try broader tags!")