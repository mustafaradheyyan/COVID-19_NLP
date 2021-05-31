from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import os
import calendar
import snscrape.modules.twitter as sntwitter
import pandas as pd

tweet_path = 'tweets'

def initiate_path():
    if not os.path.exists(tweet_path):
        os.mkdir(tweet_path)

def calculate_days_in_month(month, year):
    return calendar.monthrange(year, month)[1]

def calculate_number_of_months(start_date, end_date, date_format):
    start_date = datetime.strptime(str(start_date), date_format)
    end_date = datetime.strptime(str(end_date), date_format)
    r = relativedelta.relativedelta(end_date, start_date)
    return (r.years * 12) + r.months

def add_date_by_days(date, days, date_format):
    date = datetime.strptime(date, date_format)
    date = date + timedelta(days)
    return date.strftime(date_format)

def subtract_date_by_days(date, days, date_format):
    date = datetime.strptime(date, date_format)
    date = date - timedelta(days)
    return date.strftime(date_format)

def calculate_end_date(start_date, end_date, date_format):
    if date_format == '%m-%d-%Y':
        return str(start_date[0:2] + '-' + str(calculate_days_in_month(int(start_date[0:2]),\
                                                int(start_date[-4:]))) + '-' + start_date[-4:])
    elif date_format == '%d-%m-%Y':
        return str(str(calculate_days_in_month(int(start_date[3:5]), int(start_date[-4:])))\
                                               + '-' + start_date[3:5] + '-' + start_date[-4:])
    
def get_twitter_search_string(keyword, start_date, end_date):
     return str(keyword + ' lang:en since:' + str(start_date[-4:]) + '-' + str(start_date[-10:-8])\
                + '-' + str(start_date[-7:-5]) + ' until:' + str(end_date[-4:]) + '-'\
                + str(end_date[-10:-8]) + '-' + str(end_date[-7:-5]))
     
def get_file_name_string(keyword, end_date):
    end_date = subtract_date_by_days(end_date, 1, '%m-%d-%Y')
    return str(keyword + '_' + str(end_date[-10:-8]) + '-' + str(end_date[-7:-5]) +\
               '-' + str(end_date[-2:]) + '.csv')

def tweet_scraper(number_of_tweets_per_month, start_date, end_date, keyword):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    initiate_path()
    months = calculate_number_of_months(start_date, end_date, '%m-%d-%Y')
    final_date = end_date
    for month_count in range(0, months + 1):
        # Creating list to append tweet data to
        tweets_list2 = []
        if not months == month_count:
            end_date = calculate_end_date(start_date, end_date, '%m-%d-%Y')
        else:
            end_date = final_date
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper\
                    (get_twitter_search_string(keyword, start_date, end_date)).get_items()):
            if i > number_of_tweets_per_month:
                break
            tweets_list2.append([tweet.date, tweet.id, tweet.content])
        # Creating a dataframe from the tweets list above
        tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text'])
        file_name = os.path.join(tweet_path, get_file_name_string(keyword, end_date))
        tweets_df2.to_csv(file_name)
        start_date = add_date_by_days(end_date, 1, '%m-%d-%Y')
        
def main():
    # mm-dd-YYYY format
    start_date = '01-01-2020'
    end_date = '05-24-2021'
    keyword = 'coronavirus'
    number_of_tweets_per_month = 1000
    tweet_scraper(number_of_tweets_per_month, start_date, end_date, keyword)

if __name__ == '__main__':
    main()