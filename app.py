import streamlit as st
import pickle
import requests

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS (NETFLIX STYLE)
# ---------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

h1 {
    text-align: center;
    color: #E50914;
    font-size: 50px;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 250px;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ff1f1f;
    transform: scale(1.05);
}

img {
    border-radius: 15px;
    transition: 0.3s;
}

img:hover {
    transform: scale(1.03);
}

.movie-card {
    background-color: #1c1c1c;
    padding: 10px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------------------------------------
# FETCH MOVIE DETAILS
# ---------------------------------------------------

def fetch_movie_details(movie_title):

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=e53f008f"

    data = requests.get(url).json()

    poster = data.get('Poster', '')
    rating = data.get('imdbRating', 'N/A')
    year = data.get('Year', 'N/A')
    genre = data.get('Genre', 'N/A')

    trailer = f"https://www.youtube.com/results?search_query={movie_title}+{year}+official+trailer"

    return poster, rating, year, genre, trailer

# ---------------------------------------------------
# RECOMMENDATION FUNCTION
# ---------------------------------------------------

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_similarity = []

    for i in movies_list:

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_similarity.append(round(i[1] * 100))

    return recommended_movies, recommended_similarity

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🎬 AI Movie Recommendation System")

# ---------------------------------------------------
# TRENDING SECTION
# ---------------------------------------------------

st.markdown("## 🔥 Trending Movies")

trending_cols = st.columns(5)

trending_movies = [
    "Avatar",
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Avengers: Endgame"
]

for idx, movie in enumerate(trending_movies):

    poster, rating, year, genre, trailer = fetch_movie_details(movie)

    with trending_cols[idx]:

        st.image(poster)

        st.markdown(f"**{movie}**")

# ---------------------------------------------------
# SEARCH SECTION
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    "<h3 style='color:white;'>🔍 Search or Select a Movie</h3>",
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    "",
    movies['title'].values,
    placeholder="Type or select a movie..."
)

# ---------------------------------------------------
# RECOMMEND BUTTON
# ---------------------------------------------------

if selected_movie_name and st.button("🔥 Recommend Movies"):

    recommendations, similarities = recommend(selected_movie_name)

    st.markdown("## 🎯 Recommended Movies")

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations):

        poster, rating, year, genre, trailer = fetch_movie_details(movie)

        with cols[idx]:

            st.image(poster)

            st.markdown(f"### {movie}")

            st.markdown(f"🔥 **{similarities[idx]}% Match**")

            st.markdown(f"⭐ IMDb: {rating}")

            st.markdown(f"📅 Year: {year}")

            st.markdown(f"🎭 Genre: {genre}")

            st.markdown(
                f'<a href="{trailer}" target="_blank">'
                f'<button style="background-color:#E50914; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">▶ Watch Trailer</button>'
                f'</a>',
                unsafe_allow_html=True
            )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    "<center>Made with ❤️ using Python, Streamlit, ML & AI</center>",
    unsafe_allow_html=True
)