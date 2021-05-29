import os
import re
import requests
from tweet_scraper import calculate_number_of_months
from bs4 import BeautifulSoup

def health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term):
    number_of_results_per_page = 50
    number_of_pages = (number_of_pubs_per_month * calculate_number_of_months(start_date, end_date))\
                                                / number_of_results_per_page
    url_dict = {}
    
    for total_page_count in (range(0, number_of_pages)):
        if number_of_results_per_page is < number_of_pubs_per_month:
            additional_pages = '?page='
        else
            additional_pages = ''
        additional_page_number = 0
        for monthly_page_count in (range(0, number_of_pubs_per_month / number_of_results_per_page)):
        
            URL = (f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}%20limit_to%'
                   f'3A{end_date}%20numresults%3A{number_of_results_per_page}%20sort%3Arelevance-rank'
                   f'%20format_result%3Astandard{additional_pages}{additional_page_number}'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
          
            url_dict[ = soup.find_all('a', href=re.compile('/content/10.1101/*'))
            ++additional_page_number
        ++
                   
    print(results, file=open('../log.txt', 'w'))
        
