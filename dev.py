import json
from operator import itemgetter
import streamlit as st
from PIL import Image
from classifier import KNearestNeighbours

with open(r'fdata.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'ftitle.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)

def knn(test_point, k):
    target = [0 for item in movie_titles]
    model = KNearestNeighbours(data, target, test_point, k=k)

    model.fit()

    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    table = list()
    for i in model.indices:

        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table

if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    string = "Netflix - Watch TV Shows Online, Watch Movies Online"
    img = Image.open('./images/index.png')
    st.set_page_config(page_title='IMDb: Ratings, Reviews, and Where to Watch the Best Movies & TV Shows', page_icon=img, layout="centered",
                       initial_sidebar_state="expanded")

    #st.set_page_config(page_title=string, page_icon="https://play-lh.googleusercontent.com/TBRwjS_qfJCSj1m7zZB93FnpJM5fSpMA_wUlFDLxWAb45T9RmwBvQd5cWR5viJJOhkI")
    st.header('IMDB MOVIE RECOMMENDATION SYSTEM')
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/2560px-IMDB_Logo_2016.svg.png",
        width=450,)
    hide_st_style="""
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: visible;}
                footer:after{
                    background-color:#a873b0;
                    font-size:12px;
                    font-weight:5px;
                    height:30px;
                    margin:1rem;
                    padding:0.8rem;
                    content:'Copyright © 2022 : Akshat Sahay & Shaily Goyal';
                    display: flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                }
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    apps = ['--Select--', 'Movie based', 'Genres based']
    app_options = st.selectbox('Select application:', apps)
    img = Image.open('./images/favicon.png')

    if app_options == 'Movie based':
        movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write(
                    "You may select the movie and change the IMDb score of your choice.")
        else:
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[2]:
        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:

                st.markdown(f"[{movie}]({link})")

        else:
                st.write(
                        "You may select the genres and change the IMDb score of your choice.")

    else:
        st.write('Select option')