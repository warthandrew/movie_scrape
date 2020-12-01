# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 17:12:32 2020

@author: Andrew

This script will scrape the Wikipedia articles for years in film from 1990 to 2019, ie: https://en.wikipedia.org/wiki/1990_in_film.
It will store various data points from the film release data tables on each page, and also store the links to each film's individual wiki page.
Another script, dates_cleanup.py, will go through each individual film's page and get the release dates for the US and Japan.
"""


import wikipediaapi
from bs4 import BeautifulSoup
import urllib.request as urllib2
import pandas as pd

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

wiki = wikipediaapi.Wikipedia('en')
wikij = wikipediaapi.Wikipedia('ja')

JPDates = {}
USDates = {}
counter = 0

df_movies = pd.DataFrame()
df_mov = pd.DataFrame()
mov_link = []
quarter = []
yearl = []
for yr in range(1990,2020):
    print('in year ' + str(yr))
    if yr == 2004 or yr == 2005 or yr == 2019:
        year = urllib2.urlopen(EN_BASE + PAGE_NAME_ALT + str(yr)).read()
    else:
        year = urllib2.urlopen(EN_BASE + str(yr) + PAGE_NAME).read()
    soup = BeautifulSoup(year, 'html.parser')
    soup.prettify()
    
    mov_link=[]
    table = soup.find(id='January–March').find_next('table')
    # for a in table.find_all('a', href=re.compile('wiki/')):
    #     print(a)
    for i in table.find_all('i'):
        l = i.find_next('a')['href']
        if "Citation_needed" in l:
            continue
        else:
            mov_link.append(l)
    # df = pd.read_html(str(table))[0]
    # df_movies = df_movies.append(df)
    
    df = pd.read_html(str(table))[0]
    print('j-m counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    df = df.dropna(axis=0,how='any',thresh=3)
    df = df.drop_duplicates(subset='Title',keep='first')
    mov_link = list(dict.fromkeys(mov_link))
    print('j-m counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    for i in range(len(mov_link)):
        quarter.append('Q1')
        yearl.append(yr)
    df['link'] = mov_link
    df_movies = df_movies.append(df)
    mov_link=[]
    
    table = table.find_next('table')
    for i in table.find_all('i'):
        l = i.find_next('a')['href']
        if "Citation_needed" in l:
            continue
        else:
            mov_link.append(l)
    # df = pd.read_html(str(table))[0]
    # df_movies = df_movies.append(df)

    df = pd.read_html(str(table))[0]
    print('a-j counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    df = df.dropna(axis=0,how='any',thresh=3)
    df = df.drop_duplicates(subset='Title',keep='first')
    mov_link = list(dict.fromkeys(mov_link))
    print('a-j counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    for i in range(len(mov_link)):
        quarter.append('Q2')
        yearl.append(yr)
    df['link'] = mov_link
    df_movies = df_movies.append(df)
    mov_link=[]
    # if yr == 1991:
    #     print(mov_link)
    #     print(df_movies['Title'])
    #     break
    
    table = table.find_next('table')
    for i in table.find_all('i'):
        l = i.find_next('a')['href']
        if "Citation_needed" in l:
            continue
        else:
            mov_link.append(l)
    # df = pd.read_html(str(table))[0]
    # df_movies = df_movies.append(df)

    df = pd.read_html(str(table))[0]
    print('j-s counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    df = df.dropna(axis=0,how='any',thresh=3)
    df = df.drop_duplicates(subset='Title',keep='first')
    mov_link = list(dict.fromkeys(mov_link))
    print('j-s counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    for i in range(len(mov_link)):
        quarter.append('Q3')
        yearl.append(yr)
    df['link'] = mov_link
    df_movies = df_movies.append(df)
    mov_link=[]
    
    table = table.find_next('table')
    for i in table.find_all('i'):
        l = i.find_next('a')['href']
        if "Citation_needed" in l:
            continue
        else:
            mov_link.append(l)
    # df = pd.read_html(str(table))[0]
    # df_movies = df_movies.append(df)

    df = pd.read_html(str(table))[0]
    print('o-d counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    df = df.dropna(axis=0,how='any',thresh=3)
    df = df.drop_duplicates(subset='Title',keep='first')
    mov_link = list(dict.fromkeys(mov_link))
    print('o-d counts' + "_____" + str(len(mov_link)) + " "  + str(len(df)))
    for i in range(len(mov_link)):
        quarter.append('Q4')
        yearl.append(yr)
    df['link'] = mov_link
    df_movies = df_movies.append(df)
    
# df_movies.rename(columns = {'Production company':"Studio"}, inplace = True)
df_movies['year'] = yearl
df_movies['quarter'] = quarter
df_movies = df_movies.fillna('')
df_movies['Studio'] = df_movies['Studio'] + df_movies['Production company']
df_movies = df_movies[['year', 'quarter', 'Title', 'Studio', 'Cast and crew', 'link']]
df_movies.rename(columns = {'Title':'title','Studio':'studio','Cast and crew':'castcrew','link':'link_en'}, inplace=True)
print(df_movies.info())
print(df_movies.head())
print(df_movies.iloc[-1])
print(len(mov_link))
print(mov_link[-1])

df_movies.to_csv('movie_data.csv')

df_mov['links'] = mov_link
df_mov.to_csv('movie_links.csv')