# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 19:44:53 2020

@author: Andrew

This script will take the list of films from movie_data.csv, and run through each film's wiki page to get the langauge links for the film.
If the film has a Japanese page, it will store the date field from the Wikipedia infobox and once this data is compiled, will parse out the 
US and Japanese release dates.

Final data will be stored in movies_1990-2019.csv
"""

import wikipediaapi
import wptools
import pandas as pd
import time

def print_langlinks(page):
        langlinks = page.langlinks
        for k in sorted(langlinks.keys()):
            v = langlinks[k]
            print("%s: %s - %s: %s" % (k, v.language, v.title, v.fullurl))
            
def print_sections(sections, level=0):
        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
                print_sections(s.sections, level + 1)

EN_BASE = 'https://en.wikipedia.org/wiki/'
JA_BASE = 'https://ja.wikipedia.org/wiki/'
PAGE_NAME = '_in_film'
PAGE_NAME_ALT = 'List_of_American_films_of_'
DATE_REGEX = r'(\d+年\d+月\d+)'

wiki = wikipediaapi.Wikipedia('en')
wikij = wikipediaapi.Wikipedia('ja')

df_movies = pd.read_csv('movie_data.csv')
df_movies['link_en'] = df_movies['link_en'].apply(lambda x: x.replace('/wiki/',''))
print(df_movies.head())
print(df_movies.info())

# short_list = df_movies['link_en'].iloc[:196]
# for i in range(len(short_list)):
#     short_list[i] = short_list[i].replace('/wiki/','')
# print(short_list)
dates_raw = []
grouped = df_movies.groupby('year')

###########
# testest = '#cite_note-235'
# page_movie = wiki.page(testest)
# print(page_movie.exists())
###########


#///////////////////
for year, group in grouped:
    print(year)
    links = group['link_en']
    for movie in links:
        if 'cite_note' in movie:
            dates_raw.append('BAD_URL')
            continue
        page_movie = wiki.page(movie)
        
        print(page_movie.exists())
        # print_langlinks(page_movie)
        langs = page_movie.langlinks
        
        time.sleep(4)
        if 'ja' in langs:
            jpn = langs['ja']
            print(jpn.fullurl)
            print(jpn.title)
            
            page2 = wikij.page(jpn.title)
            print(page2.exists())
            so = wptools.page(jpn.title, lang='ja').get_parse()
            infobox = so.data['infobox']
            if infobox is not None:
                if '公開' in infobox:
                    dates = infobox['公開']
                    print(dates)
                    print(type(dates))
                    dates_raw.append(dates)
                else:
                    print('no dates for ' + movie)
                    dates_raw.append('no_dates')
            else:
                print('no infobox for ' + movie)
                dates_raw.append('no_infobox')
        else:
            print('no ja for ' + movie)
            dates_raw.append('no_ja')
    temp_name = str(year) + '_temp.csv'
    df_temp = pd.DataFrame(dates_raw)
    df_temp.to_csv(temp_name)
df_movies['dates_raw'] = dates_raw
df_movies.to_csv('movie_data_dates.csv')
#/////////////////////

df_temp1 = pd.read_csv('2011_temp.csv', header=None, names=['dates_raw'], skiprows=1)
df_temp2 = pd.read_csv('2019_temp.csv', header=None, names=['dates_raw'], skiprows=1)
df_dates = df_temp1.append(df_temp2)
df_dates = df_dates.reset_index(drop=True)
df_dates.to_csv('dates_raw.csv')

print('count pre: ' + str(df_dates['dates_raw'].count()))
df_dates['dates_raw'] = df_dates['dates_raw'].str.replace('Japan', 'JPN')
df_dates['dates_raw'] = df_dates['dates_raw'].str.replace('[', '')
df_dates['dates_raw'] = df_dates['dates_raw'].str.replace(']', '')
tempu = df_dates['dates_raw'].str.split('USA',n=1,expand=True)
tempj = df_dates['dates_raw'].str.split('JPN',n=1,expand=True)
df_dates['date_us'] = tempu[1]
df_dates['date_jp'] = tempj[1]
print('count us split: ' + str(df_dates['date_us'].count()))
print('count jp split: ' + str(df_dates['date_jp'].count()))
df_dates['date_us'] = df_dates['date_us'].str.split('日',n=1,expand=True)[0]
df_dates['date_jp'] = df_dates['date_jp'].str.split('日',n=1,expand=True)[0]
df_dates['date_us'] = df_dates['date_us'].str.extract(DATE_REGEX,expand=True)[0]
df_dates['date_jp'] = df_dates['date_jp'].str.extract(DATE_REGEX,expand=True)[0]
df_dates['date_us'] = df_dates['date_us'].str.replace(r'[年月]','-')
df_dates['date_jp'] = df_dates['date_jp'].str.replace(r'[年月]','-')
df_dates['date_us'] = df_dates['date_us'].astype('datetime64[ns]')
df_dates.at[820, 'date_jp'] = '1995-2-25'
df_dates['date_jp'] = df_dates['date_jp'].astype('datetime64[ns]')
df_dates['delay'] = df_dates['date_jp'] - df_dates['date_us']
print(df_dates['date_us'].count())
print(df_dates['date_jp'].count())

df_movies = df_movies.join(df_dates)
print(df_movies.head())
df_movies['delay'] = df_movies['delay'].apply(lambda x: x.days)
df_movies.to_csv('movies_1990-2019.csv', index=False)