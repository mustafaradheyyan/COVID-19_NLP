import os
import re
import requests
import math
from tweet_scraper import *
from process_nlp_output import write_to_file
from bs4 import BeautifulSoup

path = 'health_pub'
if not os.path.exists(path):
    os.mkdir(path)

def calculate_mid_date(start_date, end_date, date_format):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    mid_date = start_date.date() + (end_date - start_date) / 2
    return mid_date.strftime(date_format)

def health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term):
    additional_pages = '?page='
    number_of_results_per_page = 10
    months = calculate_number_of_months(start_date, end_date, '%d-%m-%Y')
    final_date = end_date
    url_dict = {}

    for month_count in range(0, months + 1):
        # Creating list to append tweet data to
        url_list = []
        if not months == month_count:
            end_date = calculate_end_date(start_date, end_date, '%d-%m-%Y')
        else:
            end_date = final_date
            
        pages = math.ceil(number_of_pubs_per_month / number_of_results_per_page)
        for monthly_page_count in range(0, pages):
            URL = (f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}%20limit_to%'
                   f'3A{end_date}%20numresults%3A{number_of_results_per_page}%20sort%3Arelevance-rank'
                   f'%20format_result%3Astandard{additional_pages}{monthly_page_count}')
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            href_results = soup.find_all('a', href=re.compile('/content/10.1101/*'))
            if not pages == monthly_page_count + 1:
                pages_remaining = number_of_results_per_page
            else:
                pages_remaining = number_of_pubs_per_month - (monthly_page_count * number_of_results_per_page)
            page_remaining_count = 0
            print(start_date + ' ' + end_date + ': ' + str(pages_remaining))
            for result in href_results:
                #print(result.attrs)
                if page_remaining_count >= pages_remaining:
                    break
                url_list.append(result['href'])
                page_remaining_count += 1

        print(url_list, file=open('../log' + str(month_count) + '.txt', 'w'))
        url_dict[calculate_mid_date(start_date, end_date, '%d-%m-%Y')] = url_list
        #print(url_dict)
        start_date = add_date_by_days(end_date, 1, '%d-%m-%Y')

    write_to_file(url_dict, os.path.join(path, search_term + '_url_dict_csv.csv'), ['Date', 'URL'])
    #print(url_dict, file=open('../log.txt', 'w'))
