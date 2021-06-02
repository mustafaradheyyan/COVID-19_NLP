import os
import re
import requests
import math
from datetime import datetime
import modules.tweet_scraper as ts
from modules.process_nlp_output import write_dict_to_file
from bs4 import BeautifulSoup

def initiate_health_pub_path_get_file_name(search_term, begin_date, final_date):
    path = 'health_pub'
    if not os.path.exists(path):
        os.mkdir(path)
    begin_date, final_date = convert_dates_to_mdy(begin_date, final_date)
    return (os.path.join(path, search_term + '_' + begin_date + '_' + final_date + '_url_dict.csv'))

def calculate_mid_date(start_date, end_date, date_format):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    mid_date = start_date.date() + (end_date - start_date) / 2
    return mid_date.strftime('%m-%d-%Y')

def convert_dates_to_mdy(start_date, end_date):
    start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime("%m-%d-%Y")
    end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime("%m-%d-%Y")
    return start_date, end_date

def convert_dates_to_dmy(start_date, end_date):
    start_date = datetime.strptime(start_date, '%m-%d-%Y').strftime("%d-%m-%Y")
    end_date = datetime.strptime(end_date, '%m-%d-%Y').strftime("%d-%m-%Y")
    return start_date, end_date

def get_url_href_results(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all('a', href=re.compile('/content/10.1101/*'))

def check_health_pub_availability(search_term, start_date, end_date):
    if (get_url_href_results(f'https://www.medrxiv.org/search/{search_term}%20limit_from%3A{start_date}'\
                             f'%20limit_to%3A{end_date}')):
        return 1
    else:
        return 0

def health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term):
    start_date, end_date = convert_dates_to_dmy(start_date, end_date)
    continue_search = check_health_pub_availability(search_term, start_date, end_date)

    if continue_search:
        file_name = initiate_health_pub_path_get_file_name(search_term, start_date, end_date)
        additional_pages = '?page='
        number_of_results_per_page = 10
        months = ts.calculate_number_of_months(start_date, end_date, '%d-%m-%Y')

        url_dict = {}
        final_date = end_date
        for month_count in range(0, months + 1):
            # Creating list to append tweet data to
            url_list = []
            if not months == month_count:
                end_date = ts.calculate_end_date(start_date, '%d-%m-%Y')
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
            start_date = ts.add_date_by_days(end_date, 1, '%d-%m-%Y')
    else:
        return None, -1
    write_dict_to_file(url_dict, file_name, ['Date', 'URL'])
    return url_dict, 1