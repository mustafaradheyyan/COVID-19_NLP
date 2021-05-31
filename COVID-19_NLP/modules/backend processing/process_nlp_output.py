import os
import warnings
import numpy as np
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

def calculate_sentiment(nlp_data):
    sentiment_score = 0.0
    sentiment_count = 0
    for pub_data in nlp_data:
        if type(pub_data) != np.ndarray:
            positions=[x for x in range(len(pub_data.split()))if pub_data.split()[x]=='{\'score\':']
            if positions:
                for position in positions:
                    sentiment_score += is_number(pub_data.split()[position + 1])
                    sentiment_count += 1
        else:
            for row in pub_data:
                positions=[x for x in range(len(row.split()))if row.split()[x]=='{\'score\':']
                if positions:
                    for position in positions:
                        sentiment_score += is_number(row.split()[position + 1])
                        sentiment_count += 1
    if sentiment_count:
        return sentiment_score / sentiment_count
    else: return 0

def calculate_keywords(nlp_data):
    keywords = []
    for pub_data in nlp_data:
        if type(pub_data) != np.ndarray:
            position = pub_data.find('{\'text\':')
            if position >= 0:
                keywords.append(pub_data[position+10:][:-1])
        else:
            for row in pub_data:
                position = row.find('{\'text\':')
                if position >= 0:
                    keywords.append(row[position+10:][:-1])
    return keywords

def sort_nlp_output(nlp_file_names, nlp_type):
    file_prefix_len = len('nlp_results_')
    sentiment_dictionary = {}
    keyword_dictionary = {}
    for file in nlp_file_names:
        date = file[file_prefix_len:-4]
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, append=1)
            if nlp_type[1:] == 'url':
                nlp_data = np.loadtxt(file,dtype=str,delimiter=',',skiprows=1,usecols=(3,7,17,18))
            elif nlp_type == 'text':
                nlp_data = np.loadtxt(file,dtype=str,delimiter=',',skiprows=1,usecols=(3,6))
        os.remove(file)
        sentiment_dictionary[date] = calculate_sentiment(nlp_data)
        keyword_dictionary[date] = calculate_keywords(nlp_data)
    return keyword_dictionary, sentiment_dictionary

def get_nlp_keywords_and_sentiment_to_file(nlp_dictionary, nlp_type, user_api_key, user_service_url):
    keywords_path, sentiments_path = initiate_path()
    nlp_file_names = nlp.generate_nlp_output(nlp_dictionary, nlp_type[-4:], user_api_key, user_service_url)
    keyword_dic, sentiment_dic = sort_nlp_output(nlp_file_names, nlp_type[-4:])
    write_to_file(keyword_dic, os.path.join(keywords_path, nlp_type[:-5] + '_nlp_keywords.csv'),\
                                                                          ['Date', 'Keywords'])
    write_to_file(sentiment_dic, os.path.join(sentiments_path, nlp_type[:-5] + '_nlp_sentiments.csv'),\
                                                                          ['Date', 'Sentiment'])
