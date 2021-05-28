import sys
import os
sys.path.insert(0, 'backend processing')
from tweet_scraper import *
from tweet_to_dict import *
from process_nlp_output import *

def main():
    start_date = '01-01-2020'
    end_date = '11-30-2020'
    search_term = 'COVID-19'
    pub_csv = open_read_csv_file('CSVs/health_pubbb.csv')
    pub_url_dictionary = create_dictionary_object(pub_csv)
    get_nlp_keywords_and_sentiment_to_file(pub_url_dictionary, 'health_pub..url')
    tweet_scraper(start_date, end_date, search_term)
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text')
    turn_keywords_into_graph(search_term)

if __name__ == '__main__':
  main()
