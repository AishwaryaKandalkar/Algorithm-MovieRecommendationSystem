import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import requests

st.set_page_config(page_title="Movie Recommender System", page_icon=":tada", layout="wide")

hide_menu_style = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden; }
</style>
"""

st.markdown(hide_menu_style, unsafe_allow_html=True)

from typing import DefaultDict, List
from collections import defaultdict, deque
from Data_Management import StoreUserData, ReadUserData
globalUserData: DefaultDict[str, List[str]] = defaultdict(deque)


UserData: DefaultDict[str, List[str]] = defaultdict(deque)
# UserData["abc"]=['xyz']
# st.write(UserData["abc"])
class User:
    # initialize
    def __init__(self):
        self.Username = ""
        self.watched = ""
        # self.UserData: DefaultDict[str, List[str]] = defaultdict(deque)

    def setName(self, name):
        self.Username = name
        # self.UserData[name] = []

    def getName(self):
        return self.Username

    def setActivity(self, movie_name):
        self.watched = movie_name
        tempname = self.getName()
        # st.write(globalUserData[tempname])
        ##st.write(globalUserData[tempname])



    def getActivity(self):
        return self.Username, self.watched


selected = option_menu(menu_title="Movie Recommendation System", options=["Login", "The Movie Store"],
                       default_index=1, )

p1 = User()
if selected == "Login":
    st.header("Login")
    x = st.text_input('enter your user id', value="", max_chars=25)

    if st.button('login', on_click=None):
        p1.setName(x)
        #st.write(p1)
        filename = x + ".txt"
        StoreUserData(x, filename)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


movies = pickle.load(open('movie_list.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

with st.container():
    st.title('The Movie Store')
    st.write(" This page shows movie recommendation")

selected_movie = st.selectbox('Type or select a movie from the dropdown', movies['title'].values)

if st.button('Show Recommendation'):
    # recommendations = recommend(selected_movie)

    p1.setActivity(selected_movie)
    #st.write(p1.Username())

    tempname,temp_movie_name= p1.getActivity()

    filename = tempname + ".txt"
    StoreUserData(temp_movie_name, filename)

    # for i in recommendations:
    # st.write(i)
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

with st.container():
    st.write("---")
    newreleases, popularmovies, blockblusters = st.columns(3)
    with newreleases:
        st.header("New Releases")
        new_movies = pickle.load(open('new_movie_list.pkl', 'rb'))
        new_movie_list = new_movies['title'].values
        count = 0
        for values1 in new_movies['title']:
            if count < 10:
                st.write(values1)
            count = count + 1
    with popularmovies:
        st.header("Popular Movies")
        popular_movies = pickle.load(open('popular_movie_list.pkl', 'rb'))
        popular_movie_list = popular_movies['title'].values
        count = 0
        for values in popular_movies['title']:
            if count < 10:
                st.write(values)
            count = count + 1

    with blockblusters:
        st.header("Block blusters")
        blockbuster_movies = pickle.load(open('blockbuster_movie_list.pkl', 'rb'))
        blockbuster_movie_list = blockbuster_movies['title'].values
        count = 0
        for values1 in blockbuster_movies['title']:
            if count < 10:
                st.write(values1)
            count = count + 1



