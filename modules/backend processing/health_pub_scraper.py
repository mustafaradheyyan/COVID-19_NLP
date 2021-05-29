import os
import re
import requests
from bs4 import BeautifulSoup

def main():
    start_date = '2020-05-01'
    end_date = '2020-05-22'
    URL = (f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}%20limit_to%'
           f'3A{end_date}%20numresults%3A25%20sort%3Arelevance-rank%20format_result%3Astandard'
    #URL = (f'https://www.medrxiv.org/search/COVID-19%252BOR%252BnCOV%252BOR%252B'
    #      f'novel%252Bcoronavirus%20jcode%3Amedrxiv%20limit_from%3A{start_date}'
    #      f'%20limit_to%3A{end_date}%20numresults%3A25%20sort%3Arelevance-rank%20'
    #      f'format_result%3Astandard')
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
  
    results = soup.find_all('a', href=re.compile('/content/10.1101/*'))
    print(results, file=open('../log.txt', 'w'))

if __name__ == '__main__':
  main()
