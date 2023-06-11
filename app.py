import pickle
import numpy as np
import pandas as pd
import requests
from flask import Flask, render_template,request
app = Flask(__name__)

similarity=pickle.load(open('static/similarity.pkl','rb'))
movies=pd.read_pickle(open('static/movies.pkl', 'rb'))

movie_titles=movies['title'].values
movie_id=movies['movie_id'].values
movie_info=movies['homepage'].values

def fetchposter(movieid):
    response=requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=c6201f04ce5f04599222cfee31bd8d64'.format(movieid))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    t=["movie1","movie2","movie3","movie4","movie5"]
    info=["","","","",""]
    poster=["","","","",""]
    if request.method=='POST':
        title = request.form['title']
        x=1
        n=1713
        for i in movies['title']:
            if i==title:
                break;
            x+=1
        if x>=n:
            return render_template('movie_not_found.html')

        x=x-1
        index_list=[]

        for i in similarity:
            index_list.append(i[x])

        recommend_index=[]
        for j in range(11):
            big=0.0000000000000000000
            index=0
            for i in range(n):
                if big<index_list[i]:
                    index=i
                    big=index_list[i]
            big=0.0000000000000000000
            recommend_index.append(index);
            index_list[index]=0
            index=0
        for i in range(5):
            t[i]=movie_titles[recommend_index[i]]
            info[i]=movie_info[recommend_index[i]]
            poster[i]=fetchposter(movie_id[recommend_index[i]])
    return render_template('recommendation.html',title=t,info=info,poster=poster)

@app.route('/')
def Home():
    return render_template('index.html')

# @app.route('/test1')
# def test1():
#     return 'test1'

if __name__=="__main__":
    app.run(debug=True)