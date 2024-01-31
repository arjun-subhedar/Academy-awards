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

    best_picture = []
    best_director = []
    best_actor = []
    best_actress = []
    best_supporting_actor = []
    best_supporting_actress = []
    other_lists = []

    for data in datas:
        t = data.text.split('\n')
        if 'Best Picture' in t:
            t.remove('Best Picture')
            other_lists.append(t)
        if 'Best Director' in t:
            t.remove('Best Director')
            other_lists.append(t)
        if 'Best Actor' in t:
            t.remove('Best Actor')
            other_lists.append(t)
        if 'Best Actress' in t:
            t.remove('Best Actress')
            other_lists.append(t)
        if 'Best Supporting Actor' in t:
            t.remove('Best Supporting Actor')
            other_lists.append(t)
        if 'Best Supporting Actress' in t:
            t.remove('Best Supporting Actress')
            other_lists.append(t)

    for i in range (0, 5):
        best_actor.append(other_lists[2][i].split(" – "))
        best_actress.append(other_lists[3][i].split(" – "))
        best_supporting_actor.append(other_lists[4][i].split(" – "))
        best_supporting_actress.append(other_lists[5][i].split(" – "))
    best_director = other_lists[1]
    best_picture = other_lists[0]
    for i in range (5):
        t = best_director[i].split(" – ")
        t[1] = t[1].rstrip("‡")
        best_director[i] = t
    best_director = [tuple(x) for x in best_director]
    for i in range (10):
        t = best_picture[i].split(" – ")[0]
        t = t.rstrip("‡")
        best_picture[i] = t
    for i in range (0, 5):
        best_actor[i][1] = best_actor[i][1].split(" as")[0].strip()
        best_actress[i][1] = best_actress[i][1].split(" as")[0].strip()
        best_supporting_actor[i][1] = best_supporting_actor[i][1].split(" as")[0].strip()
        best_supporting_actress[i][1] = best_supporting_actress[i][1].split(" as")[0].strip()
    return best_picture, best_director, best_actor, best_actress, best_supporting_actor, best_supporting_actress

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
    best_actor = []
    best_actress = []
    best_supporting_actor = []
    best_supporting_actress = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Actor in a Leading Role' in t:
            t.remove('Best Actor in a Leading Role')
            other_lists.append(t)
        if 'Best Actress in a Leading Role' in t:
            t.remove('Best Actress in a Leading Role')
            other_lists.append(t)
        if 'Best Actor in a Supporting Role' in t:
            t.remove('Best Actor in a Supporting Role')
            other_lists.append(t)
        if 'Best Actress in a Supporting Role' in t:
            t.remove('Best Actress in a Supporting Role')
            other_lists.append(t)

    for i in range (4):
        other_lists[i] = list(filter(('').__ne__, other_lists[i]))
    for i in range (0, len(other_lists[0])):
        best_actor.append(other_lists[0][i].split(" – "))
        best_actress.append(other_lists[1][i].split(" – "))
        best_supporting_actor.append(other_lists[2][i].split(" – "))
        best_supporting_actress.append(other_lists[3][i].split(" – "))
    num = int(len(best_actor))
    for i in range (0, num):
        best_actor[i][1] = best_actor[i][1].split(" as")[0].strip()
        best_actress[i][1] = best_actress[i][1].split(" as")[0].strip()
        best_supporting_actor[i][1] = best_supporting_actor[i][1].split(" as")[0].strip()
        best_supporting_actress[i][1] = best_supporting_actress[i][1].split(" as")[0].strip()

    best_actor = [tuple(x) for x in best_actor]
    best_actress = [tuple(x) for x in best_actress]
    best_supporting_actor = [tuple(x) for x in best_supporting_actor]
    best_supporting_actor = [tuple(x) for x in best_supporting_actor]
    return best_actor, best_actress, best_supporting_actor, best_supporting_actress

def get_sag_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Screen_Actors_Guild_Awards'.format(year-1994, suffix(year-1944))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")

    best_ensemble = []
    best_actor = []
    best_actress = []
    best_supporting_actor = []
    best_supporting_actress = []

    other_lists = []

    for data in datas:
        t = data.text.split('\n')
        if 'Outstanding Performance by a Male Actor in a Leading Role' in t:
            t.remove('Outstanding Performance by a Male Actor in a Leading Role')
            other_lists.append(t)
        if 'Outstanding Performance by a Female Actor in a Leading Role' in t:
            t.remove('Outstanding Performance by a Female Actor in a Leading Role')
            other_lists.append(t)
        if 'Outstanding Performance by a Male Actor in a Supporting Role' in t:
            t.remove('Outstanding Performance by a Male Actor in a Supporting Role')
            other_lists.append(t)
        if 'Outstanding Performance by a Female Actor in a Supporting Role' in t:
            t.remove('Outstanding Performance by a Female Actor in a Supporting Role')
            other_lists.append(t)
        if 'Outstanding Performance by a Cast in a Motion Picture' in t:
            t.remove('Outstanding Performance by a Cast in a Motion Picture')
            other_lists.append(t)
   
    for i in range (5):
        other_lists[i] = list(filter(('').__ne__, other_lists[i]))
    for i in range (5):
        best_ensemble.append(other_lists[4][i].split(" – ")[0])
        best_actor.append(other_lists[0][i].split(" – "))
        best_actress.append(other_lists[1][i].split(" – "))
        best_supporting_actor.append(other_lists[2][i].split(" – "))
        best_supporting_actress.append(other_lists[3][i].split(" – "))
    for i in range (0, 5):
        best_actor[i][1] = best_actor[i][1].split(" as")[0].strip()
        best_actress[i][1] = best_actress[i][1].split(" as")[0].strip()
        best_supporting_actor[i][1] = best_supporting_actor[i][1].split(" as")[0].strip()
        best_supporting_actress[i][1] = best_supporting_actress[i][1].split(" as")[0].strip()
    best_actor = [tuple(x) for x in best_actor]
    best_actress = [tuple(x) for x in best_actress]
    best_supporting_actor = [tuple(x) for x in best_supporting_actor]
    best_supporting_actress = [tuple(x) for x in best_supporting_actress]
    return best_actor, best_actress, best_supporting_actor, best_supporting_actress,best_ensemble

def get_cc_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Critics%27_Choice_Awards'.format(year-1995, suffix(year-1995))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("td")
    best_actor = []
    best_actress = []
    best_supporting_actor = []
    best_supporting_actress = []
    other_lists = []
    for data in datas:
        t = data.text.split('\n')
        if 'Best Actor' in t:
            t.remove('Best Actor')
            other_lists.append(t)
        if 'Best Actress' in t:
            t.remove('Best Actress')
            other_lists.append(t)
        if 'Best Supporting Actor' in t:
            t.remove('Best Supporting Actor')
            other_lists.append(t)
        if 'Best Supporting Actress' in t:
            t.remove('Best Supporting Actress')
            other_lists.append(t)
    for i in range (4):
        other_lists[i] = list(filter(('').__ne__, other_lists[i]))
    for i in range (0, len(other_lists[0])):
        best_actor.append(other_lists[0][i].split(" – "))
        best_actress.append(other_lists[1][i].split(" – "))
        best_supporting_actor.append(other_lists[2][i].split(" – "))
        best_supporting_actress.append(other_lists[3][i].split(" – "))
    for i in range (0, len(best_actor)):
        best_actor[i][1] = best_actor[i][1].split(" as")[0].strip()
        best_actress[i][1] = best_actress[i][1].split(" as")[0].strip()
        best_supporting_actor[i][1] = best_supporting_actor[i][1].split(" as")[0].strip()
        best_supporting_actress[i][1] = best_supporting_actress[i][1].split(" as")[0].strip()
    best_actor = [tuple(x) for x in best_actor]
    best_actress = [tuple(x) for x in best_actress]
    best_supporting_actor = [tuple(x) for x in best_supporting_actor]
    best_supporting_actress = [tuple(x) for x in best_supporting_actress]
    return best_actor, best_actress, best_supporting_actor, best_supporting_actress

def get_gg_data(year):
    r = requests.get('https://en.wikipedia.org/wiki/{}{}_Golden_Globe_Awards'.format(year-1943, suffix(year-1943))) 
    soup = BeautifulSoup(r.content, "lxml")
    datas = soup.find_all("tr")
    best_actor_d = []
    best_actress_d = []
    best_actor_mc = []
    best_actress_mc = []
    best_supporting_actor = []
    best_supporting_actress = []
    other_lists = []
    flag1 = 0
    flag2 = 0
    flag3 = 0
    for data in datas:
        t = data.text.split('\n')
        if flag1 == 1:
            if 'Actor' not in t:
                other_lists.append(t)
                flag1 = 0
        if flag2 == 1:
            if 'Actor' not in t:
                other_lists.append(t)
                flag2= 0
        if flag3 == 1:
            if 'Supporting Actor' not in t:
                other_lists.append(t)
                flag3 = 0
                break
        if 'Best Performance in a Motion Picture – Drama' in t:
            flag1 = 1
        if 'Best Performance in a Motion Picture – Musical or Comedy' in t:
            flag2 = 1
        if 'Best Supporting Performance in a Motion Picture' in t:
            flag3 = 1

    for i in range (3):
        other_lists[i] = list(filter(('').__ne__, other_lists[i]))

    for i in range (0, int(len(other_lists[2])/2)):
        best_actor_d.append(other_lists[0][i].split(" – "))
        best_actress_d.append(other_lists[0][i+int(len(other_lists[2])/2)].split(" – "))
        best_actor_mc.append(other_lists[1][i].split(" – "))
        best_actress_mc.append(other_lists[1][i+int(len(other_lists[2])/2)].split(" – "))
        best_supporting_actor.append(other_lists[2][i].split(" – "))
        best_supporting_actress.append(other_lists[2][i+int(len(other_lists[2])/2)].split(" – "))
    for i in range (0, len(best_actor_d)):
        best_actor_d[i][1] = best_actor_d[i][1].split(" as")[0].strip()
        best_actress_d[i][1] = best_actress_d[i][1].split(" as")[0].strip()
        best_actor_mc[i][1] = best_actor_mc[i][1].split(" as")[0].strip()
        best_actress_mc[i][1] = best_actress_mc[i][1].split(" as")[0].strip()
        best_supporting_actor[i][1] = best_supporting_actor[i][1].split(" as")[0].strip()
        best_supporting_actress[i][1] = best_supporting_actress[i][1].split(" as")[0].strip()
    best_actor_d = [tuple(x) for x in best_actor_d]
    best_actress_d = [tuple(x) for x in best_actress_d]
    best_actor_mc = [tuple(x) for x in best_actor_mc]
    best_actress_mc = [tuple(x) for x in best_actress_mc]
    best_supporting_actor = [tuple(x) for x in best_supporting_actor]
    best_supporting_actress = [tuple(x) for x in best_supporting_actress]
    return best_actor_d, best_actress_d, best_actor_mc, best_actress_mc, best_supporting_actor, best_supporting_actress

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

def get_age(actor_data):
    actor = actor_data[0]
    actor.replace(" ", "_")
    try:
        wikiurl = "https://en.wikipedia.org/wiki/{}".format(actor)
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        biotable = soup.find('table',{'class':"infobox biography vcard"}).decode()
        df=pd.read_html(io.StringIO(biotable))
        df=pd.DataFrame(df[0])
    except:
        wikiurl = "https://en.wikipedia.org/wiki/{}_(actress)".format(actor)
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        biotable = soup.find('table',{'class':"infobox biography vcard"}).decode()
        df=pd.read_html(io.StringIO(biotable))
        df=pd.DataFrame(df[0])

    bio_dict = df.to_dict()
    data = list(bio_dict.values())
    bio_list = []
    for i in data:
        x = list(i.values())
        bio_list.append(x)
    bio_dict = {}
    for i in range (len(bio_list[0])):
        bio_dict[bio_list[0][i]] = bio_list[1][i]
    str = bio_dict['Born'].replace('\xa0', ' ')
    str = str.replace('(', '')
    str = str.replace(')', '')
    l = str.split(" ")
    for i in range (len(l)):
        if l[i] == 'age':
            str = ""
            for c in l[i+1]:
                if c.isdigit():
                    str = str + c
                else:
                    break
            return int(str)
    return 0

def get_prev_oscar_stats(actor):
    oscarnoms = 0
    oscarwins = 0
    df = pd.read_csv('data/oscardata_acting.csv')
    df_new = df[df['Nominee'] == actor]
    oscarnoms = len(df_new)
    for index, row in df_new.iterrows():
        if row['Winner'] == 1:
            oscarwins += 1
    return [oscarnoms, oscarwins]

def get_df_row(year, i, category, sex, final_cols, oscar_stats, total_movie_noms, baftas, sag, cc, gg, imdb_rating, rt_audience, rt_critics, genres, age):
    df_row = {}
    for col in final_cols:
        df_row[col] = 0
    df_row['Year'] = year
    df_row['Category'] = category
    df_row['Nominee'] = i[0]
    df_row['Female'] = sex
    df_row['Oscarstat_previousnominations_acting'] = oscar_stats[i][0]
    df_row['Oscarstat_previouswins_acting'] = oscar_stats[i][1]
    df_row['Oscarstat_totalnoms'] = total_movie_noms[i[1]]
    if i[1] in best_picture:
        df_row['Nom_Oscar_bestfilm'] = 1
    else:
        df_row['Nom_Oscar_bestfilm'] = 0
    df_row['Win_BAFTA'] = baftas[i][0]
    df_row['Nom_BAFTA'] = baftas[i][1]
    if category in ("Actor", "Actress"):
        if gg[i][0] == "d":
            df_row['Win_GoldenGlobe_drama-leadacting'] = gg[i][1]
            df_row['Nom_GoldenGlobe_drama-leadacting'] = gg[i][2]
        elif gg[i][0] == "mc":
            df_row['Win_GoldenGlobe_comedy-leadacting'] = gg[i][1]
            df_row['Nom_GoldenGlobe_comedy-leadacting'] = gg[i][2]
    else:
        df_row['Win_GoldenGlobe_supportingacting'] = gg[i][1]
        df_row['Nom_GoldenGlobe_supportingacting'] = gg[i][2]
    df_row['Win_Criticschoice'] = cc[i][0]
    df_row['Nom_Criticschoice'] = cc[i][1]
    df_row['Win_SAG_acting'] = sag[i][0]
    df_row['Nom_SAG_acting'] = sag[i][1]
    df_row['Win_SAG_bestcast'] = sag[i][2]
    df_row['Nom_SAG_bestcast'] = sag[i][3]
    if age[i] >= 0 and age[i] < 25:
        df_row['Age_[0-25]'] = 1
    elif age[i] >= 25 and age[i] < 35:
        df_row['Age_[25-35]'] = 1
    elif age[i] >= 35 and age[i] < 45:
        df_row['Age_[35-45]'] = 1
    elif age[i] >= 45 and age[i] < 55:
        df_row['Age_[45-55]'] = 1
    elif age[i] >= 55 and age[i] < 65:
        df_row['Age_[55-65]'] = 1
    elif age[i] >= 65 and age[i] < 75:
        df_row['Age_[65-75]'] = 1
    else:
        df_row['Age_[75+]'] = 1
    df_row['Rating_IMDB'] = imdb_rating[i[1]]
    df_row['Rating_rtaudience'] = rt_audience[i[1]]
    df_row['Rating_rtcritic'] = rt_critics[i[1]]
    for col in final_cols:
        if "Genre" in col:
            if col.split("_")[1] in genres[i[1]]:
                df_row[col] = 1
    return df_row

def create_df_acting(best_actor, best_actress, best_supporting_actor, best_supporting_actress):
    nominated_actors = []
    nominated_actors.extend(best_actor)
    nominated_actors.extend(best_actress)
    nominated_actors.extend(best_supporting_actor)
    nominated_actors.extend(best_supporting_actress)

    movies_with_nominated_actors = []
    for i in nominated_actors:
        if i[1] not in movies_with_nominated_actors:
            movies_with_nominated_actors.append(i[1])
     
    imdb_rating = {}
    rt_audience = {}
    rt_critics = {}
    genres = {}
    for i in movies_with_nominated_actors:
        imdb_rating[i] = get_imdb_data(i)
        rt_critics[i], rt_audience[i] = get_RT_ratings(i)
    
    for i in movies_with_nominated_actors:
        genres[i] = get_genres(i)
    
    nominated_actors = [tuple(x) for x in nominated_actors]

    age = {}
    oscar_stats = {}
    for i in nominated_actors:
        age[i] = get_age(i)
        oscar_stats[i] = get_prev_oscar_stats(i[0])
    
    baftas = {}
    bafta_actor, bafta_actress, bafta_supporting_actor, bafta_supporting_actress = get_bafta_data(2023)
    for i in nominated_actors:
        win = 0
        nom = 0
        if i == bafta_actor[0] or i == bafta_actress[0] or i == bafta_supporting_actor[0] or i == bafta_supporting_actor[0]:
            win = 1
        if i in bafta_actor or i in bafta_actress or i in bafta_supporting_actor or i in bafta_supporting_actress:
            nom = 1
        baftas[i] = [win, nom]
    sag = {}
    sag_actor, sag_actress, sag_supporting_actor, sag_supporting_actress, sag_ensemble = get_sag_data(2023)
    for i in nominated_actors:
        win = 0
        nom = 0
        ensemble_win = 0
        ensemble_nom = 0 
        if i == sag_actor[0] or i == sag_actress[0] or i == sag_supporting_actor[0] or i == sag_supporting_actress[0]:
            win = 1
        if i in sag_actor or i in sag_actress or i in sag_supporting_actor or i in sag_supporting_actress:
            nom = 1
        if i[1] == sag_ensemble[0]:
            ensemble_win = 1
        if i[1] in sag_ensemble:
            ensemble_nom = 1
        sag[i] = [win, nom, ensemble_win, ensemble_nom]
    
    cc = {}
    cc_actor, cc_actress, cc_supporting_actor, cc_supporting_actress = get_cc_data(2023)
    for i in nominated_actors:
        win = 0
        nom = 0
        if i == cc_actor[0] or i == cc_actress[0] or i == cc_supporting_actor[0] or i == cc_supporting_actress[0]:
            win = 1
        if i in cc_actor or i in cc_actress or i in cc_supporting_actor or i in cc_supporting_actress:
            nom = 1
        cc[i] = [win, nom]
    
    gg = {}
    gg_actor_d, gg_actress_d, gg_actor_mc, gg_actress_mc, gg_supporting_actor, gg_supporting_actress = get_gg_data(2023)
    for i in nominated_actors:
        i = tuple(i)
        win = 0
        nom = 0
        flag = ""
        gg[i] = [flag, win, nom]
        if i in gg_actor_d or i in gg_actress_d:
            flag = "d"
            nom = 1
            if i == gg_actor_d[0] or i == gg_actress_d[0]:
                win = 1
            gg[i] = [flag, win, nom]

        if i in gg_actor_mc or i in gg_actress_mc:
            flag = "mc"
            nom = 1
            if i == gg_actor_mc[0] or i == gg_actress_mc[0]:
                win = 1
            gg[i] = [flag, win, nom]

        if i in gg_supporting_actor or i in gg_supporting_actress:
            nom = 1
            if i == gg_supporting_actor[0] or i == gg_supporting_actress[0]:
                win = 1
            gg[i] = [flag, win, nom]
    
    total_movie_noms = get_oscar_noms_count(2023)
    for i in movies_with_nominated_actors:
        if i not in total_movie_noms.keys():
            total_movie_noms[i] = 1
    
    final_cols = pd.read_csv('data/oscardata_acting.csv').columns
    df = pd.DataFrame()
    for i in best_actor:
        i = tuple(i)
        actor_row = get_df_row(2023, i, "Actor", 0, final_cols, oscar_stats, total_movie_noms, baftas, sag, cc, gg, imdb_rating, rt_audience, rt_critics, genres, age)
        df = df._append(actor_row, ignore_index = True)
    for i in best_actress:
        i = tuple(i)
        actress_row = get_df_row(2023, i, "Actress", 1, final_cols, oscar_stats, total_movie_noms, baftas, sag, cc, gg, imdb_rating, rt_audience, rt_critics, genres, age)
        df = df._append(actress_row, ignore_index = True)
    for i in best_supporting_actor:
        i = tuple(i)
        actress_row = get_df_row(2023, i, "Supporting Actor", 0, final_cols, oscar_stats, total_movie_noms, baftas, sag, cc, gg, imdb_rating, rt_audience, rt_critics, genres, age)
        df = df._append(actress_row, ignore_index = True)
    for i in best_supporting_actress:
        i = tuple(i)
        actress_row = get_df_row(2023, i, "Supporting Actress", 1, final_cols, oscar_stats, total_movie_noms, baftas, sag, cc, gg, imdb_rating, rt_audience, rt_critics, genres, age)
        df = df._append(actress_row, ignore_index = True)
    df.to_csv('data/2023_acting.csv')


best_picture, best_director, best_actor, best_actress, best_supporting_actor, best_supporting_actress = get_oscars_nominees(2023)
create_df_acting(best_actor, best_actress, best_supporting_actor, best_supporting_actress)
