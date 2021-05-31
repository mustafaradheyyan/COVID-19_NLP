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

def is_number(value):
    try:
        value = float(value)
        return value
    except ValueError:
        return 0

def write_header(csv_file, fieldnames):
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

def separate_list_with_date(date, data):
    concat_word = (date + ',')
    for word in data:
        concat_word = (concat_word + word + ',')
    return concat_word.split(',')

def write_dict_to_file(dictionary, file_name, fieldnames):
    if os.path.isfile(file_name):
        os.remove(file_name)
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        write_header(csv_file, fieldnames)
        writer = csv.writer(csv_file)
        for date, data in dictionary.items():
            if type(data) == list:
                word_list = separate_list_with_date(date, data)
                writer.writerow(word_list)
            else:
                writer.writerow([date,data])

def get_keyword_dict_from_nlp_dict(nlp_dict):
    keyword_dict = {}
    for date, nlp_list in nlp_dict.items():
        keyword_list = []
        for keyword in nlp_list:
            for text in keyword['keywords']:
                keyword_list.append(text['text'])
        keyword_dict[date] = keyword_list
    return keyword_dict

def write_results_to_keyword_file(file_name, nlp_dict):
    keyword_dict = get_keyword_dict_from_nlp_dict(nlp_dict)
    write_dict_to_file(keyword_dict, file_name, ['Date', 'Keywords'])

def get_sentiment_dict_from_nlp_dict(nlp_dict):
    sentiment_dict = {}
    for date, nlp_list in nlp_dict.items():
        sentiment_score = 0
        sentiment_count = 0
        for sentiment in nlp_list:
            sentiment_score += is_number(sentiment['sentiment']['document']['score'])
            sentiment_count += 1
        if sentiment_count:
            sentiment_score /= sentiment_count
            sentiment_dict[date] = sentiment_score
    return sentiment_dict

def write_results_to_sentiment_file(file_name, nlp_dict):
    sentiment_dict = get_sentiment_dict_from_nlp_dict(nlp_dict)
    write_dict_to_file(sentiment_dict, file_name, ['Date', 'Sentiment'])

def get_nlp_keywords_and_sentiment_to_file(file_name, nlp_dictionary, nlp_type, user_api_key, user_service_url, number_of_keywords):
    keywords_path, sentiments_path = initiate_path()
    nlp_dict = nlp.generate_nlp_output(nlp_dictionary, nlp_type, user_api_key, user_service_url, number_of_keywords)
    write_results_to_keyword_file(os.path.join(keywords_path, file_name + '_nlp_keywords.csv'), nlp_dict)    
    write_results_to_sentiment_file(os.path.join(sentiments_path, file_name + '_nlp_sentiments.csv'), nlp_dict)