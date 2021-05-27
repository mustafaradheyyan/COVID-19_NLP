from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import calendar
import snscrape.modules.twitter as sntwitter
import pandas as pd

def calculate_days_in_month(month, year):
    return calendar.monthrange(year, month)[1]

def calculate_number_of_months(start_date, end_date):
    start_date = datetime.strptime(str(start_date), '%m-%d-%Y')
    end_date = datetime.strptime(str(end_date), '%m-%d-%Y')
    r = relativedelta.relativedelta(end_date, start_date)
    return (r.years * 12) + r.months

def calculate_start_date(end_date):
    end_date_date_format = datetime.strptime(end_date, "%m-%d-%Y")
    start_date = end_date_date_format + timedelta(days=1)
    return start_date.strftime("%m-%d-%Y")

def calculate_end_date(start_date, end_date):
    return str(start_date[0:2] + '-' + str(calculate_days_in_month(int(start_date[0:2]),\
                                                               int(start_date[-4:]))) + '-' + start_date[-4:])
def get_twitter_search_string(keyword, start_date, end_date):
     nice_str = str(keyword + ' lang:en since:' + str(start_date[-4:]) + '-' + str(start_date[-10:-8]) + '-'\
               + str(start_date[-7:-5]) + ' until:' + str(end_date[-4:]) + '-' + str(end_date[-10:-8])\
               + '-' + str(end_date[-7:-5]))
     print(nice_str)
     return nice_str

def get_file_name_string(keyword, start_date):
    return str(keyword + '_' + str(start_date[-10:-8]) + '-' + str(start_date[-7:-5]) + '-' + str(start_date[-2:]) + '.csv')

def twitter_scraper(start_date, end_date, keyword):
    # Using TwitterSearchScraper to scrape data and append tweets to list
    months = calculate_number_of_months(start_date, end_date)
    final_date = end_date
    for month_count in range(0, months + 1):
        # Creating list to append tweet data to
        tweets_list2 = []
        if not months == month_count:
            end_date = calculate_end_date(start_date, end_date)
        else:
            end_date = final_date
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(get_twitter_search_string(keyword, start_date, end_date)).get_items()):
            if i>1000:
                break
            tweets_list2.append([tweet.date, tweet.id, tweet.content])
        # Creating a dataframe from the tweets list above
        tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text'])
        file_name = get_file_name_string(keyword, start_date)
        tweets_df2.to_csv(file_name)
        start_date = calculate_start_date(end_date)
        
def main():
    start_date = '01-12-2020'
    end_date = '01-30-2020'
    keyword = 'coronavirus'
    twitter_scraper(start_date, end_date, keyword)

if __name__ == '__main__':
    main()
