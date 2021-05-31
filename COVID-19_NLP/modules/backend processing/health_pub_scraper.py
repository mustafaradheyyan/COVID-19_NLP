import os
import re
import requests
import math
from tweet_scraper import *
from process_nlp_output import write_dict_to_file
from bs4 import BeautifulSoup

def initiate_path():
    path = 'health_pub'
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def calculate_mid_date(start_date, end_date, date_format):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    mid_date = start_date.date() + (end_date - start_date) / 2
    return mid_date.strftime('%m-%d-%Y')

def convert_dates_to_dmy(start_date, end_date):
    start_date = datetime.strptime(start_date, '%m-%d-%Y').strftime("%d-%m-%Y")
    end_date = datetime.strptime(end_date, '%m-%d-%Y').strftime("%d-%m-%Y")
    return start_date, end_date

def get_url_href_results(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all('a', href=re.compile('/content/10.1101/*'))

def health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term):
    start_date, end_date = convert_dates_to_dmy(start_date, end_date)
    additional_pages = '?page='
    number_of_results_per_page = 10
    months = calculate_number_of_months(start_date, end_date, '%d-%m-%Y')
    final_date = end_date
    url_dict = {}

    URL = (f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}%20limit_to%3A{end_date}')
    href_results = get_url_href_results(URL)
    if href_results:
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
                href_results = get_url_href_results(URL)
                if href_results:
                    if not pages == monthly_page_count + 1:
                        pages_remaining = number_of_results_per_page
                    else:
                        pages_remaining = number_of_pubs_per_month - (monthly_page_count * number_of_results_per_page)
                    page_remaining_count = 0
                    for result in href_results:
                        if page_remaining_count >= pages_remaining:
                            break
                        url_list.append('https://www.medrxiv.org' + result['href'] + '.full-text')
                        page_remaining_count += 1
                

            url_dict[calculate_mid_date(start_date, end_date, '%d-%m-%Y')] = url_list
            start_date = add_date_by_days(end_date, 1, '%d-%m-%Y')
    else:
        return None, -1
    path = initiate_path()
    write_dict_to_file(url_dict, os.path.join(path, search_term + '_url_dict_csv.csv'), ['Date', 'URL'])
    return url_dict, 1
