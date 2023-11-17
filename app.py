import streamlit as st
import pickle
import pandas as pd
import requests
def poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
    movie_index = movies_dict[movies_dict['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies_dict.iloc[i[0]].movie_id

        recommended_movies.append((movies_dict.iloc[i[0]].title))
        # fetch poster from API
        recommended_movies_poster.append(poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies_dict=pd.DataFrame(movies_dict)
st.title('Movie Recommendation System')

similarity=pickle.load(open('similarity.pkl', 'rb'))
selected_movie_name=st.selectbox('Type or Select Movies',movies_dict['title'].values)

# if st.button('Recommend'):
#     names,posters=recommend(selected_movie_name)
if st.button('Show Recommendation'):
        recommended_movie_name, recommended_movie_poster= recommend(selected_movie_name)
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_name[i])
                st.image(recommended_movie_poster[i])


