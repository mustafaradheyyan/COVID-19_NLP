import os
import re
import requests
from bs4 import BeautifulSoup

def main():
    URL = 'https://www.medrxiv.org/search/COVID-19%252BOR%252BnCOV%252BOR%252Bnovel%252Bcoronavirus%20jcode%3Amedrxiv%20limit_from%3A2021-05-01%20limit_to%3A2021-05-22%20numresults%3A25%20sort%3Arelevance-rank%20format_result%3Astandard'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.find(id = 'zone-content')
    #print(results.prettify(), file=open('../log.txt', 'w'))

    #results = soup.find_all("href = '/content/10.1101/*')
    #rows = teamtable.find_all('tr')
    results = soup.find_all('a', href=re.compile('/content/10.1101/*'))
    #dates = soup.findAll("div", {"id" : lambda L: L and L.startswith('date')})
    print(results, file=open('../log.txt', 'w'))

if __name__ == '__main__':
  main()
