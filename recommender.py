# The dataset the AI will search through
MOVIES_DATABASE = [
    {"title": "The Matrix", "genres": "Sci-Fi Action Cyberpunk"},
    {"title": "Inception", "genres": "Sci-Fi Thriller Action"},
    {"title": "Die Hard", "genres": "Action Thriller"},
    {"title": "Toy Story", "genres": "Animation Comedy Family"},
    {"title": "The Hangover", "genres": "Comedy"},
    {"title": "Interstellar", "genres": "Sci-Fi Drama Space"},
    {"title": "Superbad", "genres": "Comedy Romance"},
]
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations(user_interests, top_n=3):
    # 1. Extract all genres from the database
    movie_genres = [movie["genres"] for movie in MOVIES_DATABASE]
    
    # 2. Combine user input with database genres to find every unique word
    all_texts = [user_interests] + movie_genres
    unique_genres = list(set(" ".join(all_texts).split()))
    
    # 3. Helper function: Convert text string into a mathematical vector of 1s and 0s
    def text_to_vector(text):
        words = text.split()
        return [1 if genre in words else 0 for genre in unique_genres]
    
    # 4. Convert user interests and all movies into their vector forms
    user_vector = np.array(text_to_vector(user_interests)).reshape(1, -1)
    movie_vectors = np.array([text_to_vector(mg) for mg in movie_genres])
    
    # 5. Calculate Cosine Similarity (scores range from 0.0 to 1.0)
    similarity_scores = cosine_similarity(user_vector, movie_vectors).flatten()
    
    # 6. Pair the movies with their calculated similarity scores
    scored_movies = []
    for index, score in enumerate(similarity_scores):
        scored_movies.append({
            "title": MOVIES_DATABASE[index]["title"],
            "genres": MOVIES_DATABASE[index]["genres"],
            "score": round(float(score), 2)
        })
    
    # 7. Sort the list so the highest scoring movies are at the top
    scored_movies.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_movies[:top_n]
def main():
    print("====================================")
    print("      AI RECOMMENDATION SYSTEM      ")
    print("====================================\n")
    print("Available tags: Sci-Fi, Action, Cyberpunk, Thriller, Animation, Comedy, Family, Drama, Space, Romance\n")
    
    # Accept user input
    user_input = input("What kind of movies do you like? (Separate tags with spaces): ")
    
    print("\nProcessing your preferences against database...")
    recommendations = get_recommendations(user_input, top_n=3)
    
    print("\n============ YOUR TOP PICKS ============")
    has_matches = False
    
    for i, rec in enumerate(recommendations, 1):
        # Only show recommendations that have at least some match percentage
        if rec['score'] > 0:
            print(f"{i}. {rec['title']} | Match Score: {int(rec['score'] * 100)}%")
            print(f"   Genres: {rec['genres']}\n")
            has_matches = True
            
    if not has_matches:
        print("No matches found. Try using different keywords from the available tags list!")

if __name__ == "__main__":
    main()