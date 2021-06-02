from modules.tweet_scraper import *

def remove_non_ascii(text): 
    return ''.join(i for i in text if ord(i)<128)  

def get_tweet_csv_data_into_text_dict(start_date, end_date, search_term):
    # Creating dict to insert tweet data to
    tweets_dict = {}
    months = calculate_number_of_months(start_date, end_date, '%m-%d-%Y')
    final_date = end_date
    for month_count in range(0, months + 1):
        if not months == month_count:
            end_date = calculate_end_date(start_date, '%m-%d-%Y')
        else:
            end_date = final_date
        file_name = os.path.join(tweet_path, str(get_file_name_string(search_term, end_date)))
        df = pd.read_csv(file_name, usecols=['Text'])
        df['Text'] = df['Text'].apply(remove_non_ascii)
        tweets_dict[subtract_date_by_days(end_date, 1, '%m-%d-%Y')] = df['Text'].tolist()
        start_date = add_date_by_days(end_date, 1, '%m-%d-%Y')
    return tweets_dict