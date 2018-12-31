from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import pandas as pd

url = 'http://www.imdb.com/search/title?release_date='

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

headers = {"Accept-Language": "en-US, en;q=0.5"}

for year_url in years_url : 
    for page in pages : 
        response = get(url + year_url + '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 

        page_html = BeautifulSoup(response.text, 'html.parser')

        movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
        print(movie_containers)


        # Extract data from individual movie container
        for container in movie_containers:

            # If the movie has Metascore, then extract:
            if container.find('div', class_ = 'ratings-metascore') is not None:

                # The name
                name = container.h3.a.text
                names.append(name)

                # The year
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                # The IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # The Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))

                # The number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))


        movie_ratings = pd.DataFrame({'movie': names,
                        'year': years,
                        'imdb': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes})
        print(movie_ratings.info())

        movie_ratings = movie_ratings[['movie','year','imdb','metascore','votes']]
        movie_ratings.head()
        movie_ratings['year'].unique()
        movie_ratings.to_csv('movie_ratings.csv')



