import streamlit as st
import pickle
import pandas as pd
import requests

# ====================== CONFIG ======================
TMDB_API_KEY = "25cbbbdc29d88d8341ac297338d025f6"  # 🔑 Replace with your TMDb API key

st.set_page_config(page_title="Movie Recommender", layout="wide")

# ====================== STYLING ======================
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .main-title {
        text-align: center;
        font-size: 3em;
        color: #FF4B4B;
        margin-bottom: 30px;
        font-weight: bold;
    }
    .movie-title {
        text-align: center;
        font-size: 1.1em;
        font-weight: 600;
        color: #EAEAEA;
        margin-top: 10px;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5em 1.5em;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF1E1E;
        color: white;
        transform: scale(1.05);
    }
    img {
        border-radius: 15px;
        transition: 0.3s;
    }
    img:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ====================== FETCH POSTER ======================
def fetch_poster_by_title(title):
    """Fetch poster URL from TMDb by movie title (first result only)."""
    try:
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": title}
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")
    return "https://via.placeholder.com/500x750?text=No+Poster"

# ====================== RECOMMENDER ======================
def recommend(movie):
    """Return recommended movies and their poster URLs."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster_by_title(title))
    return recommended_movies, recommended_posters

# ====================== LOAD DATA ======================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ====================== UI ======================
st.markdown('<div class="main-title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Select a movie you like:",
    movies['title'].values,
    index=0,
    key="movie_selector"
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Make horizontal responsive layout
    num_recs = len(recommendations)
    cols = st.columns(num_recs)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{recommendations[idx]}</div>", unsafe_allow_html=True)
