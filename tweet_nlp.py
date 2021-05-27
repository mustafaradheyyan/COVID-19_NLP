from nlp_output import *
import pandas as pd
from crawler import *
from string import printable

def remove_non_ascii(text): 
    return ''.join(i for i in text if ord(i)<128)  

def get_tweet_csv_data_into_text_dict(start_date, end_date, search_term):
    # Creating dict to insert tweet data to
    tweets_dict = {}
    months = calculate_number_of_months(start_date, end_date)
    final_date = end_date
    for month_count in range(0, months + 1):
        if not months == month_count:
            end_date = calculate_end_date(start_date, end_date)
        else:
            end_date = final_date
        file_name = str(get_file_name_string(search_term, start_date))
        df = pd.read_csv(file_name, usecols=['Text'])
        df['Text'] = df['Text'].apply(remove_non_ascii)
        tweets_dict[start_date] = df['Text'].tolist()
        start_date = calculate_start_date(end_date)
    return tweets_dict

def main():
    start_date = '01-12-2020'
    end_date = '01-30-2020'
    search_term = 'coronavirus'
    #twitter_scraper(start_date, end_date, search_term)
    dict_of_text = get_tweet_csv_data_into_text_dict(start_date, end_date, search_term)
    get_nlp_keywords_and_sentiment_to_file(dict_of_text, 'text')

if __name__ == '__main__':
    main()
