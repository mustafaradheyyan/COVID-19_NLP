import sys
sys.path.insert(0, 'backend processing')
from health_pub_scraper import *
from process_nlp_output import *

def main():
    search_term = 'COVID-19'
    start_date = '01-12-2020'
    end_date = '06-24-2020'
    number_of_pubs_per_month = 3
    
    health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term)
    dict_of_urls = get_health_pub_csv_data_into_url_dict(start_date, end_date, search_term)
    get_nlp_keywords_and_sentiment_to_file(dict_of_urls, 'health_pub..url')

if __name__ == '__main__':
    main()
