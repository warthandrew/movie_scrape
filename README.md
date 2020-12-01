# movie_scrape

Small project to analyze the delay in movie releases between US and Japan.

Two scripts to scrape Wikipedia for yearly film data and release dates.
* [scrape.py](https://github.com/warthandrew/movie_scrape/blob/master/scrape.py)
  * This script will scrape the Wikipedia articles for years in film from 1990 to 2019, ie: https://en.wikipedia.org/wiki/1990_in_film.
It will store various data points from the film release data tables on each page, and also store the links to each film's individual wiki page.
Another script, dates_cleanup.py, will go through each individual film's page and get the release dates for the US and Japan.
* [dates_cleanup.py](https://github.com/warthandrew/movie_scrape/blob/master/dates_cleanup.py)
  * This script will take the list of films from movie_data.csv, and run through each film's wiki page to get the langauge links for the film.
If the film has a Japanese page, it will store the date field from the Wikipedia infobox and once this data is compiled, will parse out the 
US and Japanese release dates. Final data will be stored in movies_1990-2019.csv

Subsequent analysis and visualization done in [analyze_movies.ipynb](https://github.com/warthandrew/movie_scrape/blob/master/analyze_movies.ipynb)
