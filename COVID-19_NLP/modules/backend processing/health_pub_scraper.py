import os
import re
import requests
from tweet_scraper import *
from process_nlp_output import write_to_file
from bs4 import BeautifulSoup

path = 'health_pub'
if not os.path.exists(path):
    os.mkdir(path)
    
def health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term):
    additional_pages = '?page='
    number_of_results_per_page = 50
    months = calculate_number_of_months(start_date, end_date)
    final_date = end_date
    url_dict = {}

    for month_count in range(0, months + 1):
        # Creating list to append tweet data to
        if not months == month_count:
            end_date = calculate_end_date(start_date, end_date)
        else:
            end_date = final_date
        for monthly_page_count in (range(0, (number_of_pubs_per_month / number_of_results_per_page) + 1):
        
            URL = (f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}%20limit_to%'
                   f'3A{end_date}%20numresults%3A{number_of_results_per_page}%20sort%3Arelevance-rank'
                   f'%20format_result%3Astandard{additional_pages}{monthly_page_count}'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
          
            url_dict[month_count] = soup.find_all('a', href=re.compile('/content/10.1101/*'))
            start_date = add_date_by_days(end_date, 1)

    write_to_file(url_dict, search_term + '_url_dict_csv.csv', ['Date', 'URL'])
    #print(results, file=open('../log.txt', 'w'))
        
