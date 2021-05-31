import os
import generate_nlp_output as nlp
from read_csv_and_get_dict import *

def initiate_path():
    keywords_path = 'nlp_keywords'
    sentiments_path = 'nlp_sentiments'
    if not os.path.exists(keywords_path):
        os.mkdir(keywords_path)
    if not os.path.exists(sentiments_path):
        os.mkdir(sentiments_path)
    return keywords_path, sentiments_path

def is_number(price_value):
    try:
        price = float(price_value)
        return price
    except ValueError:
        return 0

def write_header(csv_file, fieldnames):
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

def separate_list_with_date(date, data):
    concat_word = (date + ',')
    if type(data[0]) != float and type(data[0]) != int:
        for word in data:
            concat_word = (concat_word + word + ',')
    return concat_word.split(',')

def write_to_file(dictionary, file_name, fieldnames):
    with open(file_name, mode='w', newline='') as csv_file:
        write_header(csv_file, fieldnames)
        writer = csv.writer(csv_file)
        for date, data in dictionary.items():
            if type(data) == list:
                word_list = separate_list_with_date(date, data)
                writer.writerow(word_list)
            else:
                writer.writerow([date,data])

def write_results_to_keyword_file(file_name, keyword_dict):
    date_keyword_dict = {}
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        for date, nlp_list in keyword_dict.items():
            keyword_list = []
            for keyword in nlp_list[0]['keywords']:
                keyword_list.append(keyword['text'])
            date_keyword_dict[date] = keyword_list
        write_to_file(date_keyword_dict, file_name, ['Date', 'Keywords'])

def write_results_to_sentiment_file(file_name, sentiment_dict):
    date_sentiment_dict = {}
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        for date, nlp_list in sentiment_dict.items():
            sentiment_value = 0
            sentiment_count = 0
            for sentiment in nlp_list:
                sentiment_value += sentiment['sentiment']['document']['score']
                sentiment_count += 1
            sentiment_value /= sentiment_count
            date_sentiment_dict[date] = sentiment_value
        write_to_file(date_sentiment_dict, file_name, ['Date', 'Sentiment'])

def get_nlp_keywords_and_sentiment_to_file(keyword, nlp_dictionary, nlp_type, user_api_key, user_service_url):
    keywords_path, sentiments_path = initiate_path()
    nlp_dict = nlp.generate_nlp_output(nlp_dictionary, nlp_type[-4:], user_api_key, user_service_url)
    write_results_to_keyword_file(os.path.join(keywords_path, keyword + '_' + nlp_type[:-5] + '_nlp_keywords.csv'), nlp_dict)    
    write_results_to_sentiment_file(os.path.join(sentiments_path, keyword + '_' + nlp_type[:-5] + '_nlp_sentiments.csv'), nlp_dict)