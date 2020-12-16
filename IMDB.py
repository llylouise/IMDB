from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn


timestart_time = time()
request = 0

names  = []
years = []
ratings = []
votes = []

pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2010,2021)]

for year_url in years_url:
    for page in pages:
        if page == 1:
            url = 'https://www.imdb.com/search/title/?title_type=feature,documentary,short&release_date=' + year_url + '-01-01,' + year_url + '-12-12&sort=user_rating,desc&ref_=adv_prv'
        else:
            url = 'https://www.imdb.com/search/title/?title_type=feature,documentary,short&release_date=' + year_url + '-01-01,' + year_url + '-12-12&sort=user_rating,desc&start=' + str((int(page)-1)*50+1) + 'ref_=adv_prv'
        response = get(url)
        sleep(randint(5,8))
        request += 1
        elapsed_time = time() - timestart_time
 #       print('Request:{}; Frequency:{} requests/s'.format(request,request/elapsed_time))
        clear_output(wait=True)
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(request, response.status_code))
            # Break the loop if the number of requests is greater than expected
        if request > 100:
            warn('Number of requests was greater than expected.')
            break
#print(response.text[:500])
        html = BeautifulSoup(response.text,'html.parser')
        containers = html.find_all('div', class_ = 'lister-item mode-advanced')
#print(len(containers))
        for container in containers:
            name = container.h3.a.text
            year = container.h3.find('span',class_ = 'lister-item-year text-muted unbold').text
            rating = container.strong.text
            vote = container.find('span',attrs={'name':'nv'}).text
            names.append(name)
            years.append(year)
            ratings.append(rating)
            votes.append(vote)
            print(names,years,ratings,votes)


data = pd.DataFrame({'movie':names,'year':years,'rating':ratings,'vote':votes})
print(data)

