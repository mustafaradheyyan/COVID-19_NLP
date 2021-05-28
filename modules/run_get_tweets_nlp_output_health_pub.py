import sys
import os
sys.path.insert(0, 'backend processing')
from tweet_scraper import *
from tweet_to_dict import *
from process_nlp_output import *
import keywords_into_graph as kgr

def main():
    # Only change the 5 variables below from "health_pub_file_name" to "search_term"
    health_pub_file_name = 'CSVs/health_publication_information.csv'
    # Start date for searching tweets
    start_date = '01-12-2020'
    # End date for searching tweets
    end_date = '05-24-2021'
    # Search term for tweet scraping and also applies to filtering for keyword graph
    search_term = 'COVID-19'
    # Number of tweets scraped from Twitter per month
    # (for 1000 tweets per month, tweets will only be gathered from last day of each month)
    number_of_tweets_per_month = 5
    
    # Reading health pub csv file and creating dictionary object
    pub_url_dictionary = create_dictionary_object(open_read_csv_file(health_pub_file_name))
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'health_pub' part of the string signifies the NLP file name and the ".url" is the NLP query type
    get_nlp_keywords_and_sentiment_to_file(pub_url_dictionary, 'health_pub..url')
    
    # Getting English tweets from Twitter based on dates and search term
    tweet_scraper(number_of_tweets_per_month, start_date, end_date, search_term)
    # Reading tweets csv files and creating a dictionary object from it
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'tweet' part of the string signifies the NLP file name and the "text" is the NLP query type
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text')

    # Turning (both) NLP keyword csv files into a histogram graph with the top keyword per month
    kgr.turn_keywords_into_graph(search_term)

if __name__ == '__main__':
  main()
