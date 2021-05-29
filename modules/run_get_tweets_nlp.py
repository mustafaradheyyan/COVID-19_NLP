import sys
import os
sys.path.insert(0, 'backend processing')
from tweet_scraper import *
from tweet_to_dict import *
from process_nlp_output import *

def main():
    start_date = '01-12-2020'
    end_date = '05-24-2021'
    search_term = 'COVID-19'
    number_of_tweets_per_month = 5
    tweet_scraper(number_of_tweets_per_month, start_date, end_date, search_term)
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text')

if __name__ == '__main__':
    main()