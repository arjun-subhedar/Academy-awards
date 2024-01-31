import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from imdb import Cinemagoer
import rottentomatoes as rt
import io

def suffix(number):
    str = repr(number)
    if str[-1] == "1":
        return "st"
    elif str [-1] == "2":
        return "nd"
    elif str[-1] == "3":
        return "rd"
    else:
        return "th"

def get_oscars_nominees(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Academy_Awards'.format(year-1928, suffix(year-1928))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")
    best_director = []
    best_picture = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Picture' in t:
            best_picture = t
        if 'Best Director' in t:
            best_director = t
    best_picture = list(filter(('').__ne__, best_picture))
    best_picture.remove('Best Picture')
    best_director = list(filter(('').__ne__, best_director))
    best_director.remove('Best Director')
    for i in range (5):
        t = best_director[i].split(" – ")
        t[1] = t[1].rstrip("‡")
        best_director[i] = t
    for i in range (10):
        t = best_picture[i].split(" – ")[0]
        t = t.rstrip("‡")
        best_picture[i] = t
    best_director = [tuple(x) for x in best_director]
    return best_director, best_picture

def get_oscar_noms_count(year):
    redirect = requests.get('https://en.wikipedia.org/wiki/{}{}_Academy_Awards'.format(year-1928, suffix(year-1928)))
    soup = BeautifulSoup(redirect.content, 'lxml')

    for caption in soup.find_all('caption'):
        if caption.get_text() == 'Films with multiple nominations\n':
            dtable = caption.find_parent('table', {'class': 'wikitable plainrowheaders'}).decode()

    df = pd.read_html(io.StringIO(dtable))
    df = pd.DataFrame(df[0])
    movies = list(df['Film'])
    noms = list(df['Nominations'])
    movie_nominations_count = {}
    for i in range (len(movies)):
        movie_nominations_count[movies[i]] = noms[i]
    return movie_nominations_count

def get_gg_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Golden_Globe_Awards'.format(year-1943, suffix(year-1943))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_director = []
    other_lists = []
    flag = 0
    for data in datas:
        t = data.text.split('\n')
        if flag == 1:
            other_lists = t
            break
        if 'Best Director' in t:
            flag = 1
    other_lists = list(filter(('').__ne__, other_lists))
    for i in range (0, int(len(other_lists)/2)):
        best_director.append(other_lists[i].split(" – "))
    
    best_director = [tuple(x) for x in best_director]
    return best_director

def get_bafta_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_British_Academy_Film_Awards'.format(year-1947, suffix(year-1947))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")
    best_director = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Director' in t:
            other_lists = t
    other_lists = list(filter(('').__ne__, other_lists))
    other_lists.remove('Best Director')
    for i in range (0, len(other_lists)):
        best_director.append(other_lists[i].split(" – "))
    best_director = [tuple(x) for x in best_director]
    return best_director

def get_dga_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Directors_Guild_of_America_Awards'.format(year-1948, suffix(year-1948))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_director = []
    other_lists = []
    flag = 0
    for data in datas:
        t = data.text.split("\n")
        if flag == 1:
            other_lists.append(t)
            break
        if 'Feature Film' in t:
            flag = 1
    for i in range (0, len(other_lists[0])):
        str = other_lists[0][i]
        if str != '':
            best_director.append(other_lists[0][i].split(" – "))
    best_director = [tuple(x) for x in best_director]
    return best_director

def get_imdb_data(movie_title):
    ia = Cinemagoer()
    res = ia._search_movie(movie_title, results=True)
    movie_ID = res[0][0]
    movie = ia.get_movie(movie_ID)
    rating = movie.data["rating"]
    return rating

def get_RT_ratings(movie):
    return rt.tomatometer(movie), rt.audience_score(movie)

def get_genres(movie_title):
    genres1 = [genre.lower() for genre in rt.genres(movie_title)]
    ia = Cinemagoer()
    res = ia._search_movie(movie_title, results=True)
    movie_ID = res[0][0]
    movie = ia.get_movie(movie_ID)
    genres2 = [genre.lower() for genre in movie.data["genres"]]
    return list(set(genres1+genres2))


def get_prev_oscar_stats(director):
    oscarnoms = 0
    oscarwins = 0
    df = pd.read_csv('data/oscardata_bestdirector.csv')
    df_new = df[df['Nominee'] == director]
    oscarnoms = len(df_new)
    for index, row in df_new.iterrows():
        if row['Winner'] == 1:
            oscarwins += 1
    return [oscarnoms, oscarwins]

def get_df_row(year, i, totalnoms, final_cols, oscar_stats, baftas, gg, dga, imdb_rating, rt_audience, rt_critics, genres):
    df_row = {}
    for col in final_cols:
        df_row[col] = 0
    df_row['Year'] = year
    df_row['Nominee'] = i[0]
    df_row['Category'] = 'Director'
    df_row['Film'] = i[1]
    df_row['Oscarstat_totalnoms'] = totalnoms[i[1]]
    df_row['Oscarstat_previousnominations_bestdirector'] = oscar_stats[i[0]][0]
    df_row['Oscarstat_previouswins_bestdirector'] = oscar_stats[i[0]][1]
    if i[1] in best_picture:
        df_row['Nom_Oscar_bestfilm'] = 1
    else:
        df_row['Nom_Oscar_bestfilm'] = 0
    df_row['Win_BAFTA'] = baftas[i][0]
    df_row['Nom_BAFTA'] = baftas[i][1]
    df_row['Win_GoldenGlobe_bestdirector'] = gg[i][0]
    df_row['Nom_GoldenGlobe_bestdirector'] = gg[i][1]
    df_row['Rating_IMDB'] = imdb_rating[i[1]]
    df_row['Rating_rtaudience'] = rt_audience[i[1]]
    df_row['Rating_rtcritic'] = rt_critics[i[1]]
    df_row['Win_DGA'] = dga[i][0]
    df_row['Nom_DGA'] = dga[i][1]
    for col in final_cols:
        if "Genre" in col:
            if col.split("_")[1] in genres[i[1]]:
                df_row[col] = 1
    return df_row

def create_df_directing(best_director):

    imdb_rating = {}
    rt_audience = {}
    rt_critics = {}
    genres = {}
    for i in best_director:
        imdb_rating[i[1]] = get_imdb_data(i[1])
        rt_critics[i[1]], rt_audience[i[1]] = get_RT_ratings(i[1])
    
    for i in best_director:
        genres[i[1]] = get_genres(i[1])
    
    oscar_stats = {}
    for i in best_director:
        oscar_stats[i[0]] = get_prev_oscar_stats(i[0])
    
    baftas = {}
    bafta_director = get_bafta_data(2023)
    for i in best_director:
        win = 0
        nom = 0
        if i == bafta_director[0]:
            win = 1
        if i in bafta_director:
            nom = 1
        baftas[i] = [win, nom]

    gg = {}
    gg_director = get_gg_data(2023)
    for i in best_director:
        win = 0
        nom = 0
        if i == gg_director[0]:
            win = 1
        if i in gg_director:
            nom = 1
        gg[i] = [win, nom]
    
    dga = {}
    dga_director = get_dga_data(2023)
    for i in best_director:
        win = 0
        nom = 0
        if i == dga_director[0]:
            win = 1
        if i in dga_director:
            nom = 1
        dga[i] = [win, nom]
    
    totalnoms = get_oscar_noms_count(2023)
    final_cols = pd.read_csv('data/oscardata_bestdirector.csv').columns
    df = pd.DataFrame()
    for i in best_director:
        director_row = get_df_row(2023, i, totalnoms, final_cols, oscar_stats, baftas, gg, dga, imdb_rating, rt_audience, rt_critics, genres)
        df = df._append(director_row, ignore_index = True)
    df.to_csv('data/2023_directing.csv')

best_director, best_picture = get_oscars_nominees(2023)
create_df_directing(best_director)

