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

def get_bafta_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_British_Academy_Film_Awards'.format(year-1947, suffix(year-1947))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")
    best_picture = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Film' in t:
            other_lists = t
    other_lists = list(filter(('').__ne__, other_lists))
    other_lists.remove('Best Film')
    for i in range (0, len(other_lists)):
        best_picture.append(other_lists[i].split(" – ")[0])
    return best_picture

def get_gg_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Golden_Globe_Awards'.format(year-1943, suffix(year-1943))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_picture_mc = []
    best_picture_d = []
    other_lists = []
    flag = 0
    for data in datas:
        t = data.text.split('\n')
        if flag == 1:
            other_lists = t
            break
        if 'Drama' in t and 'Musical or Comedy' in t:
            flag = 1
    other_lists = list(filter(('').__ne__, other_lists))
    num = len(other_lists)/2
    best_picture_d = other_lists[0:int(num)]
    best_picture_mc = other_lists[int(num):]
    return best_picture_d, best_picture_mc

def get_sag_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Screen_Actors_Guild_Awards'.format(year-1994, suffix(year-1944))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_ensemble = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Outstanding Performance by a Cast in a Motion Picture' in t:
            other_lists = t
    other_lists = list(filter(('').__ne__, other_lists))
    other_lists.remove('Outstanding Performance by a Cast in a Motion Picture')
    for i in range (0, 5):
        best_ensemble.append(other_lists[i].split(" – ")[0])
    return best_ensemble

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

def get_pga_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Producers_Guild_of_America_Awards'.format(year-1989, suffix(year-1989))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_picture = []
    other_lists = []
    flag = 0
    for data in datas:
        t = data.text.split("\n")
        if flag == 1:
            other_lists = t
            break
        if 'Darryl F. Zanuck Award for Outstanding Producer of Theatrical Motion Pictures' in t:
            flag = 1
    other_lists = list(filter(('').__ne__, other_lists))
    for i in range (0, len(other_lists)):
        best_picture.append(other_lists[i].split(" – ")[0])
    return best_picture

def get_cc_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Critics%27_Choice_Awards'.format(year-1995, suffix(year-1995))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")
    best_picture = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Picture' in t:
            other_lists = t
            break
    other_lists = list(filter(('').__ne__, other_lists))
    other_lists.remove('Best Picture')
    for i in range (0, len(other_lists)):
        str = other_lists[i]
        if "[" in other_lists[i]:
            str = other_lists[i][0:len(other_lists[i])-3]
        best_picture.append(str)
    return best_picture


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

def get_df_row(year, i, final_cols, totalnoms, baftas, gg, cc, sag, dga, pga, imdb_rating, rt_audience, rt_critics, genres):
    df_row = {}
    for col in final_cols:
        df_row[col] = 0
    df_row['Year'] = year
    df_row['Nominee'] = i
    df_row['Category'] = 'Picture'
    df_row['Film'] = i
    df_row['Oscarstat_totalnoms'] = totalnoms[i]
    movies_with_nominated_director = []
    for j in best_director:
        movies_with_nominated_director.append(j[1])
    if i in movies_with_nominated_director:
        df_row['Nom_Oscar_bestdirector'] = 1
    else:
        df_row['Nom_Oscar_bestdirector'] = 0
    df_row['Win_BAFTA'] = baftas[i][0]
    df_row['Nom_BAFTA'] = baftas[i][1]
    if gg[i][0] == "d":
        df_row['Win_GoldenGlobe_bestdrama'] = gg[i][1]
        df_row['Nom_GoldenGlobe_bestdrama'] = gg[i][2]
    elif gg[i][0] == "mc":
        df_row['Win_GoldenGlobe_bestcomedy'] = gg[i][1]
        df_row['Nom_GoldenGlobe_bestcomedy'] = gg[i][2]
    df_row['Win_SAG_bestcast'] = sag[i][0]
    df_row['Nom_SAG_bestcast'] = sag[i][1]
    df_row['Rating_IMDB'] = imdb_rating[i]
    df_row['Rating_rtaudience'] = rt_audience[i]
    df_row['Rating_rtcritic'] = rt_critics[i]
    df_row['Win_Criticschoice'] = cc[i][0]
    df_row['Nom_Criticschoice'] = cc[i][1]
    df_row['Win_DGA'] = dga[i][0]
    df_row['Nom_DGA'] = dga[i][1]
    df_row['Win_PGA'] = pga[i][0]
    df_row['Nom_PGA'] = pga[i][1]
    for col in final_cols:
        if "Genre" in col:
            if col.split("_")[1] in genres[i]:
                df_row[col] = 1
    return df_row

def create_df_picture(best_picture):
    imdb_rating = {}
    rt_audience = {}
    rt_critics = {}
    genres = {}
    for i in best_picture:
        imdb_rating[i] = get_imdb_data(i)
        rt_critics[i], rt_audience[i] = get_RT_ratings(i)
    
    for i in best_picture:
        genres[i] = get_genres(i)
 
    baftas = {}
    bafta_picture = get_bafta_data(2023)
    for i in best_picture:
        win = 0
        nom = 0
        if i == bafta_picture[0]:
            win = 1
        if i in bafta_picture:
            nom = 1
        baftas[i] = [win, nom]

    gg = {}
    gg_picture_d, gg_picture_mc = get_gg_data(2023)
    for i in best_picture:
        win = 0
        nom = 0
        flag = ""
        gg[i] = [flag, win, nom]
        if i in gg_picture_d:
            flag = "d"
            nom = 1
            if i == gg_picture_d[0]:
                win = 1
            gg[i] = [flag, win, nom]

        if i in gg_picture_mc:
            flag = "mc"
            nom = 1
            if i == gg_picture_mc[0]:
                win = 1
            gg[i] = [flag, win, nom]
    
    cc = {}
    cc_picture = get_cc_data(2023)
    for i in best_picture:
        win = 0
        nom = 0
        if i == cc_picture[0]:
            win = 1
        if i in cc_picture:
            nom = 1
        cc[i] = [win, nom]
    sag = {}
    sag_ensemble = get_sag_data(2023)
    for i in best_picture:
        win = 0
        nom = 0
        if i == sag_ensemble[0]:
            win = 1
        if i in sag_ensemble:
            nom = 1
        sag[i] = [win, nom]

    dga = {}
    dga_director = get_dga_data(2023)
    movies_with_nominated_director = []
    for i in dga_director:
        movies_with_nominated_director.append(i[1])
    for i in best_picture:
        win = 0
        nom = 0
        if i == movies_with_nominated_director[0]:
            win = 1
        if i in movies_with_nominated_director:
            nom = 1
        dga[i] = [win, nom]
    
    pga = {}
    pga_picture = get_pga_data(2023)
    for i in best_picture:
        win = 0
        nom = 0
        if i == pga_picture[0]:
            win = 1
        if i in pga_picture:
            nom = 1
        pga[i] = [win, nom]
    
    totalnoms = get_oscar_noms_count(2023)
    final_cols = pd.read_csv('data/oscardata_bestpicture.csv').columns
    df = pd.DataFrame()
    for i in best_picture:
        picture_row = get_df_row(2023, i, final_cols, totalnoms, baftas, gg, cc, sag, dga, pga, imdb_rating, rt_audience, rt_critics, genres)
        df = df._append(picture_row, ignore_index = True)
    df.to_csv('data/2023_picture.csv')

best_director, best_picture = get_oscars_nominees(2023)
create_df_picture(best_picture)

