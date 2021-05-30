import sys
import os
sys.path.insert(0, 'backend processing')
sys.path.insert(0, 'frontend gui')
from health_pub_scraper import *
from tweet_scraper import *
from tweet_to_dict import *
from process_nlp_output import *
import keywords_into_graph as kgr
from user_input_gui import *

def main():
    gui_window = Window()
    #start_date, end_date, search_term, number_of_pubs_per_month, number_of_tweets_per_month = create_user_input_gui()

    # Only change the 5 variables below from "start_date" to "number_of_tweets_per_month"
    # Start date for searching tweets
    start_date = '01-12-2020'
    # End date for searching tweets
    end_date = '03-24-2020'
    # Search term for tweet scraping and also applies to filtering for keyword graph
    search_term = 'COVID-19'
    # Number of health publications scraped from medRxiv per month
    number_of_pubs_per_month = 2
    # Number of tweets scraped from Twitter per month
    # (for 1000 tweets per month, tweets will only be gathered from last day of each month)
    number_of_tweets_per_month = 5
    
    # Reading health pub csv file and creating dictionary object
    print("\nScraping medRxiv " + search_term + " publication urls", flush = True)
    dict_of_urls = health_pub_scraper(number_of_pubs_per_month, start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'health_pub' part of the string signifies the NLP file name and the ".url" is the NLP query type
    print("Success\n\nProcessing health pub urls with NLP", flush = True)
    get_nlp_keywords_and_sentiment_to_file(dict_of_urls, 'health_pub..url')
    
    # Getting English tweets from Twitter based on dates and search term
    print("Success\n\nScraping Twitter tweets", flush = True)
    tweet_scraper(number_of_tweets_per_month, start_date, end_date, search_term)
    # Reading tweets csv files and creating a dictionary object from it
    print("Success\n\nConverting tweet csv files into a text dictionary", flush = True)
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    # Processing dictionary object with NLP to return a keywords and sentiments file
    # The 'tweet' part of the string signifies the NLP file name and the "text" is the NLP query type
    print("Success\n\nProcessing tweets with NLP", flush = True)
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'tweet.text')

    # Turning (both) NLP keyword csv files into a histogram graph with the top keyword per month
    print("Success\n\nProcessing NLP keyword csv files into graphs", flush = True)
    kgr.turn_keywords_into_graph(search_term)
    print("Success")

if __name__ == '__main__':
      main()
